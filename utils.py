class Utils:
    @staticmethod
    def is_int(s):
        if s[0] in ["-", "+"]:
            return s[1:].isdigit()
        return s.isdigit()

    @staticmethod
    def is_float(s):
        if s[0] in ["-", "+"]:
            return s[1:].isdecimal()
        return s.isdecimal()
