

class FileGlobals(object):
    """
    File related global constants
    """

    __global_constants = {
        'FILE_PREFIX': 'Murree_weather',
        'FILE_EXTENTION': 'txt'
    }

    @staticmethod
    def get(item):
        return FileGlobals.__global_constants.get(item)


class ArgsParserOptions(object):
    """
    File related global constants
    """

    __args_parser_options = [
        'year', 'year_with_month', 'month_bar_chart'
    ]

    @staticmethod
    def get_options():
        for constant in ArgsParserOptions.__args_parser_options:
            yield constant


class MonthsMapper(object):
    """
    Months mapper used to return numeric months to str prefix
    """
    __months_map = {
        1: 'Jan',
        2: 'Feb',
        3: 'Mar',
        4: 'Apr',
        5: 'May',
        6: 'Jun',
        7: 'Jul',
        8: 'Aug',
        9: 'Sep',
        10: 'Oct',
        11: 'Nov',
        12: 'Dec'
    }


    @staticmethod
    def get(item):
        return MonthsMapper.__months_map.get(item)


class Helper(object):

    __helper_dict = {
        'neg-infinity': -99999,
        'pos-infinity': 99999
    }

    @staticmethod
    def get(item):
        return Helper.__helper_dict.get(item)
