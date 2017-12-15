from elements.element import Element


class HyperLink(Element):
    def xpath(self):
        return self.create_xpath("a")

    def item_name(self):
        return self.name_string("a")
