# from sqlalchemy import Column, String, Integer, DateTime
# from books_spider.database_files.db_con_obj import Base
#
#
# class AllData(Base):
#     __tablename__ = "books record"
#     id = Column(Integer, primary_key=True)
#     Book_Name = Column(String(1000))
#     Book_Price = Column(String(1000))
#     Book_Author = Column(String(1000))
#     Book__Img_Url = Column(String(1000))
#     Book_Category = Column(String(1000))
#     Book_Condition = Column(String(1000))
#     Book_Weight = Column(String(1000))
#     Book_Language = Column(DateTime)
#
#     def __init__(self, id=None, name=None, price=None, author=None, img_url=None, category=None,
#                  condition=None, weight=None, language=None):
#         self.id = id
#         self.Book_Name = name
#         self.Book_Price = price
#         self.Book_Author = author
#         self.Book__Img_Url = img_url
#         self.Book_Category = category
#         self.Book_Condition = condition
#         self.Book_Weight = weight
#         self.Book_Language = language
#
#     def __repr__(self):
#         return "<AllData: id='%d', Book_Name='%s', Book_Price='%s', Book_Author='%s'," \
#                " Book__Img_Url='%s', Book_Category='%s', Book_Condition='%s',Book_Weight='%s', " \
#                "Book_Language='%s'>" % (self.id, self.Book_Name, self.Book_Price, self.Book_Author,
#                                         self.Book__Img_Url, self.Book_Category, self.Book_Condition,
#                                         self.Book_Weight, self.Book_Language)
