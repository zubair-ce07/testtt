"""
This module checks if a matrix is symmetric.Returns True if it is symmetric
False otherwise
"""


def check_symmetry(list1, list2):
    """
    General Function to check if two list are the same.
    """
    if len(list1) == len(list2):
        for i in range(0, len(list1)):
            if list1[i] != list2[i]:
                return False
        return True
    return False


def generate_list(m, col, n):
    list2 = [0]*n
    for j in range(0, n):
        list2[j] = m[j][col]

    return list2


def symmetric(matrix):
    n = len(matrix)
    for i in range(0, n):
        list1 = matrix[i]
        list2 = generate_list(matrix, i, n)
        if not check_symmetry(list1, list2):
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