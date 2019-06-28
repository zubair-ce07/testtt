class ColorPrint:

    @staticmethod
    def red(input_str):
        print('\33[31;0m'+input_str+'\33[0m')

    @staticmethod
    def red_raw(input_str):
        return '\33[31;0m'+input_str+'\33[0m'

    @staticmethod
    def blue(input_str):
        print('\33[34;0m'+input_str+'\33[0m')

    @staticmethod
    def blue_raw(input_str):
        return '\33[34;0m' + input_str + '\33[0m'
