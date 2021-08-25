from flango_framework.template_engine import linkage


class Index:
    def __call__(self, request):
        return '200 OK', linkage('index.html', data=request.get('data', None))


class About:
    def __call__(self, request):
        return '200 OK', linkage('about.html')


class Blog:
    def __call__(self, request):
        return '200 OK', linkage('blog.html')


class Contacts:
    def __call__(self, request):
        return '200 OK', linkage('contacts.html', phone_1=request.get('phone_1', None), phone_2=request.get('phone_2', None))
