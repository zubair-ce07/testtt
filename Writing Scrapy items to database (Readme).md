Writing Scrapy items to database
=======

## Prerequisites:

1. Python 3.5 should be installed.
2. Scrapy should be installed.


## Writing items to MongoDB:

Steps:

1. Install PyMongo using this [link](https://docs.mongodb.com/getting-started/python/client/).
2. Use Scrapy’s [item pipeline](https://doc.scrapy.org/en/latest/topics/item-pipeline.html#write-items-to-mongodb) to write data to MongoDB.
3. In application, to import MongoDB use: **import pymongo**.

In MongoDB, use MongoClient (client for a MongoDB instance) to create a connection.
I.e. client = MongoClient(). If you do not specify any arguments to MongoClient, then MongoClient defaults to the MongoDB instance that runs on the localhost interface on port 27017.

To assign a database, following code is used:
db = client['myfirstdatabase'].
MongoDB creates new databases implicitly (if not exist) upon their first use.

To assign a collection (it holds groups of related [documents](https://docs.mongodb.com/manual/reference/glossary/#term-document)), following code is used:
coll = db['myfirstcollection'].
Document is a record in a MongoDB collection and the basic unit of data in MongoDB. Documents stored in the database are in a type-rich format known as [BSON](https://docs.mongodb.com/manual/reference/glossary/#term-bson)

Following MongoDB’s methods examples are given in the example project:

**insert_one, insert_many, find_one, find, update_one, update_many, delete_one, dete_many, drop**





## Writing items to PostgreSQL:

Steps:

1. Install and setup PostGreSQL server locally and pgAdmin III (GUI for PostgreSQL) using this [link](https://help.ubuntu.com/community/PostgreSQL).
2. Install Psycopg2 (it is a PostgreSQL adapter for the Python programming language) using this [link](http://www.brocade.com/content/html/en/software-installation-guide/SDN-Controller-2.1.0-Software-Installation/GUID-FDA442F0-70D9-41D2-926F-D5021DE9F159.html).
3. Use Scrapy’s item pipeline to write data to PostgreSQL.
4. In application, to import psycopg use: **import psycopg2**.

To create connection with postgres following connect method is used:

conn = psycopg2.connect(dbname='postgres' user='postgres' host='localhost' password='password' port='5432')

Where ‘dbname’ is the database name which user had provided while installing postgres, ‘user’ and ‘password’ are the parameters defining the username and password of your database which user had set while creating database.
Default port for postgres is 5432. In connect method in the example given, make sure to update the dbname, user, and password parameters with the dbname, user, and password you had set while following the [link](https://help.ubuntu.com/community/PostgreSQL).
It is recommended to create postgres connection in pipeline class built-in method **open_spider** and close the connection in method **close_spider**.

Following Postgres examples are given in the example project:

**CREATE TABLE,  INSERT record(s), UPDATE record(s) DELETE record(s), and
SELECT record(s)**

----------------------------------------------------------------------------------------------------------------------------

To run sample project, open terminal window and go to project directory and run the following command in:
**scrapy crawl orsay_itemloader -o items.json**

What this sample project does is that spider **“orsay_itemloader”** crawl over all the products links and every link is scraped for product details. Once a product is scraped, it will go through pipelines (MongoDB pipeline and PostgreSQL pipeline)
defined in project in pipelines.py file and will write data to database