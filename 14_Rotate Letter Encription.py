# coding: utf-8

# Write a procedure, rotate which takes as its input a string of lower case
# letters, a-z, and spaces, and an integer n, and returns the string
# constructed by shifting each of the letters n steps, and leaving the spaces
# unchanged.
# Note that 'a' follows 'z'. You can use an additional procedure if you
# choose to as long as rotate returns the correct string.
# Note that n can be positive, negative or zero.


def shift_n_letters(letter, n):
    alpha = ord(letter)
    if n > 0:
        count = 0
        while n is not 0:
            if chr(alpha + 1) > 'z':
                alpha = ord('a') + count
                count += 1
            else:
                alpha += 1
            n -= 1
    else:
        count = 0
        while n is not 0:
            if chr(alpha - 1) < 'a':
                alpha = ord('z') - count
                count += 1
            else:
                alpha -= 1
            n += 1
    return chr(alpha)


def rotate(string, number):
    new_str = ''
    for char in string:
        if char is not ' ':
            new_str += shift_n_letters(char, number)
        else:
            new_str += char
    return new_str


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
