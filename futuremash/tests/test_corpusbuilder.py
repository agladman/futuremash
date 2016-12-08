#!/usr/bin/env Python3


import unittest
from futuremash import corpusbuilder


class TestAgeCalcMethods(unittest.TestCase):

    default = 10368000  # must match default given in code

    def test_age_limit_to_seconds(self):
        self.assertEqual(
            corpusbuilder.age_limit_to_seconds(30), 2592000)

    def test_age_limit_to_seconds_negvalue(self):
        self.assertEqual(
            corpusbuilder.age_limit_to_seconds(-10), self.default)

    def test_age_limit_to_seconds_zero(self):
        self.assertEqual(
            corpusbuilder.age_limit_to_seconds(0), self.default)

    def test_age_limit_to_seconds_str(self):
        self.assertEqual(
            corpusbuilder.age_limit_to_seconds('0'), self.default)

    def test_age_limit_to_seconds_noparam(self):
        self.assertEqual(
            corpusbuilder.age_limit_to_seconds(), self.default)


if __name__ == '__main__':
    unittest.main()
