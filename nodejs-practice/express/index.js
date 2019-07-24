const express = require('express');
const wiki = require('./wiki.js');

const MongoClient = require('mongodb').MongoClient;
const uri = "mongodb+srv://admin:admin@cluster0-ttgom.mongodb.net/test?retryWrites=true&w=majority";
const client = new MongoClient(uri, { useNewUrlParser: true });

console.log("Connecting to DB...");

client.connect(err => {
    console.log("Successfully Connected to DB...");
    const collection = client.db("sample_weatherdata").collection("data");
    const record = collection.find({dataSource: "4"})
    record.forEach((e)=> {
        console.log(e)
    })
    client.close();
});

var app = express();
let listenPort = 8080;

// Middleware function
var onUserConnection = function (req, res, next) {
    console.log("User connected from port: " + 
                req.connection.remotePort + 
                " for path " + 
                req.originalUrl);
    next();
}

app.use(onUserConnection);

app.use('/wiki', wiki);

app.use('/public', express.static('public'));

app.get('/', (req, res) => {
    res.sendFile('index.html', {root: __dirname });
})

app.listen(listenPort, () => {
    console.log("App now listening on port " + listenPort);
})
