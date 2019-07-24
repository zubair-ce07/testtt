var express = require('express');

var app = express();
let listenPort = 8080

app.get('/', (req, res) => {
    console.log('Client connected');
    res.send('Hello, World!');
})

app.listen(listenPort, () => {
    console.log("App now listening on port " + listenPort);
})
