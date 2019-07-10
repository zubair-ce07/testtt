# coding: utf-8

# Write a procedure, rotate which takes as its input a string of lower case
# letters, a-z, and spaces, and an integer n, and returns the string
# constructed by shifting each of the letters n steps, and leaving the spaces
# unchanged.
# Note that 'a' follows 'z'. You can use an additional procedure if you
# choose to as long as rotate returns the correct string.
# Note that n can be positive, negative or zero.


def shift_char(char, step):
    if char is ' ':
        return char
    else:
        return chr(ord('a') + (ord(char) - ord('a') + step) % 26)


def rotate(string, number):
    new = ''
    for char in string:
        new += shift_char(char, number)
    return new


print(rotate('sarah', 13))
# >>> 'fnenu'
print(rotate('fnenu', 13))
# >>> 'sarah'
print(rotate('dave', 5))
# >>>'ifaj'
print(rotate('ifaj', -5))
# >>>'dave'
print(rotate(("zw pfli tfuv nfibj tfiivtkcp pfl jyflcu "
              "sv rscv kf ivru kyzj"), -17))
# >>> ???
