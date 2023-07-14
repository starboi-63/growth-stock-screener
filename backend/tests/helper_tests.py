import unittest
import math
from backend.src.helper_functions import *


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
