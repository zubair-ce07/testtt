var express = require('express');
var wiki = require('./wiki.js')

var app = express();
let listenPort = 8080

// Using a Router to handle route-prefix
app.use('/wiki', wiki);

app.use('/public', express.static('public'));

app.get('/', (req, res) => {
    res.sendFile('index.html', {root: __dirname });
})

app.listen(listenPort, () => {
    console.log("App now listening on port " + listenPort);
})
