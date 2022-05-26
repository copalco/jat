import wsgiref.simple_server

from main.web import create_app

with wsgiref.simple_server.make_server('', 8080, create_app()) as server:
    server.serve_forever()