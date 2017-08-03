
class Node:
    """Node is used to store an element of a list with its index and data"""

    def __init__(self, data=None, index=None, previous=None):

        self.data = data
        self.index = index
        self.next = None
        self.previous = previous

    def __str__(self):
        return '{data}'.format(data=self.data)


class CustomList:
    """A custom list store collection of Nodes/elements"""

    def __init__(self):
        self.length = 0
        self.header = Node()
        self.iterator = self.header
        self.tail = None

    def __str__(self):
        """
        :return: string representation of CustomList instance
        """
        if not self.length:
            return "[]"

        list_name = "["
        counter = 1
        for node in self:
            if counter == self.length:
                list_name += '{data}]'.format(data=node)
                break
            counter += 1
            list_name += '{data}, '.format(data=node)

        return list_name

    def __len__(self):
        """
        :return: Total length of the CustomList
        """
        return self.length

    def __getitem__(self, key):
        """
        :param key: index of the Node/Element to get
        :return: value of the Node at the given index
        """
        if isinstance(key, slice):
            split_list = CustomList()
            for index in range(key.start, key.stop):
                split_list.append(self.__getitem__(index))
            return split_list

        if key < 0:
            key += self.length
        current_node = self.header.next
        while current_node:
            if current_node.index == key:
                return current_node.data
            current_node = current_node.next

        raise IndexError('list index out of range')

    def __setitem__(self, key, value):
        """
        :param key: index of the Node/Element to set
        :param value: new value to set the the given position
        :return: returns Nothing else raise IndexError
        """
        current_node = self.header.next
        while current_node:
            if current_node.index == key:
                current_node.data = value
                return value
            current_node = current_node.next

        raise IndexError('list index out of range')

    def __iter__(self):
        """
        Make the Custom List iterable
        :return: the object itself, to call next function
        """
        self.iterator = self.header
        return self

    def __next__(self):
        """
        Iterate over the existing CustomList
        :return: Value of the Node
        """
        if self.iterator.next:
            obj = self.iterator.next
            self.iterator = self.iterator.next
            return obj.data
        else:
            raise StopIteration

    def __add__(self, obj):
        """
        Concatenate the two Objects and return a new Custom List
        :param obj: any iterable object
        """
        added_list = CustomList()
        added_list.extend(self)
        added_list.extend(obj)
        return added_list

    def __contains__(self, obj):
        """
        Check the membership of the Object in the existing CustomList
        :param obj: Any Python Object
        :return: True if Object is a member else False
        """
        current_node = self.header.next
        while current_node:
            if current_node.data == obj:
                return True
            current_node = current_node.next
        return False

    def __mul__(self, rep):
        """
        Repeat the existing CustomList given number of time and return a new CustomList
        :param rep: Integer: Number of times repeat the CustomList
        """
        repeted_list = CustomList()
        for i in range(rep):
            repeted_list.extend(self)
        return repeted_list

    def __eq__(self, other):
        """
        Check if the existing CustomList is equals to the other Object
        :param other: Any Object
        :return: True if equals else False
        """
        if type(self) != type(other):
            return False

        if self.length != len(other):
            return False

        for index in range(self.length):
            if self[index] != other[index]:
                return False
        return True

    def __ne__(self, other):
        """
        Check if the existing CustomList is not equal to the other Object
        :param other: Any Object
        :return: True if not equal else False
        """
        if type(self) != type(other):
            return False

        if self.length != len(other):
            return False

        for index in range(self.length):
            if self[index] != other[index]:
                return True
        return False

    def __lt__(self, other):
        """
        Check if the existing CustomList is less than the other CustomList
        :param other: CustomList object
        :return: True if CustomList is less than other CustomList else False
        """
        if type(self) != type(other):
            raise TypeError(f"'<' not supported between instances of {type(self)} and {type(other)}")

        for index in range(self.length):
            if self[index] == other[index]:
                continue
            return self[index] < other[index]

    def __gt__(self, other):
        """
        Check if the existing CustomList is greater than the other CustomList
        :param other: CustomList object
        :return: True if CustomList is greater than other CustomList else False
        """
        if type(self) != type(other):
            raise TypeError(f"'>' not supported between instances of {type(self)} and {type(other)}")

        for index in range(self.length):
            if self[index] == other[index]:
                continue
            return self[index] > other[index]

    def __ge__(self, other):
        """
        Check if the existing CustomList is equal or greater than the other CustomList
        :param other: CustomList object
        :return: True if CustomList is greater or equal to the other CustomList else False
        """
        if self == other:
            return True

        return self.__gt__(other)

    def __le__(self, other):
        """
        Check if the existing CustomList is less than or equal to the other CustomList
        :param other: CustomList object
        :return: True if CustomList is less or equal to the other CustomList else False
        """
        if self == other:
            return True

        return self.__lt__(other)

    def append(self, obj):
        """
        Appends a passed obj into the existing CustomList.
        :param obj: This is the object to be appended in the CustomList.
        :return: This method does not return any value but updates existing CustomList.
        """
        current_node = self.header
        while current_node.next:
            current_node = current_node.next

        current_node.next = Node(obj, self.length, current_node)
        self.length += 1

    def count(self, obj):
        """
        Returns count of how many times obj occurs in list.
        :param obj: This is the object to be counted in the list.
        :return: Count of how many times obj occurs in list.
        """
        count = 0
        current_node = self.header.next
        while current_node:
            if current_node.data == obj:
                count += 1
            current_node = current_node.next

        return count

    def extend(self, seq):
        """
        Appends the contents of seq to list.
        :param seq: An iterable sequence
        :return: Does not return any value but add the content to existing list.
        """
        for value in seq:
            self.append(value)

    def index(self, obj):
        """
        The method returns the lowest index in list that obj appears
        :param obj: This is the object to be find out.
        :return: Index of the found object otherwise raise an exception
        """
        current_node = self.header.next
        while current_node:
            if current_node.data == obj:
                return current_node.index
            current_node = current_node.next

        raise ValueError('{obj} is not in list'.format(obj=obj))

    def insert(self, index, obj):
        """
        This method inserts object obj into list at offset index.
        :param index: This is the Index where the object obj need to be inserted.
        :param obj: This is the Object to be inserted into the existing CustomList.
        :return: Does not return any value
        """
        current_node = self.header.next
        while current_node:
            if current_node.index == index:
                previous_node = current_node.previous
                new_node = Node(obj, index, previous_node)
                previous_node.next = new_node
                new_node.next = current_node
                current_node.previous = new_node
                self.length += 1
                while current_node:
                    current_node.index += 1
                    current_node = current_node.next
                return
            current_node = current_node.next

        current_node.next = Node(obj, self.length, current_node)
        self.length += 1

    def pop(self, index=-1):
        """
        This method removes and returns last object or obj at the given index.
        :param index: An optional parameter, index of the object to be removed from the list.
        :return: Returns the removed object from the list
        """
        if index < 0:
            index += self.length
        current_node = self.header.next
        while current_node:
            if current_node.index == index:
                previous_node = current_node.previous
                previous_node.next = current_node.next
                data = current_node.data
                del current_node
                self.length -= 1
                return data
            current_node = current_node.next
        raise IndexError('list index out of range')

    def remove(self, obj):
        """
        This method removes the given Object obj from the existing List
        :param obj: The object to be removed from the list.
        :return: Does not return any value
        """
        current_node = self.header.next
        while current_node:
            if current_node.data == obj:
                previous_node = current_node.previous
                previous_node.next = current_node.next
                self.length -= 1
                current_node = current_node.next
                while current_node:
                    current_node.index -= 1
                    current_node = current_node.next
                return
            current_node = current_node.next
        raise ValueError('{obj} is not in list'.format(obj=obj))

    def reverse(self):
        """
        Reverses objects of list in place
        :return: Does not return any value
        """
        current_node = self.header.next
        count = 0
        while count < self.length:
            current_node.index = self.length - current_node.index - 1
            temp = current_node.next
            current_node.next = current_node.previous
            current_node.previous = temp
            if count == 0:
                current_node.next = None
            elif count == (self.length - 1):
                current_node.previous = self.header
                self.header.next = current_node
            current_node = temp
            count += 1

    def sort(self):
        """Sorts objects of CustomList"""
        sorted_list = sorted(self, key=lambda x: str(x))
        for index in range(self.length):
            self[index] = sorted_list[index]

    def copy(self):
        """
        Deep copy of the existing CustomList
        :return: A new CustomList with the same content as the existing CustomList
        """
        new_list = CustomList()
        for val in self:
            new_list.append(val)
        return new_list

    def clear(self):
        """
        Empty the existing CustomList
        :return: does not return anything
        """
        self.length = 0
        self.header.next = None
