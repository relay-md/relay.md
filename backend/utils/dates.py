# -*- coding: utf-8 -*-
import datetime


def last_day_of_month(any_day):
    any_day = datetime.date(any_day.year, any_day.month, any_day.day)
    next_month = any_day.replace(day=28) + datetime.timedelta(days=4)
    return next_month - datetime.timedelta(days=next_month.day)


def percentage_of_current_year(any_date):
    year = any_date.year
    first_day_in_year = datetime.date(year, 1, 1)
    last_day_in_year = datetime.date(year + 1, 1, 1) - datetime.timedelta(days=1)
    return (any_date.date() - first_day_in_year) / (
        last_day_in_year - first_day_in_year
    )


def percentage_of_current_month(any_date):
    year = any_date.year
    month = any_date.month
    first_day_in_month = datetime.date(year, month, 1)
    next_month = any_date.replace(day=28) + datetime.timedelta(days=4)
    last_day_in_month = (next_month - datetime.timedelta(days=next_month.day)).date()
    return (any_date.date() - first_day_in_month) / (
        last_day_in_month - first_day_in_month
    )
