from wsgiref.simple_server import make_server
from courses_app.links import router, mid_layers
from flango_framework.mainframe import Flango

application = Flango(router, mid_layers)

with make_server('', 8080, application) as httpd:
    print("Запуск на порту 8080...")
    httpd.serve_forever()
