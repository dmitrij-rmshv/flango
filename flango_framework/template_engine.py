# Это как бы templator.py
from jinja2 import Template


def linkage(pattern_name, **kwargs):

    with open(pattern_name, encoding='utf-8') as pt:
        template = Template(pt.read())
    return template.render(**kwargs)
