from rest_framework import renderers
from collections import OrderedDict


class JSONRenderer(renderers.JSONRenderer):
    def render(self, data, *args, **kwargs):
        if data:
            print(data[0])
            new_dict = OrderedDict()
            for key, value in data[0].items():
                print(key, value)
                new_dict[underscore_to_camelcase(key)] = value
        return super(JSONRenderer, self).render(new_dict, *args, **kwargs)


def underscore_to_camelcase(variable_name):
    result = ''.join(word.capitalize() for word in variable_name.split('_'))
    return result[0].lower() + result[1:]
