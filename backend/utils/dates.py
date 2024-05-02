# -*- coding: utf-8 -*-
import datetime


def last_day_of_month(any_day):
    any_day = datetime.date(any_day.year, any_day.month, any_day.day)
    next_month = any_day.replace(day=28) + datetime.timedelta(days=4)
    return next_month - datetime.timedelta(days=next_month.day)


def percentage_of_period_year(any_date: datetime.date, until: datetime.date):
    first_day_in_period = until - datetime.timedelta(days=365)
    last_day_in_period = until
    return (any_date - first_day_in_period) / (last_day_in_period - first_day_in_period)


def percentage_of_period_month(any_date: datetime.date, until: datetime.date):
    if until.month > 1:
        first_day_in_period = until.replace(month=until.month - 1)
    else:
        first_day_in_period = until.replace(month=12, year=until.year - 1)
    last_day_in_period = until
    return (any_date - first_day_in_period) / (last_day_in_period - first_day_in_period)
