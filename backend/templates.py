# -*- coding: utf-8 -*-
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(
    directory=r"backend/templates",
)

# Jade templating is nice for faster prototyping
templates.env.add_extension("pypugjs.ext.jinja.PyPugJSExtension")
