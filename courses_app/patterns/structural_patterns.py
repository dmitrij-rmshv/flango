from time import time


class FlaskRoute:
    def __init__(self, routes, url):
        self.routes = routes
        self.url = url

    def __call__(self, cls):
        self.routes[self.url] = cls()


class Debug:

    def __init__(self, name):
        self.wrapped_func = name

    def __call__(self, cls):
        def timeit(method):
            def timed(*args, **kwargs):
                begin_time = time()

                result = method(*args, **kwargs)

                end_time = time()
                delta_time = end_time - begin_time
                print(
                    f'debug --> {self.wrapped_func} исполнен за {delta_time:2.2f} ms')
                return result

            return timed

        return timeit(cls)
