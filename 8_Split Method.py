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


def split_string(source, splitlist):
    separators = list(splitlist)
    words = []
    subwords = []
    to_remove = []

    words += source.split(separators[0])
    separators = separators[1:]
    while len(separators) > 0:
        for word in words:
            split_word = str(word).split(separators[0])
            if len(split_word) > 1:
                to_remove.append(word)
                subwords += split_word
        words += subwords
        # print (words)
        words = list(dict.fromkeys(words))
        for word in to_remove:
            words.remove(word)
        subwords = []
        to_remove = []
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
