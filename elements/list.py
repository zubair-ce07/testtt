from elements.element import Element


class List(Element):
    def xpath(self):
        return self.create_xpath("ul")

    def item_name(self):
        return self.name_string("ul")
