from flask import Flask, json, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc

app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:2321@localhost:5433/books_db'
db = SQLAlchemy(app)


class BooksTable(db.Model):
    """Sqlalchemy books table model"""
    __tablename__ = "booksRecord"
    id = db.Column(db.Integer, primary_key=True)
    Book_Name = db.Column('Book_Name', db.String(150))
    Book_price = db.Column('Book_Price', db.String(10))
    Book_Author = db.Column('Book_Author', db.String(150))
    Image__Img_Url = db.Column('Image__Img_Url', db.String(150))
    Book_Category = db.Column('Book_Category', db.String(50))
    Book_Condition = db.Column('Book_Condition', db.String(20))
    Book_Weight = db.Column('Book_Weight', db.String(10))
    Book_Language = db.Column('Book_Language', db.String(20))

    def __init__(self, name=None, price=None, author=None, img_url=None, category=None,
                 condition=None, weight=None, language=None):
        self.Book_Name = name
        self.Book_Price = price
        self.Book_Author = author
        self.Book__Img_Url = img_url
        self.Book_Category = category
        self.Book_Condition = condition
        self.Book_Weight = weight
        self.Book_Language = language


@app.route('/categories', methods=['GET'])
def get_categories():
    book_category = []
    category = []
    cate = []
    books_counter = 0
    for obj in BooksTable.query.distinct(BooksTable.Book_Category):
        cate.append(obj.Book_Category)
        b = BooksTable.query.filter_by(Book_Category=cate[-1])
        for obj1 in b:
            print(obj1.Book_Category)
            books_counter += 1
        category.append(books_counter)
        books_counter = 0
        book_category.append({
            'Name ': obj.Book_Category,
            'Total Books (counts)': category[-1]
        })

    return json.dumps({'Categories': book_category})


@app.route('/all_price/ascending', methods=['GET'])
def get_data_ascending():
    book_records = []
    book = BooksTable.query.order_by(BooksTable.Book_price).all()
    for obj in book:
        book_records.append({
            'id': obj.id,
            'Book Name': obj.Book_Name,
            'Book Price': obj.Book_price,
            'Book_Author': obj.Book_Author,
            'Book Img Src': obj.Image__Img_Url,
            'Book Category': obj.Book_Category,
            'Book Condition': obj.Book_Condition,
            'Book Weight': obj.Book_Weight,
            'Book Language': obj.Book_Language,
        })

    return json.dumps({'Books': book_records})


@app.route('/all/findbyID/<int:abc>', methods=['GET'])
def find_by_id(abc):
    abc -= 1
    book_records = []
    book = BooksTable.query.all()
    # for obj in book:
    #     if obj.id == Id:
    book_records.append({
        'id': book[abc].id,
        'Book Name': book[abc].Book_Name,
        'Book Price': book[abc].Book_price,
        'Book_Author': book[abc].Book_Author,
        'Book Img Src': book[abc].Image__Img_Url,
        'Book Category': book[abc].Book_Category,
        'Book Condition': book[abc].Book_Condition,
        'Book Weight': book[abc].Book_Weight,
        'Book Language': book[abc].Book_Language,
    })
    return json.dumps({'Books': book_records})


@app.route('/all/deleteByID/<int:abcd>', methods=['DELETE'])
def delete_by_id(abcd):
    abc = BooksTable.query.all()
    for data in abc:
        if data.id == abcd:
            db.session.delete(data)
            db.session.commit()
            return "value delete"
    return "not found"


@app.route('/all_price/descending', methods=['GET'])
def get_data_descending():
    book_records = []
    book = BooksTable.query.order_by(desc(BooksTable.Book_price)).all()
    for obj in book:
        book_records.append({
            'id': obj.id,
            'Book Name': obj.Book_Name,
            'Book Price': obj.Book_price,
            'Book_Author': obj.Book_Author,
            'Book Img Src': obj.Image__Img_Url,
            'Book Category': obj.Book_Category,
            'Book Condition': obj.Book_Condition,
            'Book Weight': obj.Book_Weight,
            'Book Language': obj.Book_Language,
        })

    return json.dumps({'Books': book_records})


@app.route('/all_data')
def get_data():

    book_records = []
    book = BooksTable.query.all()
    for obj in book:
        book_records.append({
            'id': obj.id,
            'Book Name': obj.Book_Name,
            'Book Price': obj.Book_price,
            'Book_Author': obj.Book_Author,
            'Book Img Src': obj.Image__Img_Url,
            'Book Category': obj.Book_Category,
            'Book Condition': obj.Book_Condition,
            'Book Weight': obj.Book_Weight,
            'Book Language': obj.Book_Language,
        })

    return json.dumps({'Books': book_records})

if __name__ == '__main__':
    app.run(debug=True)

