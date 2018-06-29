import unittest
import String_manip_functions as funcsModule


class TestValues(unittest.TestCase):
    manual_values_1 = (
        ("techteam", "techam"),
        ("", "0empty"),
        ("sdf3", "0num"),
        ("2", "0num")
    )

    manual_values_2 = (
        ("techteam", "chteam"),
        ("", "0empty"),
        ("sdf3", "0num"),
        ("2", "0num")
    )

    def test_retain_first_occurence_remove_rest(self):
        """
        Tests the function as mentioned in the function name
        """
        for input, expected_output in self.manual_values_1:
            result = funcsModule.retain_first_occurence_remove_rest(input)
            self.assertEqual(expected_output, result)

    def test_retain_last_occurence_remove_rest(self):
        """
        Tests the function as mentioned in the function name
        """
        for input, expected_output in self.manual_values_2:
            result = funcsModule.retain_last_occurence_remove_rest(input)
            self.assertEqual(expected_output, result)

unittest.main()