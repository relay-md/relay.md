# -*- coding: utf-8 -*-
from ..config import get_config


def get_price(yearly: bool = False, private: bool = False):
    if not private:
        return 0
    if yearly:
        return get_config().PRICING_TEAM_YEARLY
    return get_config().PRICING_TEAM_MONTHLY
