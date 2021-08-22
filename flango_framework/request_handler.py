class TheGetHandler:

    @staticmethod
    def parse_input_data(data: str) -> dict:
        return {item.split('=')[0]: item.split('=')[1] for item in data.split("&") if data}

    @staticmethod
    def get_request_params(environ):
        return TheGetHandler.parse_input_data(environ['QUERY_STRING'])


class ThePostHandler:

    @staticmethod
    def parse_input_data(data: str) -> dict:
        return {item.split('=')[0]: item.split('=')[1] for item in data.split("&") if data}

    @staticmethod
    def get_wsgi_input_data(env) -> bytes:
        content_length = int(env.get('CONTENT_LENGTH', 0))
        # считываем данные, если они есть
        data = env['wsgi.input'].read(
            content_length) if content_length > 0 else b''
        return data

    def parse_wsgi_input_data(self, data: bytes) -> dict:
        result = {}
        if data:
            # декодируем данные
            data_str = data.decode(encoding='utf-8')
            # собираем их в словарь
            result = self.parse_input_data(data_str)
        return result

    def get_request_params(self, environ):
        return self.parse_wsgi_input_data(self.get_wsgi_input_data(environ))
