from elements.element import Element


class Span(Element):
    def xpath(self):
        return self.create_xpath("span")

    def item_name(self):
        return self.name_string("span")
