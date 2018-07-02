""" Soduku Checker.
This module returns true if the following
conditions are met:
1. Each column of the square contains each of the whole
numbers from 1 to n exactly once.

2. Each row of the square contains each of the whole
numbers from 1 to n exactly once.
"""


correct = [[1, 2, 3],
           [2, 3, 1],
           [3, 1, 2]]

incorrect = [[1, 2, 3, 4],
             [2, 3, 1, 3],
             [3, 1, 2, 3],
             [4, 4, 4, 4]]

incorrect2 = [[1, 2, 3, 4],
              [2, 3, 1, 4],
              [4, 1, 2, 3],
              [3, 4, 1, 2]]

incorrect3 = [[1, 2, 3, 4, 5],
              [2, 3, 1, 5, 6],
              [4, 5, 2, 1, 3],
              [3, 4, 5, 2, 1],
              [5, 6, 4, 3, 2]]

incorrect4 = [['a', 'b', 'c'],
              ['b', 'c', 'a'],
              ['c', 'a', 'b']]

incorrect5 = [[1, 1.5],
              [1.5, 1]]

matrix6 = [[1, 1.5, 3],
           [3, 1, 1.5],
           [1.5, 3, 1]]


def check_repetition_in_rows(matrix, n):
    """
    Checks if repetition is found in Rows of a matrix
    """
    for i in range(0, n):
        row = [True] * n
        for j in range(0, n):
            if 1 <= matrix[i][j] <= n and isinstance(matrix[i][j], (int, long)) \
                    and row[matrix[i][j] - 1]:
                row[matrix[i][j] - 1] = False
            else:
                return False
    return True


def check_repetition_in_columns(matrix, n):
    """
    Checks if repetition is found in Columns of a matrix
    """
    for i in range(0, n):
        col = [True] * n
        for j in range(0, n):
            if 1 <= matrix[j][i] <= n and isinstance(matrix[i][j], (int, long)) \
                    and col[matrix[i][j] - 1]:
                col[matrix[j][i] - 1] = False
            else:
                return False
    return True


def check_sudoku(matrix):
    n = len(matrix)
    if check_repetition_in_rows(matrix, n):
        return check_repetition_in_columns(matrix, n)
    else:
        return False


print check_sudoku(incorrect)
#>>> False

print check_sudoku(correct)
#>>> True

print check_sudoku(incorrect2)
#>>> False

print check_sudoku(incorrect3)
#>>> False

print check_sudoku(incorrect4)
#>>> False

print check_sudoku(incorrect5)
#>>> False

print check_sudoku(matrix6)
#>>> False

