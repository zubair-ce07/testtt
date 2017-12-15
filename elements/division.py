from elements.element import Element


class Division(Element):
    def xpath(self):
        return self.create_xpath("div");

    def item_name(self):
        return self.name_string("div")
