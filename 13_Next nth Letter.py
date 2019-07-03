# coding: utf-8

# Write a procedure, shift_n_letters which takes as its input a lowercase
# letter, a-z, and an integer n, and returns the letter n steps in the
# alphabet after it. Note that 'a' follows 'z', and that n can be positive,
# negative or zero.


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


print(shift_n_letters('s', 1))
# >>> t
print(shift_n_letters('s', 2))
# >>> u
print(shift_n_letters('s', 10))
# >>> c
print(shift_n_letters('s', -10))
# >>> i
