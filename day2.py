#                   First week Tuesday
#                      Topic Covered
#   Classes
#   Class Function
#   Using of class attrbute
#   Public behavior
#   Inheritance
#   calling function of parent through inheritance OOP concepts


class Book:

    def __init__(self, name, book_pages, author):
        self.name = name
        self.book_pages = book_pages
        self.author = author

    def print_book(self):
        print("Book Name: {0}\nPages: {1}\nAuthor: {2}\n ".format(self.name, self.book_pages, self.author))


class MathBook(Book):

    def print_book(self):
        print(self.author + " This function is calling through Inheritance")


print("Enter Book Name : ")
book_name = input()
print("Enter Book Pages : ")
pages = input()
print("Enter Book's Author Name : ")
author_name = input()

b1 = Book(book_name, pages, author_name)
b1.print_book()


b1.pages = 100
b1.print_book()


math_book = MathBook(b1.name, b1.pages, b1.author)
math_book.print_book()
