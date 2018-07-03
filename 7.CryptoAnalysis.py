"""Crypto Analysis: Frequency Analysis.
The input to the function will be an encrypted body of text that only contains the lowercase letters a-z.
As output you should return a list of the normalized frequency for each of the letters a-z.
"""

import string


def freq_analysis(message):
    alphabets = list(string.ascii_lowercase)
    length = len(message)
    result = [float(message.count(a))/length for a in alphabets]
    return result


# Tests

print freq_analysis("abcd")
# >>> [0.25, 0.25, 0.25, 0.25, 0.0, ..., 0.0]

print freq_analysis("adca")
# >>> [0.5, 0.0, 0.25, 0.25, 0.0, ..., 0.0]

print freq_analysis('bewarethebunnies')
# >>> [0.0625, 0.125, 0.0, 0.0, ..., 0.0]
