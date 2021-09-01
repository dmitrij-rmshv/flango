# Это как бы main.py
import quopri
from time import ctime
from flango_framework.request_handler import TheGetHandler, ThePostHandler


class PageMissing():

    def __call__(self, request):
        return '404 Not OK', '404 PAGE missing'


class Flango():

    def __init__(self, routes, mid_layers) -> None:
        self.routes = routes
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
            decoded_data = Flango.decode_value(data)
            print(f'Нам пришёл POST-запрос: {decoded_data}')
            if 'user_msg' in data:
                with open('user_messages.txt', 'a') as msg_log:
                    record = '; '.join(
                        [f'{key.title()}: {value}' for key, value in decoded_data.items()])
                    msg_log.write(ctime() + record + '\n')
        if method == 'GET':
            request_params = TheGetHandler().get_request_params(environ)
            request['request_params'] = request_params
            print(f'Нам пришли GET-параметры: {request_params}')

        for layer in self.mid_layers:
            layer(request)
        if way in self.routes:
            print("I'm worked")
            view = self.routes[way]
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


class DebugApp(Flango):

    def __init__(self, routes_obj, mid_layers_obj):
        self.parent_app = Flango(routes_obj, mid_layers_obj)
        super().__init__(routes_obj, mid_layers_obj)

    def __call__(self, env, start_response):
        print(f"DEBUG MODE, тип запроса: =={env['REQUEST_METHOD']}==")
        print(env)
        return self.parent_app(env, start_response)


class FakeApp(Flango):

    def __init__(self, routes_obj, mid_layers_obj):
        self.parent_app = Flango(routes_obj, mid_layers_obj)
        super().__init__(routes_obj, mid_layers_obj)

    def __call__(self, env, start_response):
        start_response('200 OK', [('Content-Type', 'text/html')])
        return [b'Hello from Fake']
