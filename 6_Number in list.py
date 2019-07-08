# coding: utf-8

# Numbers in lists by SeanMc from forums
# define a procedure that takes in a string of numbers from 1-9 and
# outputs a list with the following parameters:
# Every number in the string should be inserted into the list.
# If the first number in the string is greater than or equal 
# to the proceeding number, the proceeding number should be inserted 
# into a sublist. Continue adding to the sublist until the proceeding number 
# is greater than the first number before the sublist. 
# Then add this bigger number to the normal list.

# Hint - "int()" turns a string's element into a number


def numbers_in_lists(str_rec):
    num_list = [int(str_rec[i]) for i in range(len(str_rec))]
    nums_list = [num_list[0]]
    i = 0
    j = 1
    while j < len(str_rec):
        if num_list[i] >= num_list[j]:
            sublist = [num_list[j]]
            k = j + 1
            while k < len(str_rec) and num_list[k] <= num_list[j]:
                sublist.append(num_list[k])
                k += 1
            nums_list.append(sublist)
            j += k - j
        else:
            nums_list.append(num_list[j])
            i = j
            j += 1
    return nums_list


# testcases
string = '543987'
result = [5, [4, 3], 9, [8, 7]]
print(numbers_in_lists(string))
print(repr(string), numbers_in_lists(string) == result)
string = '987654321'
result = [9, [8, 7, 6, 5, 4, 3, 2, 1]]
print(numbers_in_lists(string))
print(repr(string), numbers_in_lists(string) == result)
string = '455532123266'
result = [4, 5, [5, 5, 3, 2, 1, 2, 3, 2], 6, [6]]
print(numbers_in_lists(string))
print(repr(string), numbers_in_lists(string) == result)
string = '123456789'
result = [1, 2, 3, 4, 5, 6, 7, 8, 9]
print(numbers_in_lists(string))
print(repr(string), numbers_in_lists(string) == result)
