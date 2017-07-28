from flask import Flask
from flask import g
import csv
import sqlite3

DATABASE = '/home/hamza/test.db'
app = Flask(__name__)
app.config.from_object(__name__)


def connect_to_database():
    return sqlite3.connect(app.config['DATABASE'])


def get_db():
    db = getattr(g, 'db', None)
    if db is None:
        db = g.db = connect_to_database()
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


def execute_query(query, args=()):
    cur = get_db().execute(query, args)
    rows = cur.fetchall()
    cur.close()
    return rows


@app.route('/')
def startpage():
    return 'Go to http://127.0.0.1:5000/getproducts/start=?/limit=? to query database'


@app.route("/viewdb")
def viewdb():
    rows = execute_query("""SELECT * FROM Products""")
    return '<br>'.join(str(row) for row in rows)



@app.route("/getproducts/",defaults={'start':'0','limit':'2'})
@app.route("/getproducts/start=<start>/limit=<limit>")
def selectfromtop(start,limit):
    rows = execute_query("""SELECT * FROM Products LIMIT {} OFFSET {}""".format(limit,start))
    return '<br>'.join(str(row) for row in rows)


if __name__ == '__main__':
    app.run(debug=True)
