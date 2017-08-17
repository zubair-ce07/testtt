import flask
from flask import Flask
from flask import g
from flask import request

import sqlite3

app = Flask(__name__)

DATABASE = 'lemon_db.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/')
def index():
    return "It's working"


@app.route('/custom/<column_names>')
def custom_column_result(column_names):
    cur = get_db()
    query = ("select {} from lemon".format(column_names))
    readings = cur.execute(query)
    return flask.jsonify(readings.fetchall())


@app.route('/all')
def get_all_products():
    cur = get_db()
    return flask.jsonify(cur.execute('select * from lemon').fetchall())


@app.route('/products')
def get_range_of_products():
    cur = get_db()
    start = int(request.args.get('start'))
    end = int(request.args.get('end'))
    limit = (end - start) + 1
    query = 'select * from lemon limit {} offset {}'.format(limit, start)
    return flask.jsonify(cur.execute(query).fetchall())
