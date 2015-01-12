#!/usr/bin/env python
# -*- coding: UTF-8 -*-
temp = u'\u1234'
utf8r = ''
utf16r = ''
utf32r = ''
print temp
#####################utf8#######################
utf8 = temp.encode("utf-8")
print '\n++++++++++\nutf8\n+++++++++\n'
print repr(utf8)
for a in utf8:
    utf8r = utf8r + ' ' + bin(ord(a))
print utf8r
####################utf-16#####################
utf16 = temp.encode("utf-16")
print '\n++++++++++\nutf16\n+++++++++\n'
print repr(utf16)

for a in utf16:
    utf16r = utf16r + ' ' + bin(ord(a))
print utf16r
##################utf-32#####################
utf32 = temp.encode("utf-32")
print '\n++++++++++\nutf32\n+++++++++\n'
print repr(utf32)
for a in utf32:
    utf32r = utf32r + ' ' + bin(ord(a))
print utf32r
