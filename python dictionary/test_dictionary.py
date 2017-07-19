__author__ = 'luqman'


import unittest
from dictionary import SparseList, Dictionary


class SparseListTestCase(unittest.TestCase):
    def setUp(self):
        self.sparse_list = SparseList()
        self.sparse_list[1] = 10
        self.sparse_list[5] = 20
        self.sparse_list['abc'] = 30
        self.sparse_list[7] = 40

    def test_at_key_1__getitem__(self):
        self.assertEqual(self.sparse_list[1].items[0],
                         10,
                         msg='first inserted key value pair')

    def test_at_key_7__getitem__(self):
        self.assertEqual(self.sparse_list[7].items[0],
                         40,
                         msg='last inserted key value pair')

    def test_at_key_abc__getitem__(self):
        self.assertEqual(self.sparse_list['abc'].items[0],
                         30,
                         msg='if sparse list accepts string key')

    def test_at_key_efg__getitem__(self):
        self.assertIsNone(self.sparse_list['efg'],
                          msg='if key does not exists sparse list should return None')


class DictionaryTestCase(unittest.TestCase):
    def setUp(self):
        self.dictionary = Dictionary()
        self.dictionary[1] = 10
        self.dictionary[2] = 20
        self.dictionary[1] = 50
        self.dictionary['abc'] = 30
        self.dictionary[4] = 'efg'

    def test_at_key_1__getitem__(self):
        self.assertEquals(self.dictionary[1],
                          50,
                          msg='over writing value at specific key')

    def test_at_key_abc__getitem__(self):
        self.assertEquals(self.dictionary['abc'],
                          30,
                          msg='testing string key')

    def test_at_key_4__getitem__(self):
        self.assertEquals(self.dictionary[4],
                          'efg',
                          msg='testing string values')

    def test_at_key_20__getitem__(self):
        self.assertIsNone(self.dictionary[20],
                          msg='if key does not exists return None')

    def test_list_values(self):
        self.assertEqual(self.dictionary.values(),
                         [50, 20, 'efg', 30],
                         msg='should return all list of values')

    def test_list_keys(self):
        self.assertEqual(self.dictionary.keys(),
                         [1, 2, 4, 'abc'],
                         msg='should return all list of keys')

    def test_clear(self):
        self.dictionary.clear()
        self.assertTrue((len(self.dictionary.hash_table) == 0) and (self.dictionary.size == 0),
                        msg='hash table size and dictionary size should be 0')

    def test_copy(self):
        dictionary_copy = self.dictionary.copy()
        self.assertEqual(self.dictionary, dictionary_copy,
                         msg='both variables should point to same reference')

    def test_at_key_1_exists_get(self):
        self.assertEqual(self.dictionary.get(1, 'not found'),
                         50,
                         msg='if key exists value against key should be returned else default value should be returned')

    def test_at_key_20_not_exists_get(self):
        self.assertEqual(self.dictionary.get(20, 'not found'),
                         'not found',
                         msg='if key exists value against key should be returned else default value should be returned')

    def test_at_key_20_not_exists_set_default(self):
        self.dictionary.set_default(20, 'value set')
        self.assertEqual(self.dictionary[20],
                         'value set',
                         msg='if key does not exists set default value against key')

    def test_at_key_1_exists_set_default(self):
        self.dictionary.set_default(1, 'value set')
        self.assertNotEqual(self.dictionary[1],
                            'value set',
                            msg='if key does not exists set default value against key')

    def test_at_key_4_exists_has_key(self):
        self.assertTrue(self.dictionary.has_key(4),
                        msg='if dictionary has key return True else False')

    def test_at_key_0_not_exists_has_key(self):
        self.assertFalse(self.dictionary.has_key(0),
                         msg='if dictionary has key return True else False')

    def test_at_key_abc_pop(self):
        value = self.dictionary.pop('abc')
        self.assertTrue((value == 30) and (self.dictionary['abc'] is None),
                        msg='value should be return and popped from dictionary')

    def test_items(self):
        self.assertEqual(self.dictionary.items(),
                         [(1, 50), (2, 20), (4, 'efg'), ('abc', 30)],
                         msg='should return all key value pairs in the dictionary')

    def test_update(self):
        another_dictionary = Dictionary()
        another_dictionary[1] = 5
        another_dictionary['qwe'] = 'rty'

        self.dictionary.update(another_dictionary)

        self.assertEqual(self.dictionary.items(),
                         [(1, 5), (2, 20), (4, 'efg'),
                          ('abc', 30), ('qwe', 'rty')],
                         msg='dictionary should be updated with all the key value pairs of other dictionary')

    def test__len__(self):
        self.assertEqual(len(self.dictionary),
                         4,
                         msg='should return current number of key value pairs')

    def test__str__(self):
        self.assertEqual(str(self.dictionary),
                         "{1:50, 2:20, 4:'efg', 'abc':30}",
                         msg='should return string form of dictionary')


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(SparseListTestCase))
    suite.addTest(unittest.makeSuite(DictionaryTestCase))
    return suite


if __name__ == '__main__':
    unittest.main()
