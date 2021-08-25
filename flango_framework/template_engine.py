# Это как бы templator.py
from jinja2 import Template, FileSystemLoader
from jinja2.environment import Environment


def linkage(pattern_name, folder='courses_app/templates', **kwargs):

    env = Environment()
    env.loader = FileSystemLoader(folder)
    template = env.get_template(pattern_name)
    return template.render(**kwargs)
