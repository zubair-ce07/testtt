from __future__ import print_function
from http.server import HTTPServer

from Server import Server


def run(server_class=HTTPServer, handler_class=Server, port=8000):
    try:
        server_address = ('', port)
        httpd = server_class(server_address, handler_class)
    except:
        port = 8123
        server_address = ('', port)
        httpd = server_class(server_address, handler_class)

    print('Listening at port: ' + str(port))
    httpd.serve_forever()

run()
