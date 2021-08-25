# это как бы urls.py
from courses_app.views import Contacts, Index, About, Blog


def secret_token(request):
    request['data'] = 'er6in9h78imn6rr'


def other_layer(request):
    request['phone_1'] = '+7(981)123-45-23'
    request['phone_2'] = '+7(911)345-89-43'


mid_layers = [secret_token, other_layer]

router = {
    '/': Index(),
    '/about/': About(),
    '/blog/': Blog(),
    '/contacts/': Contacts(),
}
