"""
This module checks if a matrix is symmetric.Returns True if it is symmetric
False otherwise
"""


def symmetric(matrix):
    length = len(matrix)
    for i in range(0, length):
        list1 = matrix[i]
        list2 = [matrix[j][i] for j in range(0, length)]
        if not list1 == list2:
            return False
    return True

print symmetric([[1, 2, 3], [2, 3, 4], [3, 4, 1]])
#>>> True

print symmetric([["cat", "dog", "fish"],
                ["dog", "dog", "fish"],
                ["fish", "fish", "cat"]])
#>>> True

print symmetric([["cat", "dog", "fish"],
                ["dog", "dog", "dog"],
                ["fish","fish","cat"]])
#>>> False

print symmetric([[1, 2],
                [2, 1]])
#>>> True

print symmetric([[1, 2, 3, 4],
                [2, 3, 4, 5],
                [3, 4, 5, 6]])
#>>> False

print symmetric([[1, 2, 3],
                 [2, 3, 1]])
#>>> False
