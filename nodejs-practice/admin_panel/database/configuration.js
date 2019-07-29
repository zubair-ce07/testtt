const MongoClient = require('mongodb').MongoClient;
const uri = `mongodb+srv://${process.env.DB_USER}:${process.env.DB_PASS}@${process.env.DB_CLUSTER}`;
const client = new MongoClient(uri, { useNewUrlParser: true });

module.exports = client;
