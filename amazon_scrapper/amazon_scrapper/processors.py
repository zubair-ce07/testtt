class StripString(object):
    def __call__(self, values):
        for value in values:
            string = value.strip(' \r\n')
            if string:
                return string
        return 'Not Found'


class StripRating:
    def __call__(self, values):
        for value in values:
            # splitting str '4.5 out of 5' to get rating
            string = value.split()
            if string:
                return string[0]
        return 'Not Found'
