# coding: utf-8


# Longest Repetition

# Define a procedure, longest_repetition, that takes as input a
# list, and returns the element in the list that has the most
# consecutive repetitions. If there are multiple elements that
# have the same number of longest repetitions, the result should
# be the one that appears first. If the input list is empty,
# it should return None.


def longest_repetition(li):
    if len(li) == 0:
        return None
    occurrences = 1
    occurrent = li[0]
    i = 0
    while i < len(li):
        j = i + 1
        latest_count = 0
        while j < len(li) and li[i] == li[j]:
            latest_count += 1
            j += 1
        if latest_count + 1 > occurrences:
            occurrences = latest_count + 1
            occurrent = li[i]
        i += j - i
    return occurrent


# For example,

print(longest_repetition([1, 2, 2, 3, 3, 3, 2, 2, 1]))
# 3

print(longest_repetition(['a', 'b', 'b', 'b', 'c', 'd', 'd', 'd']))
# b

print(longest_repetition([1, 2, 3, 4, 5]))
# 1

print(longest_repetition([]))
# None
