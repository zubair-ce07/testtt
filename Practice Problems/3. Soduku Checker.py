# THREE GOLD STARS

# Sudoku [http://en.wikipedia.org/wiki/Sudoku]
# is a logic puzzle where a game
# is defined by a partially filled
# 9 x 9 square of digits where each square
# contains one of the digits 1,2,3,4,5,6,7,8,9.
# For this question we will generalize
# and simplify the game.

# Define a procedure, check_sudoku,
# that takes as input a square list
# of lists representing an n x n
# sudoku puzzle solution and returns the boolean
# True if the input is a valid
# sudoku square and returns the boolean False
# otherwise.

# A valid sudoku square satisfies these
# two properties:

#   1. Each column of the square contains
#       each of the whole numbers from 1 to n exactly once.

#   2. Each row of the square contains each
#       of the whole numbers from 1 to n exactly once.

# You may assume the the input is square and contains at
# least one row and column.

correct = [[1,2,3],
           [2,3,1],
           [3,1,2]]

incorrect = [[1,2,3,4],
             [2,3,1,3],
             [3,1,2,3],
             [4,4,4,4]]

incorrect2 = [[1,2,3,4],
              [2,3,1,4],
              [4,1,2,3],
              [3,4,1,2]]

incorrect3 = [[1,2,3,4,5],
              [2,3,1,5,6],
              [4,5,2,1,3],
              [3,4,5,2,1],
              [5,6,4,3,2]]

incorrect4 = [['a','b','c'],
              ['b','c','a'],
              ['c','a','b']]

incorrect5 = [ [1, 1.5],
               [1.5, 1]]

matrix6 = [[1,1.5,3],[3,1,1.5],[1.5,3,1]]


def check_row(matrix):
    try:
        for index_i, val_i in matrix:
            lis = range(1, len(matrix)+1)
            for index_j, val_j in val_i:
                lis.remove(matrix[index_i][index_j])
    except:
        return False
    return True


def check_col(matrix):
    try:
        for index_i, val_i in matrix:
            lis = range(1, len(matrix)+1)
            for index_j, val_j in val_i:
                lis.remove(matrix[index_j][index_i])
    except:
        return False
    return True


# In[33]:


def check_sudoku(matrix):
    return check_row(matrix) and check_col(matrix)


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
