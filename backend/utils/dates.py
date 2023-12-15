# -*- coding: utf-8 -*-
import datetime


def last_day_of_month(any_day):
    any_day = datetime.date(any_day.year, any_day.month, any_day.day)
    next_month = any_day.replace(day=28) + datetime.timedelta(days=4)
    return next_month - datetime.timedelta(days=next_month.day)
