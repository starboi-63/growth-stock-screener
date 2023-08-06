import unittest
import math
from ..src.growth_stock_screener.utils import *


class TestPercentChange(unittest.TestCase):
    def test_percent_change_simple(self):
        result = percent_change(1, 2)
        expected = 100.0
        self.assertAlmostEqual(result, expected, places=3)

    def test_percent_change_negative(self):
        result = percent_change(1, 0.4)
        expected = -60.0
        self.assertAlmostEqual(result, expected, places=3)

    def test_percent_change_decimal_input(self):
        result = percent_change(6.3, 9.45)
        expected = 50.0
        self.assertAlmostEqual(result, expected, places=3)

    def test_percent_change_decimal_result(self):
        result = percent_change(100, 100.05)
        expected = 0.05
        self.assertAlmostEqual(result, expected, places=3)

    def test_percent_change_to_zero(self):
        result = percent_change(6.3, 0)
        expected = -100.0
        self.assertAlmostEqual(result, expected, places=3)

    def test_percent_change_zero_div(self):
        self.assertRaises(ZeroDivisionError, percent_change, 0, 6.3)

    def test_percent_change_nan_input(self):
        self.assertRaises(ValueError, percent_change, math.nan, 5)
        self.assertRaises(ValueError, percent_change, 5, math.nan)


class TestRelativeStrength(unittest.TestCase):
    def test_relative_strength_simple(self):
        result = relative_strength(1, 2, 3, 4, 5, 6, 7, 8)
        expected = 36.38095238
        self.assertAlmostEqual(result, expected, places=3)

    def test_relative_strength_nan_inputs(self):
        self.assertRaises(ValueError, relative_strength, math.nan, 2, 3, 4, 5, 6, 7, 8)
        self.assertRaises(ValueError, relative_strength, 1, math.nan, 3, 4, 5, 6, 7, 8)
        self.assertRaises(ValueError, relative_strength, 1, 2, 3, 4, 5, 6, 7, math.nan)

    def test_relative_strength_zero_div(self):
        self.assertRaises(ZeroDivisionError, relative_strength, 0, 2, 3, 4, 5, 6, 7, 8)
        self.assertRaises(ZeroDivisionError, relative_strength, 1, 2, 0, 4, 5, 6, 7, 8)
        self.assertRaises(ZeroDivisionError, relative_strength, 1, 2, 3, 4, 0, 6, 7, 8)
        self.assertRaises(ZeroDivisionError, relative_strength, 1, 2, 3, 4, 5, 6, 0, 8)

    def test_relative_strength_negatives(self):
        result = relative_strength(100, 50, 25, 20, 15, 10, 5, 0)
        expected = -60.66666666

    def test_relative_strength_pos_and_neg(self):
        result = relative_strength(100, 50, 25, 30, 15, 20, 5, 0)
        expected = -39.33333333
