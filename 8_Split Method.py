# coding: utf-8

# The built-in <string>.split() procedure works
# okay, but fails to find all the words on a page
# because it only uses whitespace to split the
# string. To do better, we should also use punctuation
# marks to split the page into words.

# Define a procedure, split_string, that takes two
# inputs: the string to split and a string containing
# all of the characters considered separators. The
# procedure should return a list of strings that break
# the source string up by the characters in the
# splitlist.


def insert(list1, index, list2):
    while '' in list2:
        list2.remove('')
    before_index = list1[:index]
    before_index += list2
    before_index += list1[index + 1:]
    return before_index


def split_string(source, splitlist):
    separators = list(splitlist)
    words = []
    found = 0

    words += source.split(separators[0])
    while '' in words:
        words.remove('')

    separators = separators[1:]
    while len(separators) > 0:
        for index, word in enumerate(words):
            split_word = str(word).split(separators[0])
            found = 0
            if len(split_word) > 1:
                words = insert(words, index, split_word)
                found = 1
                break
        if found == 0:
            separators = separators[1:]
    if '' in words:
        words.remove('')
    return words


out = split_string("This is a test-of the,string separation-code!", " ,!-")
print(out)
# >>> ['This', 'is', 'a', 'test', 'of', 'the', 'string', 'separation', 'code']

out = split_string("After  the flood   ...  all the colors came out.", " .")
print(out)
# >>> ['After', 'the', 'flood', 'all', 'the', 'colors', 'came', 'out']

out = split_string("First Name,Last Name,Street Address,City,State,Zip Code", ",")
print(out)
# >>>['First Name', 'Last Name', 'Street Address', 'City', 'State', 'Zip Code']
