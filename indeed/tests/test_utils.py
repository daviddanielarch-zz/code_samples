from unittest import TestCase

from utils import combinations


class TestCombinations(TestCase):
    def setUp(self):
        pass

    def test_3_tokens(self):
        new_york_combinations = list(combinations('New York City'))
        self.assertEqual(len(new_york_combinations), 3)
        self.assertEqual(new_york_combinations[0], 'New')
        self.assertEqual(new_york_combinations[1], 'New York')
        self.assertEqual(new_york_combinations[2], 'New York City')