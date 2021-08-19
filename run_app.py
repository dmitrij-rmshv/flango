from courses_app.links import router, mid_layers
from flango_framework.mainframe import Flango

application = Flango(router, mid_layers)
