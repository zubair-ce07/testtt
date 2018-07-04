""" Split the String
Define a procedure, split_string, that takes two inputs: the string to split
and a string containing all of the characters considered separators. The
procedure should return a list of strings that break the source string up by
the characters in the splitlist
"""

import re


def split_string(source, split_list):
    pattern = '|'.join(map(re.escape, split_list))
    result = [string for string in re.split(pattern, source) if string]
    return result

out = split_string("This is a test-of the,string separation-code!", " ,!-")
print out
#>>> ['This', 'is', 'a', 'test', 'of', 'the', 'string', 'separation', 'code']

out = split_string("After  the flood   ...  all the colors came out.", " .")
print out
#>>> ['After', 'the', 'flood', 'all', 'the', 'colors', 'came', 'out']

out = split_string("First Name,Last Name,Street Address,City,State,Zip Code",",")
print out
#>>>['First Name', 'Last Name', 'Street Address', 'City', 'State', 'Zip Code']
