from wsgiref.simple_server import make_server

from simba_framework.main import Framework
from urls import *


application = Framework(routes, fronts)

addr = ''
port = 8080

with make_server(addr, port, application) as httpd:
    print(f'Server is runing on port {port}')
    httpd.serve_forever()
