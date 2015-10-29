# -*- coding: utf-8 -*-


class DemoUTF(object):

    def __init__(self, str_to_convert):
        self.str_to_convert = str_to_convert

    def show_in_utf8(self):

        print '##########################'
        print '#          UTF-8         #'
        print '##########################'

        print "Same string in Binary"
        print map(lambda x: "{0:08b}".format(ord(x)), self.str_to_convert)

        print "Same string code points in decimal"
        for c in self.str_to_convert: print ord(c)

        print "Same string in UTF-8"

        u = self.str_to_convert.encode('utf-8')
        print 'Separated Bytes'
        print map(lambda x: "{0:08b}".format(ord(x)), u)
        print 'All Bytes Combined'
        print '{:b}'.format(int(self.str_to_convert.encode('utf-8').encode('hex'), 16))

    def show_in_utf16(self):

        # First show in binary

        print '##########################'
        print '#          UTF-16        #'
        print '##########################'

        print "Same String in Binary"
        print map(lambda x: "{0:08b}".format(ord(x)), self.str_to_convert)

        print "Same string code points in decimal"
        for c in self.str_to_convert: print ord(c)

        print "Same string in UTF-16"
        u = self.str_to_convert.encode('utf-16')
        print 'Separated Bytes'
        print map(lambda x: "{0:08b}".format(ord(x)), u)
        print 'All Bytes Combined'
        print '{:b}'.format(int(self.str_to_convert.encode('utf-16').encode('hex'), 16))

    def show_in_utf32(self):
        # First show in binary

        print '##########################'
        print '#          UTF-32        #'
        print '##########################'

        print "Same string in Binary"
        print map(lambda x: "{0:08b}".format(ord(x)), self.str_to_convert)

        print "Same string code points in decimal"
        for c in self.str_to_convert: print ord(c)

        print "Same string in UTF-32"
        u = self.str_to_convert.encode('utf-32')
        print 'Separated Bytes'
        print map(lambda x: "{0:08b}".format(ord(x)), u)
        print 'All Bytes Combined'
        print '{:b}'.format(int(self.str_to_convert.encode('utf-32').encode('hex'), 16))


def main():

    print '##########################'
    print '#         Unicode        #'
    print '##########################'
    print "It is a set of characters used around the world, In Unicode a letter does not map to some bits. It maps to a " \
          "code point"
    print "What is code point ?"
    print "A code point is an integer value, usually denoted in base 16. In the standard, a code point is written using" \
          " the notation U+12ca"
    print 'Why we use UTF-8,16,32?'
    print 'Because we want to use characters that are not available in ASCII and for internationalization.'

    print '##########################'
    print '#          UTF-8         #'
    print '##########################'
    print "UTF-8 is a character encoding capable of encoding all possible characters (called code points) in Unicode"
    print "Its code unit is 8-bits"
    print 'EXAMPLE: 00100100 for "$" (one 8-bits);11000010 10100010 for "¢" (two 8-bits);11100010 10000010 10101100 for' \
          ' "€" (three 8-bits)'
    print 'UTF-8 is the dominant character encoding for the World Wide Web,'
    print 'UTF-8 and ASCII are same for Latin letters'
    print 'UTF-8 encoding has few rules'
    print '1: If code point value of character is < 128 then it is represented in one byte'
    print '2: If code point value of character is b/w 128 and 2047 then character is represented in 2 bytes and  if a ' \
          'byte starts with 110 then it means its a 2 byte sequence.'
    print '3: If code point value is >2047 then they are represented by three- or four-byte sequences'

    print '##########################'
    print '#          UTF-16        #'
    print '##########################'
    print 'UTF-16 (16-bit Unicode Transformation Format) is a character encoding capable of encoding 1,112,064 possible' \
          ' characters in Unicode. The encoding is variable-length, as code points are encoded with one or two 16-bit ' \
          'code units'
    print 'EXAMPLE: 00000000 00100100 for "$" (one 16-bits);11011000 01010010 11011111 01100010 for "𤭢" (two 16-bits)'

    print '##########################'
    print '#          UTF-32        #'
    print '##########################'
    print 'It is a protocol to encode Unicode code points that uses exactly 32 bits per Unicode code point.'
    print 'This makes UTF-32 a fixed-length encoding, in contrast to all other Unicode transformation formats' \
          ' which are variable-length encodings.'
    print 'In UTF-32 every character is represented in 4 bytes (32 bits)'

    print "As an example lets say we have a string '€' "
    string1 = u'€'
    du = DemoUTF(string1)
    du.show_in_utf8()
    du.show_in_utf16()
    du.show_in_utf32()

    print 'You can enter any string and I can convert it for you in all 3 encodings'
    while True:
        string1 = raw_input('Enter a string to convert: ').decode('utf-8')
        du = DemoUTF(string1)
        du.show_in_utf8()
        du.show_in_utf16()
        du.show_in_utf32()

    return

#: python main.py
if __name__ == "__main__":
    main()
