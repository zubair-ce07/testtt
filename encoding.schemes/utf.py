#!/usr/bin/env python
# -*- coding: UTF-8 -*-
def utf8_encode(query_string):
    utf8binary = ''
    utf8 = query_string.encode("utf-8")
    for result in utf8:
        utf8binary = utf8binary + ' ' + bin(ord(result))
    return utf8, utf8binary


####################utf-16#####################
def utf16_encode(query_string):
    utf16binary = ''
    utf16 = query_string.encode("utf-16")
    for result in utf16:
        utf16binary = utf16binary + ' ' + bin(ord(result))
    return utf16, utf16binary


##################utf-32#####################
def utf32_encode(query_string):
    utf32binary = ''
    utf32 = query_string.encode("utf-32")
    for result in utf32:
        utf32binary = utf32binary + ' ' + bin(ord(result))
    return utf32, utf32binary


def main():
    special_char = u'\u1234'
    print '\n++++++++++\nutf8\n+++++++++\n'
    utf8, utf8binary = utf8_encode(special_char)
    print utf8
    print utf8binary
    print '\n++++++++++\nutf16\n+++++++++\n'
    utf16, utf16binary = utf16_encode(special_char)
    print utf16
    print utf16binary
    print '\n++++++++++\nutf32\n+++++++++\n'
    utf32, utf32binary = utf32_encode(special_char)
    print utf32
    print utf32binary

if __name__ == "__main__":
    main()