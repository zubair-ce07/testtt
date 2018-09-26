def get(response, path):
    return response.css(path).extract()


def get_first(response, path):
    return response.css(path).extract_first()