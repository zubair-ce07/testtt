""" Split the String
Define a procedure, split_string, that takes two inputs: the string to split
and a string containing all of the characters considered separators. The
procedure should return a list of strings that break the source string up by
the characters in the splitlist
"""


def split_string(source, split_list):
    result = []
    string = ""
    for s in source:
        if string and s in split_list:
            result.append(string)
            string = ""
        elif s not in split_list:
            string = string + s
    if string not in split_list:
        result.append(string)
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
