"""Tests for shared outpatient-system validation helpers."""

import unittest

from validators import validate_positive_number


class PositiveNumberValidationTests(unittest.TestCase):
    def test_accepts_finite_positive_numbers(self):
        self.assertEqual(validate_positive_number(12, "Base fee"), 12.0)
        self.assertEqual(validate_positive_number("12.5", "Base fee"), 12.5)

    def test_rejects_non_positive_and_non_finite_numbers(self):
        for value in (0, -1, float("nan"), float("inf"), float("-inf")):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    validate_positive_number(value, "Base fee")


if __name__ == "__main__":
    unittest.main()
