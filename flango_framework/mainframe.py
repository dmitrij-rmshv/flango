# Это как бы main.py
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
