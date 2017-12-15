from elements.element import Element


class Attribute(Element):
    def __init__(self):
        Element.__init__(self)
        self.direct_child = True
        self.attribute_name = None

    def xpath(self):
        return self.create_xpath(f'@{self.attribute_name}');

    def item_name(self):
        return self.name_string("attr")
