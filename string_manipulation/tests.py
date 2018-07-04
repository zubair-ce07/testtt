import unittest
import helpers
from ddt import ddt, data

@ddt
class TestValues(unittest.TestCase):
    manual_values_1 = {
        "techteam": "techam",
        "": ValueError,
        "sdf3": TypeError,
        "2": TypeError
    }

    manual_values_2 = {
        "techteam": "chteam",
        "": ValueError,
        "sdf3": TypeError,
        "2": TypeError
    }

    @data("techteam", "", "sdf3", "2")
    def test_retain_first_occurence_remove_rest(self, value):
        """
        Tests the function as mentioned in the function name
        """
        try:
            result = helpers.retain_first_occurence_remove_rest(value)
            self.assertEqual(self.manual_values_1[value], result)
        except TypeError:
            self.assertEqual(self.manual_values_1[value], TypeError)
        except ValueError:
            self.assertEqual(self.manual_values_1[value], ValueError)

    @data("techteam", "", "sdf3", "2")
    def test_retain_last_occurence_remove_rest(self, value):
        """
        Tests the function as mentioned in the function name
        """
        try:
            result = helpers.retain_last_occurence_remove_rest(value)
            self.assertEqual(self.manual_values_2[value], result)
        except TypeError:
            self.assertEqual(self.manual_values_2[value], TypeError)
        except ValueError:
            self.assertEqual(self.manual_values_2[value], ValueError)

unittest.main()
