from unittest import TestCase
from itertools import repeat
from poker import Hand, Card, Values, Suits, Categories, values_as_hand

def test_equal(label, a, b):
    def runTest(self):
        return self.assertEqual(a, b)
    return type(label, (TestCase,), {'runTest': runTest})


def test_hand_category(values, category):
    hand = values_as_hand(values)
    return test_equal('%sTest' % category, hand.best_category, category)

class CategoriesTest(TestCase):
    def runTest(self):
        Categories.OnePair < Categories.StraightFlush


class FullHouseTest(TestCase):
    def runTest(self):
        cards = {
            Card(5, Suits.Clubs),
            Card(5, Suits.Spades),
            Card(2, Suits.Hearts),
            Card(2, Suits.Diamonds),
            Card(2, Suits.Spades),
        }
        hand = Hand(cards)
        self.assertEqual(hand.best_category, Categories.FullHouse, hand.count_groups())


class StraightFlushTest(TestCase):
    def runTest(self):
        cards = {Card(v, s) for (v, s) in zip(range(7), repeat(Suits.Spades))}
        hand = Hand(cards)
        self.assertEqual(hand.best_category, Categories.StraightFlush)


class StraightTest(TestCase):
    def runTest(self):
        hand = values_as_hand([2, 3, 4, 5, 6])
        self.assertEqual(hand.best_category, Categories.Straight)


class FlushTest(TestCase):
  def runTest(self):
    cards = {
        Card(1, Suits.Clubs),
        Card(2, Suits.Clubs),
        Card(5, Suits.Clubs),
        Card(6, Suits.Clubs),
        Card(7, Suits.Clubs)
    }
    hand = Hand(cards)
    self.assertEqual(hand.best_category, Categories.Flush)


FourOfAKind = test_hand_category([9, 9, 9, 9, 7], Categories.FourOfAKind)
ThreeOfAKind = test_hand_category([1, 1, 1, 4, 5], Categories.ThreeOfAKind)
OnePair = test_hand_category([2, 2, 3, 4, 5], Categories.OnePair)
TwoPair = test_hand_category([2, 2, 3, 3, 6], Categories.TwoPair)


class HighCardTest(TestCase):
    def runTest(self):
        hand = values_as_hand([2, 7, 4, 5, 6])
        self.assertEqual(hand.best_category, Categories.HighCard)
