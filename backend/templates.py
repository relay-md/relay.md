# -*- coding: utf-8 -*-
import pypugjs
from fastapi.templating import Jinja2Templates
from markdown import markdown as markdown2html

from .config import get_config

templates = Jinja2Templates(
    directory=r"backend/templates",
)

templates.env.globals["config"] = get_config()

# Jade templating is nice for faster prototyping
templates.env.add_extension("pypugjs.ext.jinja.PyPugJSExtension")


@pypugjs.register_filter("markdown")
def markdown(text, ast):
    return markdown2html(text)
