"""
Define a procedure that takes in a string of numbers from 1-9 and outputs a list with the
following parameters:
 - Every number in the string should be inserted into the list.
 - If the first number in the string is greater than or equal to the proceeding number, the
   proceeding number should be inserted into a sublist. Continue adding to the sublist until
   the proceeding number is greater than the first number before the sublist.Then add this
   bigger number to the normal list.
"""


def numbers_in_lists(input_string):
    result_list, sub_list = [], []
    current_max = 0
    for s in input_string:
        number = int(s)
        if number > current_max:
            current_max = number
            if sub_list:
                result_list.append(sub_list)
                sub_list = []
            result_list.append(current_max)
        else:
            sub_list.append(number)
    if sub_list:  # if the sub list generated is to be inserted at the end
        result_list.append(sub_list)
    return result_list


# test cases
string = '5439876'
result = [5, [4, 3], 9, [8, 7, 6]]
print repr(string), numbers_in_lists(string) == result
string = '987654321'
result = [9, [8, 7, 6, 5, 4, 3, 2, 1]]
print repr(string), numbers_in_lists(string) == result
string = '455532123266'
result = [4, 5, [5, 5, 3, 2, 1, 2, 3, 2], 6, [6]]
print repr(string),   numbers_in_lists(string) == result
string = '123456789'
result = [1, 2, 3, 4, 5, 6, 7, 8, 9]
print repr(string), numbers_in_lists(string) == result
