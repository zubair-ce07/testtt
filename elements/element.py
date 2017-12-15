from abc import ABC
from abc import abstractmethod


class Element(ABC):
    def __init__(self):
        ABC.__init__(self)
        self.multiple = False
        self.root_path = None
        self.name = None
        self.css_class = None
        self.only_class = None
        self.id = None
        self.react_id = None
        self.data = None
        self.parent_element = None
        self.data_elements = []
        self.leaf_elements = []
        self.crawlable_links = []
        self.direct_child = False

    @abstractmethod
    def xpath(self):
        return

    @abstractmethod
    def item_name(self):
        return

    def add_data_element(self, data):
        data.parent_element = self
        self.data_elements.append(data)

    def add_leaf_element(self, data):
        data.parent_element = self
        self.leaf_elements.append(data)

    def add_crawlable_link(self, link):
        link.parent_element = self
        self.crawlable_links.append(link)

    def create_xpath(self, item_name):

        if self.direct_child:
            path = f"./{item_name}"
        else:
            path = f".//{item_name}"

        if self.root_path is not None:
            path = path.replace(".", self.root_path)

        separator = "["
        end = ""
        # if self.parent_element is not None:
        #     path = f"{self.parent_element.xpath()}//{item_name}"
        if self.id is not None:
            path = path + separator + f"@id='{self.id}'"
            separator = "and "
            end = "]"
        if self.css_class is not None:
            path = path + separator + f"contains(@class, '{self.css_class}')"
            separator = "and "
            end = "]"
        if self.only_class is not None:
            path = path + separator + f"@class='{self.only_class}'"
            end = "]"
        path += end
        return path

    def name_string(self, item_name):
        id = ""
        if self.id is not None:
            id = "#" + self.id
        return item_name + id
