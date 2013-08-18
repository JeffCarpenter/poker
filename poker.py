from itertools import groupby, cycle
from collections import defaultdict
from collections import namedtuple
from operator import eq
from enum import Enum
import unittest

# Hand: 5 cards
# Card: Number, suit
Card = namedtuple('card', ('value', 'suit'))

class PrettyEnum(Enum):
    def __str__(self):
        return c.key

Suits = PrettyEnum('clubs', 'spades', 'hearts', 'diamonds')
Categories = PrettyEnum('HighCard', 'OnePair', 'TwoPair', 'ThreeOfAKind', 'Straight', 'Flush', 'FullHouse', 'FourOfAKind', 'StraightFlush')


class Hand(object):
    value_compositions = {
         # (1, 1, 1, 1, 1): 'allunique',
         (1, 4): Categories.FourOfAKind,
         (2, 3): Categories.FullHouse,
         (1, 1, 3): Categories.ThreeOfAKind,
         (1, 2, 2): Categories.TwoPair,
         (1, 1, 1, 2): Categories.OnePair,
    }
    def __init__(self, cards=set()):
        self.cards = cards

    def add_card(self, card):
        self.cards.add(card)

    def groupby_value(self):
        return tuple(tuple(v) for (k, v) in groupby(sorted(self.cards), lambda c: c.value))

    def count_values(self):
        groups = self.groupby_value()
        return tuple(sorted(map(len, groups)))

    def is_flush(self):
        return reduce(eq, tuple(c.suit for c in self.cards))

    def is_straight(self):
        return self.values() == range(self.values()[0], self.values()[-1] + 1)

    # We need to keep the cards that compose the hand associated with the "value composition"
    def get_categories(self):
        categories = set((Categories.HighCard,))
        comp = Hand.value_compositions.get(self.count_values(), None)
        if comp:
            categories.add(comp)
        if self.is_straight():
            categories.add(Categories.Straight)
        if self.is_flush():
            categories.add(Categories.Flush)
        if {Categories.Straight, Categories.Flush}.issubset(categories):
            categories.add(Categories.StraightFlush)

        return categories
    
    def values(self):
        return sorted([c.value for c in self.cards])

    def best_category(self):
        return max(self.get_categories())

    # Need to keep the cards associated with their value composition (count_values)
    # Ie, at some point, we need to seperate the hand from the kicker.
    # And when the best category is determined, we'll want to know what cards comprise it: the others are the kicker.
    def __eq__(self, other):
        return self.best_category() == other.best_category and self.values() == other.values

    def __gt__(self, other):
        return self.best_category() > other.best_category or \
            (self.best_category() == other.best_category and self.values() > other.values)

    def __lt__(self, other):
        return self.best_category() < other.best_category or \
            (self.best_category() == other.best_category and self.values() < other.values)

    def __str__(self):
        return ', '.join(map(str, self.cards))

def values_as_hand(values):
    hand = Hand()
    cards = [Card(v, s) for (v, s) in zip(values, cycle(Suits))]
    return Hand(cards)

class FullHouseTest(unittest.TestCase):
    def runTest(self):
        my_cards = [
            Card(5, 'clubs'),
            Card(5, 'spades'),
            Card(2, 'hearts'),
            Card(2, 'diamonds'),
            Card(2, 'spades')
        ]
        my_hand = Hand(my_cards)
        assert my_hand.best_category == Categories.FullHouse

class StraightTest(unittest.TestCase):
    def runTest(self):
        hand = values_as_hand([2, 3, 4, 5, 6])
        #raise Exception( hand.best_category )
        assert hand.best_category == Categories.Straight
