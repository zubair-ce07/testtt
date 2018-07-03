import unittest
import helpers


class TestValues(unittest.TestCase):
    manual_values_1 = (
        ("techteam", "techam"),
        ("", ValueError),
        ("sdf3", TypeError),
        ("2", TypeError)
    )

    manual_values_2 = (
        ("techteam", "chteam"),
        ("", ValueError),
        ("sdf3", TypeError),
        ("2", TypeError)
    )

    def test_retain_first_occurence_remove_rest(self):
        """
        Tests the function as mentioned in the function name
        """
        for input, expected_output in self.manual_values_1:
            try:
                result = helpers.retain_first_occurence_remove_rest(input)
                self.assertEqual(expected_output, result)
            except TypeError:
                self.assertEqual(expected_output, TypeError)
            except ValueError:
                self.assertEqual(expected_output, ValueError)

    def test_retain_last_occurence_remove_rest(self):
        """
        Tests the function as mentioned in the function name
        """
        for input, expected_output in self.manual_values_2:
            try:
                result = helpers.retain_last_occurence_remove_rest(input)
                self.assertEqual(expected_output, result)
            except TypeError:
                self.assertEqual(expected_output, TypeError)
            except ValueError:
                self.assertEqual(expected_output, ValueError)

unittest.main()
