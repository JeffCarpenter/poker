import unittest
from poker import Hand, Card, Values, Suits, Categories, values_as_hand

def test_equal(label, a, b):
    def runTest(self):
        return self.assertEqual(a, b)
    return type(label, (unittest.TestCase,), {'runTest': runTest})

def test_hand_category(values, category):
    hand = values_as_hand(values)
    return test_equal('%sTest' % category, hand.best_category, category)

# 'HighCard', 'OnePair', 'TwoPair', 'ThreeOfAKind', 'FourOfAKind', 'StraightFlush'
##################
### Unit tests ###
##################
class CategoriesTest(unittest.TestCase):
    def runTest(self):
        Categories.OnePair < Categories.StraightFlush


class FullHouseTest(unittest.TestCase):
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


class StraightTest(unittest.TestCase):
    def runTest(self):
        hand = values_as_hand([2, 3, 4, 5, 6])
        self.assertEqual(hand.best_category, Categories.Straight)


class FlushTest(unittest.TestCase):
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

TwoPair = test_hand_category([2, 2, 3, 4, 5], Categories.OnePair)

class HighCardTest(unittest.TestCase):
    def runTest(self):
        hand = values_as_hand([2, 7, 4, 5, 6])
        self.assertEqual(hand.best_category, Categories.HighCard)
