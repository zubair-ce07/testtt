import unittest

from custom_list import CustomList


class CustomListTestCase(unittest.TestCase):
    def setUp(self):
        self.custom_list = CustomList()
        self.custom_list.extend([3, 2.12, 3, "string", [1, 2, "123"]])
        self.custom_list[3] = "changed"

    def test_len_function(self):
        self.assertEqual(len(self.custom_list), 5, msg="Get the length of the CustomList")

    def test_getitem_with_key_3(self):
        self.assertEqual(self.custom_list[3], "changed", msg="Get the Value at index 3")

    def test_getitem_with_key_minus_1(self):
        self.assertEqual(self.custom_list[-1], [1, 2, "123"], msg="Get the Value at index -1")

    def test_getitem_with_key_7(self):
        self.assertRaises(IndexError, lambda: self.custom_list[7])

    def test__add__with_CustomList(self):
        custom_list = CustomList()
        custom_list.extend([1, 2, 1])
        added_list = CustomList()
        added_list.extend([3, 2.12, 3, "changed", [1, 2, "123"], 1, 2, 1])
        self.assertEqual(self.custom_list + custom_list, added_list, msg="Get an added CustomList")

    def test__contains__with_obj_3(self):
        self.assertEqual(self.custom_list.__contains__(3), True, msg="Check membership of object")

    def test__mul__with_obj_2(self):
        repeated_list = CustomList()
        repeated_list.extend([3, 2.12, 3, "changed", [1, 2, "123"], 3, 2.12, 3, "changed", [1, 2, "123"]])
        self.assertEqual(self.custom_list * 2, repeated_list, msg="Get a repeated custom list ")

    def test_append_function(self):
        custom_list = CustomList()
        custom_list.append(3)
        custom_list.append(2.12)
        custom_list.append(3)
        custom_list.append("changed")
        custom_list.append([1, 2, "123"])
        self.assertEqual(custom_list, self.custom_list, msg="Check the append function")

    def test_count_function(self):
        self.assertEqual(self.custom_list.count(3), 2, msg="Check the count function")

    def test_index_function_with_obj_changed(self):
        self.assertEqual(self.custom_list.index("changed"), 3, msg="Get the index of the object")

    def test_insert_with_obj_10_index_3(self):
        custom_list1 = CustomList()
        custom_list1.extend([1, 2, 3, 4, 5])
        custom_list1.insert(3, 10)
        inserted_list = CustomList()
        inserted_list.extend([1, 2, 3, 10, 4, 5])
        self.assertEqual(custom_list1, inserted_list, msg="check the insert function")

    def test_pop_function(self):
        custom_list1 = CustomList()
        custom_list1.extend([1, 2, 3, "xyz"])
        self.assertEqual(custom_list1.pop(), "xyz", msg="get the popped item")

    def test_remove_function_with_obj_changed(self):
        custom_list1 = CustomList()
        custom_list1.extend([3, 2.12, 3, [1, 2, "123"]])
        custom_list2 = self.custom_list.copy()
        custom_list2.remove("changed")
        self.assertEqual(custom_list2, custom_list1, msg="check remove function")

    def test_reverse_function(self):
        custom_list1 = CustomList()
        custom_list1.extend([[1, 2, "123"], "changed", 3, 2.12, 3])
        self.custom_list.reverse()
        self.assertEqual(self.custom_list, custom_list1, msg="check reverse function")

    def test_sort_function(self):
        custom_list1 = CustomList()
        custom_list1.extend([2.12, 3, 3, [1, 2, '123'], "changed"])
        self.custom_list.sort()
        self.assertEqual(self.custom_list, custom_list1, msg="Check sort function")

    def test_copy_function(self):
        self.assertEqual(self.custom_list, self.custom_list.copy(), msg="Check copy function")

    def test_clear_function(self):
        custom_list1 = CustomList()
        self.custom_list.clear()
        self.assertEqual(self.custom_list, custom_list1, msg="Check Clear function")


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(CustomListTestCase))
    return suite


if __name__ == '__main__':
    unittest.main()
