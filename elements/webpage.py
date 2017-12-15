from elements.hyperlink import HyperLink


class WebPage(HyperLink):
    def __init__(self):
        HyperLink.__init__(self)
        self.url = ''

    def item_name(self):
        return self.name_string("web-page")

    def url_string(self, xpath_result):
        return self.url + xpath_result
