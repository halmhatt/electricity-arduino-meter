from unittest import TestCase

from categorizers.positive_step import PositiveStep


class TestPositiveStep(TestCase):

    def test_similar(self):
        self.assertTrue(PositiveStep.similar([1.0, 1.1]))
        self.assertTrue(PositiveStep.similar([100, 101, 102, 103]))
        self.assertTrue(PositiveStep.similar([1000, 1010]))

        self.assertTrue(PositiveStep.similar([2000, 2086]))

        self.assertFalse(PositiveStep.similar([1, 2]))
        self.assertFalse(PositiveStep.similar([100, 1000]))
