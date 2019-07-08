const url = require('url');
const http = require('http');
const fs = require('fs');

const app = http.createServer((request, response) => {
    pathName = url.parse(request.url).pathname;
    if (pathName == '/') {
        pathName = '/index.html'
    }

    fs.readFile(__dirname + pathName, function(err, data){
        if(err){
            fs.readFile(__dirname + '/404.html', function(err, data){
                response.write(data);
                response.end( );
            })
         } else {
           response.write(data);
           response.end( );
         }
    })
});

app.listen(8080);