from unittest import TestCase, skip
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
    def setUp(self):
        cards = {
            Card(5, Suits.Clubs),
            Card(5, Suits.Spades),
            Card(2, Suits.Hearts),
            Card(2, Suits.Diamonds),
            Card(2, Suits.Spades),
        }
        self.hand = Hand(cards)
    def test_category(self):
        self.assertEqual(self.hand.best_category, Categories.FullHouse, self.hand.count_groups())
    def test_kickers(self):
        self.assertEqual(self.hand.kickers, set())

class StraightFlushTest(TestCase):
    def setUp(self):
        cards = {Card(v, s) for (v, s) in zip(range(7), repeat(Suits.Spades))}
        self.hand = Hand(cards)
        
    def test_category(self):
        self.assertEqual(self.hand.best_category, Categories.StraightFlush)
    def test_kickers(self):
        self.assertEqual(self.hand.kickers, set())

class StraightTest(TestCase):
    def setUp(self):
        self.hand = values_as_hand([2, 3, 4, 5, 6])
    def test_category(self):    
        self.assertEqual(self.hand.best_category, Categories.Straight)
    def test_kickers(self):
        self.assertEqual(self.hand.kickers, set())


class FlushTest(TestCase):
    def setUp(self):
        cards = {
            Card(1, Suits.Clubs),
            Card(2, Suits.Clubs),
            Card(5, Suits.Clubs),
            Card(6, Suits.Clubs),
            Card(7, Suits.Clubs)
        }
        self.hand = Hand(cards)
    def test_category(self):
        self.assertEqual(self.hand.best_category, Categories.Flush)
    def test_kickers(self):
        self.assertEqual(self.hand.kickers, set())

# TODO: Change these into ordinary, red-blooded, God-fearing, apple pie-loving unit tests
FourOfAKind = test_hand_category([9, 9, 9, 9, 7], Categories.FourOfAKind)
ThreeOfAKind = test_hand_category([1, 1, 1, 4, 5], Categories.ThreeOfAKind)

class OnePair(TestCase):
    def setUp(self):
        self.hand = values_as_hand([2, 2, 3, 4, 5])
    def test_category(self):
        self.assertEqual(self.hand.best_category, Categories.OnePair)
    def test_kickers(self):
        kickers_values = {c.value for c in self.hand.kickers}
        self.assertEqual(kickers_values, {3, 4, 5})

class TwoPair(TestCase):
    def setUp(self):
        self.hand = values_as_hand([2, 2, 3, 3, 6])
    def test_category(self):
        self.assertEqual(self.hand.best_category, Categories.TwoPair)
    def test_kickers(self):
        kicker = self.hand.kickers.pop()
        self.assertEqual(kicker.value, 6, kicker)
    def test_punchers(self):
        pairs_values = {c.value for c in self.hand.punchers}
        self.assertEqual(pairs_values, {2, 2, 3, 3})


class HighCardTest(TestCase):
    def setUp(self):
        self.hand = values_as_hand([2, 7, 4, 5, 6])
    def test_category(self):
        self.assertEqual(self.hand.best_category, Categories.HighCard)
    def test_kickers(self):
        kicker_values = {c.value for c in self.hand.kickers}
        self.assertEqual(kicker_values, {2, 4, 5, 6})
    def test_punchers(self):
        high_card = self.hand.punchers.pop()
        self.assertEqual(high_card.value, 7)


class TwoPairVsOnePair(TestCase):
    def runTest(self):
        one_pair = values_as_hand([2, 2, 5, 5, 6])
        two_pair = values_as_hand([1, 1, 3, 4, 7])
        self.assertGreater(one_pair, two_pair)


class TwoPairVsTwoPair(TestCase):
    pass