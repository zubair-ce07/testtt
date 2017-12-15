from elements.element import Element


class Text(Element):
    def __init__(self):
        Element.__init__(self)
        self.direct_child = True

    def xpath(self):
        return self.create_xpath("text()")

    def item_name(self):
        return self.name_string("text")
