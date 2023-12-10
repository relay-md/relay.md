# -*- coding: utf-8 -*-
import pypugjs
from fastapi.templating import Jinja2Templates
from markdown import markdown as markdown2html

templates = Jinja2Templates(
    directory=r"backend/templates",
)

# Jade templating is nice for faster prototyping
templates.env.add_extension("pypugjs.ext.jinja.PyPugJSExtension")


@pypugjs.register_filter("markdown")
def markdown(text, ast):
    return markdown2html(text)
