import sqlite3

from flask import Flask, g

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


@app.route("/viewdb")
def viewdb():
    rows = execute_query("""SELECT * FROM Products""")
    return '<br>'.join(str(row) for row in rows)
