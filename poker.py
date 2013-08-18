from itertools import groupby
from collections import defaultdict
from collections import namedtuple
from operator import eq
import unittest

# Hand: 5 cards
# Card: Number, suit
Card = namedtuple('card', ('value', 'suit'))


class Category(object):
    def __cmp__(self, other):
        return self.__class__.val.__cmp__(other.__class__.val)


class StraightFlush(Category):
    val = 10

class FourOfAKind(Category):
    val = 9

class FullHouse(Category):
    val = 8

class Flush(Category):
    val = 7

class Straight(Category):
    val = 6

class ThreeOfAKind(Category):
    val = 5

class TwoPair(Category):
    val = 4

class OnePair(Category):
    val = 3

class HighCard(Category):
    val = 2

class Hand(object):
    def __init__(self):
        self.cards = set()
        self.value_compositions = {
         # (1, 1, 1, 1, 1): 'allunique',
         (1, 4): FourOfAKind,
         (2, 3): FullHouse,
         (1, 1, 3): ThreeOfAKind,
         (1, 2, 2): TwoPair,
         (1, 1, 1, 2): OnePair,
    }

    def add_card(self, card):
        self.cards.add(card)

    def groupby_value(self):
        return tuple(tuple(v) for (k, v) in groupby(sorted(self.cards), lambda c: c.value))

    def count_values(self):
        groups = self.groupby_value()
        return tuple(sorted(map(len, groups)))

    # This is only used for flushes and highcard
    def is_flush(self):
        return reduce(eq, tuple(c.suit for c in self.cards))

    def is_straight(self):
        cards = list(self.cards)
        return self.cards == range(cards[0].value, cards[-1].value + 1)

    # We need to keep the cards that compose the hand associated with the "value composition"
    def get_categories(self):
        categories = set((HighCard,))
        comp = self.value_compositions.get(self.count_values(), None)
        if comp:
            categories.add(comp)
        if self.is_straight():
            categories.add(Straight)
        if self.is_flush():
            categories.add(Flush)
        if {Straight, Flush}.issubset(categories):
            categories.add(StraightFlush)

        return categories
        
    def best_category(self):
        return max(self.get_categories())

    # Need a way to compare only the cards' values that make up the category.
    # Probably best to have a data structure with the cards associated with their value composition (count_values)
    def __eq__(self, other):
        return self.best_category() == other.best_category() and all([c[0].value == c[1].value for c in zip(self.cards, other._cards)])

    def __gt__(self, other):
        return self.best_category() > other.best_category()

    def __lt__(self, other):
        return self.best_category() < other.best_category()


class MyTest(unittest.TestCase):
    def test_fullhouse(self):

        my_cards = [
            Card(5, 'clubs'),
            Card(5, 'spades'),
            Card(2, 'hearts'),
            Card(2, 'diamonds'),
            Card(2, 'spades')
        ]
        my_hand = Hand()
        my_hand.cards = my_cards
        assert my_hand.best_category() == FullHouse