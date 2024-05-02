# -*- coding: utf-8 -*-
from collections import namedtuple

import pycountry
from phonenumbers import country_code_for_region

Country = namedtuple("Country", "alpha_2 name flag country_code")
countries = list()
for c in sorted(pycountry.countries, key=lambda x: x.name):
    countries.append(
        Country(
            alpha_2=c.alpha_2,
            name=c.name,
            flag=c.flag,
            country_code=country_code_for_region(c.alpha_2),
        )
    )
