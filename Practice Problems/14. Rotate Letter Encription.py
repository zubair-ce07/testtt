
# Write a procedure, rotate which takes as its input a string of lower case
# letters, a-z, and spaces, and an integer n, and returns the string constructed
# by shifting each of the letters n steps, and leaving the spaces unchanged.
# Note that 'a' follows 'z'. You can use an additional procedure if you
# choose to as long as rotate returns the correct string.
# Note that n can be positive, negative or zero.

#COments


def shift_n_letters(letter, n):
    int_val = ord(letter)
    int_val = int_val + n
    if int_val > 122:
        int_val -= 26
    elif int_val < 97:
        int_val += 26
    return chr(int_val)


def rotate(string, number):
    temp = None
    for character in string:
        if character == " ":
            temp += " "
            continue
        temp += shift_n_letters(character, number)
    return temp


print rotate ('sarah', 13)
#>>> 'fnenu'
print rotate('fnenu',13)
#>>> 'sarah'
print rotate('dave',5)
#>>>'ifaj'
print rotate('ifaj',-5)
#>>>'dave'
print rotate(("zw pfli tfuv nfibj tfiivtkcp pfl jyflcu "
                "sv rscv kf ivru kyzj"),-17)
