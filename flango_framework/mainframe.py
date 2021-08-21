# Это как бы main.py
import quopri
from flango_framework.request_handler import TheGetHandler, ThePostHandler


class PageMissing():

    def __call__(self, request):
        return '404', '404 PAGE missing'


class Flango():

    def __init__(self, router, mid_layers) -> None:
        self.router = router
        self.mid_layers = mid_layers

    def __call__(self, environ, start_response):
        way = environ['PATH_INFO']
        way += '/' if way[-1] != '/' else ''
        request = {}

        method = environ['REQUEST_METHOD']
        request['method'] = method

        if method == 'POST':
            data = ThePostHandler().get_request_params(environ)
            request['data'] = data
            print(f'Нам пришёл POST-запрос: {Flango.decode_value(data)}')
        if method == 'GET':
            request_params = TheGetHandler().get_request_params(environ)
            request['request_params'] = request_params
            print(f'Нам пришли GET-параметры: {request_params}')

        for layer in self.mid_layers:
            layer(request)
        if way in self.router:
            print("I'm worked")
            view = self.router[way]
        else:
            view = PageMissing()
        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]

    @staticmethod
    def decode_value(data):
        new_data = {}
        for k, v in data.items():
            val = bytes(v.replace('%', '=').replace("+", " "), 'UTF-8')
            val_decode_str = quopri.decodestring(val).decode('UTF-8')
            new_data[k] = val_decode_str
        return new_data
