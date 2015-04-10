
def get_text_from_node(node):
        text_array = node.extract()
        if text_array:
            return normalize(text_array[0])
        else:
            return ''

def normalize(data):
    if type(data) is str or type(data) is unicode:
        return clean(data)
    elif type(data) is list:
        lines = [clean(x) for x in data]
        return [line for line in lines if line]
    else:
        return data

def clean(data):
    data = data.replace(u'&amp;', u'&').replace(u'&nbsp;', u' ')
    return data.replace(u'\u00e2\u20ac\u2122', u"'").replace(u'\u00e2\u20ac\u0153', u'"').replace(
        u'\u00e2\u20ac\ufffd', u'"').replace(u'\u2013', u"-").replace(u'\u00a0', u' ') \
        .replace(u'\u2012', u"-").replace(u'\u2018', u"'").replace(u'\u2019', u"'").replace(u'\u201c', u'"') \
        .replace(u'\u201d', u'"').replace(u'\xd0', u'-').strip()
