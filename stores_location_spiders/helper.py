
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
    return data.replace("\n", "")\
                .replace("\r", "")\
                .replace("\t", "").strip()
