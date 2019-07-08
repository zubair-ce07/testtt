const url = require('url');
const http = require('http');
const fs = require('fs');

const app = http.createServer((request, response) => {
    parsed = url.parse(request.url);
    let pathName = parsed.pathname
    console.log(pathName)
    if (pathName == '/' && parsed.query != null) {
        if(parsed.query.split('=')[1] == '1') {
            let files = fs.readdirSync('files');
            response.write(files.toString());
            response.end();
        }
    } else {
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
    }
});

app.listen(8080);