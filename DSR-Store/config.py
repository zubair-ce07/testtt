from flask import Flask
from flask_mysqldb import MySQLdb
app = Flask(__name__)
app.secret_key = 'many random bytes'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'passroot'
app.config['MYSQL_DB'] = 'crudapplication'

database = MySQLdb.connect("localhost","root","passroot","crudapplication" )