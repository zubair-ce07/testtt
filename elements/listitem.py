from elements.element import Element


class ListItem(Element):
    def xpath(self):
        return self.create_xpath("li")

    def item_name(self):
        return self.name_string("li")
