class Helper():

    @staticmethod
    def get_text_from_node(node):
        text_array = node.extract()
        if text_array:
            return Helper.normalize(''.join(text_array))
        else:
            return ''

    @staticmethod
    def normalize(data):
        if type(data) is str or type(data) is unicode:
            return Helper.clean(data)
        elif type(data) is list:
            lines = [Helper.clean(x) for x in data]
            return [line for line in lines if line]
        else:
            return data

    @staticmethod
    def clean(data):
        return data.replace("\n", "") \
            .replace("\r", "") \
            .replace("\t", "").strip()
