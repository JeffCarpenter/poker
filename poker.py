#!/usr/bin/env python2

from itertools import groupby, cycle, repeat
from collections import defaultdict
from collections import namedtuple
from enum import Enum
import unittest

"""
4 types of combinations:
    1. Value combination (ie. 3 Kings and 2 Queens -> full house)
    2. Same suit (flush)
    3. Incr value (straight)
    4. 2 & 3 (straight flush)
"""

class Card(object):
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def __cmp__(self, other):
        return self.value.__cmp__(other.value)

    def __str__(self):
        return '%s of %s' % (self.value, self.suit)

    def __repr__(self):
        return '<Card(value=%s, suit=%s)>' % (self.value, self.suit)

Suits = Enum('Clubs', 'Spades', 'Hearts', 'Diamonds')
Values = Enum('One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', ' Queen', 'King', 'Ace')
Categories = Enum('HighCard', 'OnePair', 'TwoPair', 'ThreeOfAKind', 'Straight', 'Flush', 'FullHouse', 'FourOfAKind', 'StraightFlush')


class Hand(object):
    value_compositions = {
         (1, 4): Categories.FourOfAKind,
         (2, 3): Categories.FullHouse,
         (1, 1, 3): Categories.ThreeOfAKind,
         (1, 2, 2): Categories.TwoPair,
         (1, 1, 1, 2): Categories.OnePair,
    }
    def __init__(self, cards=set()):
        self.cards = cards

    def rank(self):
        self.category = self.get_categories()

    def add_card(self, card):
        self.cards.add(card)

    def groupby_value(self):
        return tuple(tuple(v) for (k, v) in groupby(sorted(self.cards), lambda c: c.value))

    def count_groups(self):
        return tuple((len(g), g) for g in self.groupby_value())

    def count_values(self):
        groups = self.groupby_value()
        return tuple(sorted(map(len, groups)))

    def is_flush(self):
        return len({c.suit for c in self.cards}) == 1

    def is_straight(self):
        return self.values == range(self.values[0], self.values[-1] + 1)

    # We need to keep the cards that compose the hand associated with the "value composition"
    def get_categories(self):
        categories = set()
        comp = Hand.value_compositions.get(self.count_values(), Categories.HighCard)
        categories.add(comp)
        if self.is_straight():
            categories.add(Categories.Straight)
        if self.is_flush():
            categories.add(Categories.Flush)
        if {Categories.Straight, Categories.Flush}.issubset(categories):
            categories.add(Categories.StraightFlush)
        return categories

    @property
    def punchers(self):
        return self.cards - self.kickers

    @property
    def kickers(self):
        cat = self.best_category
        if cat in {Categories.StraightFlush, Categories.Flush, Categories.Straight}:
            return set()
        elif cat == Categories.HighCard:
            return set(sorted(self.cards)[:-1])
        else:
            kicker_groups = {g for (i, g) in self.count_groups() if i == 1}
            kickers = set()
            for group in kicker_groups:
                for card in group:
                    kickers.add(card)
            return kickers

    @property
    def values(self):
        return sorted([c.value for c in self.cards])

    @property
    def best_category(self):
        return max(self.get_categories())

    # TODO: Keep the cards associated with their value composition (count_values) in order to seperate the hand from the kicker.
    def __eq__(self, other):
        return self.best_category == other.best_category and self.values == other.values

    def __gt__(self, other):
        return self.best_category > other.best_category or \
            (self.best_category == other.best_category and self.values > other.values)

    def __lt__(self, other):
        return self.best_category < other.best_category or \
            (self.best_category == other.best_category and self.values < other.values)

    def __str__(self):
        return ', '.join(map(str, self.cards))

    def __repr__(self):
        return '<Hand(cards=%r, best_category=%r)>' % (self.cards, self.best_category)

def values_as_hand(values):
    hand = Hand()
    cards = {Card(v, s) for (v, s) in zip(values, cycle(Suits))}
    return Hand(cards)
