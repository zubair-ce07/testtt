const credentials = require("./credentials.js");

const MongoClient = require('mongodb').MongoClient;
const uri = `mongodb+srv://${credentials.username}:${credentials.password}@cluster0-ttgom.mongodb.net/test?retryWrites=true&w=majority`;
const client = new MongoClient(uri, { useNewUrlParser: true });

module.exports = client;
