# # from django.db import models
# #
# # class SeparatedValuesField(models.TextField):
# #     __metaclass__ = models.SubfieldBase
# #
# #     def __init__(self, *args, **kwargs):
# #         self.token = kwargs.pop('token', ',')
# #         super(SeparatedValuesField, self).__init__(*args, **kwargs)
# #
# #     def to_python(self, value):
# #         if not value: return
# #         if isinstance(value, list):
# #             return value
# #         return value.split(self.token)
# #
# #     def get_db_prep_value(self, value):
# #         if not value: return
# #         assert(isinstance(value, list) or isinstance(value, tuple))
# #         return self.token.join([unicode(s) for s in value])
# #
# #     def value_to_string(self, obj):
# #         value = self._get_val_from_obj(obj)
# #         return self.get_db_prep_value(value)
#
# from django.db import models
# import ast
#
#
# class ListField(models.TextField):
#     __metaclass__ = models.Field
#     description = "Stores a python list"
#
#     def __init__(self, *args, **kwargs):
#         super(ListField, self).__init__(*args, **kwargs)
#
#     def to_python(self, value):
#         if not value:
#             value = []
#
#         if isinstance(value, list):
#             return value
#
#         return ast.literal_eval(value)
#
#     def get_prep_value(self, value):
#         if value is None:
#             return value
#
#         return unicode(value)
#
#     def value_to_string(self, obj):
#         value = self._get_val_from_obj(obj)
#         return self.get_db_prep_value(value)
#
#
# class ListModel(models.Model):
#     test_list = ListField()

from django.db import models
import re

from django.core.exceptions import ValidationError
from django.db import models
from product.hand import Hand


def parse_hand(hand_string):
    """Takes a string of cards and splits into a full hand."""
    p1 = re.compile('.{26}')
    p2 = re.compile('..')
    args = [p2.findall(x) for x in p1.findall(hand_string)]
    if len(args) != 4:
        raise ValidationError("Invalid input for a Hand instance")
    return Hand(*args)


class HandField(models.Field):
    description = "A hand of cards (bridge style)"

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 104
        super(HandField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(HandField, self).deconstruct()
        del kwargs['max_length']
        return name, path, args, kwargs

    def from_db_value(self, value, expression, connection, context):
        if value is None:
            return value
        return parse_hand(value)

    def to_python(self, value):
        if isinstance(value, Hand):
            return value

        if value is None:
            if __name__ == '__main__':
                return value

        return parse_hand(value)

    def get_prep_value(self, value):
        return ''.join([''.join(l) for l in (value.north, value.east, value.south, value.west)])
