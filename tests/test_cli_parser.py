import unittest
from src.cli_parser import CronParser

class TestCronParser(unittest.TestCase):
    
    def test_basic_every_15_minutes(self):
        expression = CronParser("*/15 0 1,15 * 1-5 /usr/bin/find")
        result = expression.parse()
        self.assertEqual(result['minute'], [0, 15, 30, 45])

    
    def test_every_nth_hour(self):
        expression = CronParser("0 */4 * * * /usr/bin/test")
        result = expression.parse()
        self.assertEqual(result['hour'], [0, 4, 8, 12, 16, 20])

    def test_range_with_steps(self):
        expression = CronParser("0 9-17/2 * * * /usr/bin/test")
        result = expression.parse()
        self.assertEqual(result['hour'], [9, 11, 13, 15, 17])

    def test_multiple_ranges(self):
        expression = CronParser("0 0 1-5,10-15 * * /usr/bin/test")
        result = expression.parse()
        self.assertEqual(result['day of month'], [1, 2, 3, 4, 5, 10, 11, 12, 13, 14, 15])

    def test_valid_expression(self):
        parser = CronParser("*/15 0 1,15 * 1-5 /usr/bin/find")
        result = parser.parse()
        self.assertEqual(result['minute'], [0, 15, 30, 45])
        self.assertEqual(result['hour'], [0])
        self.assertEqual(result['day of month'], [1, 15])
        self.assertEqual(result['month'], list(range(1, 13)))
        self.assertEqual(result['day of week'], [1, 2, 3, 4, 5])
        self.assertEqual(result['command'], ['/usr/bin/find'])


    def test_invalid_expression(self):
        with self.assertRaises(ValueError):
            CronParser("* * * *").parse()


    def test_complex_combinations(self):
        expression = CronParser("*/15 0-12/3 1,15 */4 1-5 /usr/bin/test")
        result = expression.parse()
        self.assertEqual(result['minute'], [0, 15, 30, 45])
        self.assertEqual(result['hour'], [0, 3, 6, 9, 12])
        self.assertEqual(result['day of month'], [1, 15])
        self.assertEqual(result['month'], [1, 5, 9])
        self.assertEqual(result['day of week'], [1, 2, 3, 4, 5])

    def test_single_values(self):
        expression = CronParser("5 10 15 3 2 /usr/bin/test")
        result = expression.parse()
        self.assertEqual(result['minute'], [5])
        self.assertEqual(result['hour'], [10])
        self.assertEqual(result['day of month'], [15])
        self.assertEqual(result['month'], [3])
        self.assertEqual(result['day of week'], [2])

    def test_overlapping_ranges(self):
        expression = CronParser("0 0 1-15,10-20 * * /usr/bin/test")
        result = expression.parse()
        expected_days = list(range(1, 21))
        self.assertEqual(result['day of month'], expected_days)

    def test_step_with_range(self):
        expression = CronParser("0 0 1-30/5 * * /usr/bin/test")
        result = expression.parse()
        self.assertEqual(result['day of month'], [1, 6, 11, 16, 21, 26])

    def test_command_with_arguments(self):
        command = "/usr/bin/find /path -name '*.txt' -type f"
        expression = CronParser("0 0 * * * "+command)
        result = expression.parse()
        self.assertIn(command, result['command'][0])


    def test_invalid_minute_range(self):
        with self.assertRaises(ValueError):
            CronParser("60 * * * * /usr/bin/test").parse()

    def test_invalid_hour_range(self):
        with self.assertRaises(ValueError):
            CronParser("0 24 * * * /usr/bin/test").parse()

    def test_invalid_day_range(self):
        with self.assertRaises(ValueError):
            CronParser("0 0 32 * * /usr/bin/test").parse()

    def test_invalid_month_range(self):
        with self.assertRaises(ValueError):
            CronParser("0 0 * 13 * /usr/bin/test").parse()

    def test_invalid_step_value(self):
        with self.assertRaises(ValueError):
            CronParser("*/0 * * * * /usr/bin/test").parse()


if __name__ == '__main__':
    unittest.main()