# -*- coding: utf-8 -*-
from fastapi.templating import Jinja2Templates
from markdown import markdown as markdown2html

from . import __version__
from .config import get_config

templates = Jinja2Templates(
    directory=r"backend/templates",
)

templates.env.globals["config"] = get_config()
templates.env.globals["__version__"] = __version__
templates.env.filters["markdown"] = lambda text: markdown2html(text)

# Jade templating is nice for faster prototyping
templates.env.add_extension("pypugjs.ext.jinja.PyPugJSExtension")
