from dictionary import MyDictionary

# initializing Dictionary
dictionary = MyDictionary()

# inserting values in dictionary
dictionary['a'] = 8
dictionary['b'] = 2
dictionary[1] = None
dictionary[5] = 10
print dictionary

# over writing dictionary key value
dictionary['a'] = 9
print dictionary

# deleting key-value pair from dictionary
del dictionary['a']
print dictionary

# return key-value pair tuples
print dictionary.items()

# list of values stored in dictionary
print dictionary.values()

# list of keys stored in dictionary
print dictionary.keys()

# if key exists return value else return default provided value
print dictionary.get('z', 'No value')

# if key exists return value else set key value equal to default
print dictionary.set_default('z', 'Done')

# setting a dictionary against a key
another_dictionary = MyDictionary()
another_dictionary['hello'] = 'world'
another_dictionary['test'] = 'successful'
dictionary['another_dictionary'] = another_dictionary
print dictionary
# update dictionary with key-value pairs of other dictionary
another_dictionary['update_dictionary'] = 'updated'
dictionary.update(another_dictionary)
print dictionary

# get a dictionary from a set of sequence and a assign a against keys
another_dictionary = MyDictionary().fromkeys(('name', 'age', 'sex'), 10)
print another_dictionary

# shallow copy of the dictionary
another_dictionary = dictionary.copy()
another_dictionary['dictionary'] = 'copied'
print dictionary
