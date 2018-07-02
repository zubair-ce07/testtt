import unittest
import helpers as funcs_module


class TestValues(unittest.TestCase):
    manual_values_1 = (
        ("techteam", "techam"),
        ("", IndexError),
        ("sdf3", ValueError),
        ("2", ValueError)
    )

    manual_values_2 = (
        ("techteam", "chteam"),
        ("", IndexError),
        ("sdf3", ValueError),
        ("2", ValueError)
    )

    def test_retain_first_occurence_remove_rest(self):
        """
        Tests the function as mentioned in the function name
        """
        for input, expected_output in self.manual_values_1:
            try:
                result = funcs_module.retain_first_occurence_remove_rest(input)
                self.assertEqual(expected_output, result)
            except IndexError:
                self.assertEqual(expected_output, IndexError)
            except ValueError:
                self.assertEqual(expected_output, ValueError)

    def test_retain_last_occurence_remove_rest(self):
        """
        Tests the function as mentioned in the function name
        """
        for input, expected_output in self.manual_values_2:
            try:
                result = funcs_module.retain_last_occurence_remove_rest(input)
                self.assertEqual(expected_output, result)
            except IndexError:
                self.assertEqual(expected_output, IndexError)
            except ValueError:
                self.assertEqual(expected_output, ValueError)

unittest.main()