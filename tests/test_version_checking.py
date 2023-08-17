import unittest
from growth_stock_screener.screen.iterations.utils import *


class TestVersionGeq(unittest.TestCase):
    def test_versions_simple(self):
        result = version_geq("1", "0")
        expected = True
        self.assertEqual(result, expected)

        result = version_geq("1", "1")
        expected = True
        self.assertEqual(result, expected)

        result = version_geq("10", "1")
        expected = True
        self.assertEqual(result, expected)

        result = version_geq("0", "1")
        expected = False
        self.assertEqual(result, expected)

        result = version_geq("1", "2")
        expected = False
        self.assertEqual(result, expected)

        result = version_geq("1", "10")
        expected = False
        self.assertEqual(result, expected)

    def test_versions_two_places(self):
        result = version_geq("1.0", "0.1")
        expected = True
        self.assertEqual(result, expected)

        result = version_geq("6.3", "3.4")
        expected = True
        self.assertEqual(result, expected)

        result = version_geq("0.0", "0.0")
        expected = True
        self.assertEqual(result, expected)

        result = version_geq("6.3", "6.3")
        expected = True
        self.assertEqual(result, expected)

        result = version_geq("0.1", "1.0")
        expected = False
        self.assertEqual(result, expected)

        result = version_geq("3.4", "6.3")
        expected = False
        self.assertEqual(result, expected)

        result = version_geq("3.5", "3.6")
        expected = False
        self.assertEqual(result, expected)

        result = version_geq("3.6", "3.5")
        expected = True
        self.assertEqual(result, expected)

    def test_versions_three_places(self):
        result = version_geq("3.6.3", "3.6.0")
        expected = True
        self.assertEqual(result, expected)

        result = version_geq("3.6.3", "3.6.1")
        expected = True
        self.assertEqual(result, expected)

        result = version_geq("3.6.3", "3.5.3")
        expected = True
        self.assertEqual(result, expected)

        result = version_geq("3.6.3", "3.5.4")
        expected = True
        self.assertEqual(result, expected)

        result = version_geq("3.6.3", "2.10.100")
        expected = True
        self.assertEqual(result, expected)

        result = version_geq("3.6.3", "3.6.3")
        expected = True
        self.assertEqual(result, expected)

        result = version_geq("3.6.3", "3.6.30")
        expected = False
        self.assertEqual(result, expected)

        result = version_geq("3.6.3", "3.7.3")
        expected = False
        self.assertEqual(result, expected)

        result = version_geq("3.6.3", "4.6.3")
        expected = False
        self.assertEqual(result, expected)

        result = version_geq("0.0.1", "00.00.2")
        expected = False
        self.assertEqual(result, expected)

    def test_versions_diff_lens(self):
        result = version_geq("1", "00.00.00")
        expected = True
        self.assertEqual(result, expected)

        result = version_geq("1", "1.0.0")
        expected = True
        self.assertEqual(result, expected)

        result = version_geq("1.0", "1.0.0")
        expected = True
        self.assertEqual(result, expected)

        result = version_geq("1.5", "1.5.0")
        expected = True
        self.assertEqual(result, expected)

        result = version_geq("6.38.49", "6.37.50.71")
        expected = True
        self.assertEqual(result, expected)

        result = version_geq("1.1.1", "1.1")
        expected = True
        self.assertEqual(result, expected)

        result = version_geq("3.11.4", "3.11")
        expected = True
        self.assertEqual(result, expected)

        result = version_geq("0.11.3", "0.11")
        expected = True
        self.assertEqual(result, expected)

        result = version_geq("1.1.1", "1.1.1.1")
        expected = False
        self.assertEqual(result, expected)

        result = version_geq("1.0.0.1", "1.0.1")
        expected = False
        self.assertEqual(result, expected)

        result = version_geq("3", "4.0.16")
        expected = False
        self.assertEqual(result, expected)

        result = version_geq("3.11", "3.11.4")
        expected = False
        self.assertEqual(result, expected)

        result = version_geq("3.11.2.27", "4")
        expected = False
        self.assertEqual(result, expected)

        result = version_geq("0.11", "0.11.3")
        expected = False
        self.assertEqual(result, expected)

        result = version_geq("3.10.12", "3.11")
        expected = False
        self.assertEqual(result, expected)

        result = version_geq("3.11", "3.10.12")
        expected = True
        self.assertEqual(result, expected)

        result = version_geq("3.10.12", "3.11")
        expected = False
        self.assertEqual(result, expected)

        result = version_geq("3.11", "3.10.12")
        expected = True
        self.assertEqual(result, expected)
