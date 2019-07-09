const url = require('url');
const http = require('http');
const fs = require('fs');

const app = http.createServer((request, response) => {
    let listFiles = '0';
    let closed = 0;
    if(request.method === 'POST') {
        console.log('POST request')
        let body = '';
        request.on('data', chunk => {
            body += chunk.toString();
        });
        request.on('end', () => {
            listFiles = body.split('=')[1]
            if(listFiles == '1') {
                let files = fs.readdirSync('files');
                response.write(files.toString());
                response.end();
                closed = 1
            }
        });
    }

    parsed = url.parse(request.url);
    let pathName = parsed.pathname
    
    if(parsed.query && parsed.query.split('=')[1] == '1')
        listFiles = '1'

    if (pathName == '/' && parsed.query != null) {
        if(listFiles == '1' && closed == 0) {
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
             } else if (!closed){
               response.write(data);
               response.end( );
             }
        })
    }
});

app.listen(8080);