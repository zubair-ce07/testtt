class InvalidNameInputError(Exception):

    def __init__(self, arg):
        self.strerror = arg
        self.args = {arg}
