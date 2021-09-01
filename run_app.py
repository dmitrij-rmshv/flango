from wsgiref.simple_server import make_server
from courses_app.links import mid_layers
from courses_app.views import routes
from flango_framework.mainframe import Flango, DebugApp, FakeApp


class AppFactory:
    types = {'w': Flango, 'd': DebugApp, 'f': FakeApp}

    @classmethod
    def create(cls, app_kind):
        return cls.types[app_kind](routes, mid_layers)


app = input("Choose app mod('w'-working(default); 'd'-debug; 'f'-fake): ") or 'w'
application = AppFactory.create(app)

with make_server('', 8080, application) as httpd:
    print("Запуск на порту 8080...")
    httpd.serve_forever()
