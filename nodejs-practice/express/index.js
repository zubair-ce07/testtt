var express = require('express');
var wiki = require('./wiki.js')

var app = express();
let listenPort = 8080;


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
