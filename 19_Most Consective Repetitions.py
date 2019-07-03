# coding: utf-8


# Longest Repetition

# Define a procedure, longest_repetition, that takes as input a
# list, and returns the element in the list that has the most
# consecutive repetitions. If there are multiple elements that
# have the same number of longest repetitions, the result should
# be the one that appears first. If the input list is empty,
# it should return None.
from collections import OrderedDict
import heapq


def longest_repetition(li):
    if len(li) == 0:
        return None
    consec_occurences = OrderedDict()
    pos = 0
    i = 0
    while i < len(li):
        consec_occurences[li[i]] = [1, pos]
        j = i + 1
        while j < len(li) and li[i] == li[j]:
            consec_occurences[li[i]][0] += 1
            consec_occurences[li[i]][1] = pos
            j += 1
        i += j - i
        pos += 1
    return sorted(consec_occurences.items(), key=lambda x: x[1][0],
                  reverse=True)[0][0]


# For example,

print(longest_repetition([1, 2, 2, 3, 3, 3, 2, 2, 1]))
# 3

print(longest_repetition(['a', 'b', 'b', 'b', 'c', 'd', 'd', 'd']))
# b

print(longest_repetition([1, 2, 3, 4, 5]))
# 1

print(longest_repetition([]))
# None
