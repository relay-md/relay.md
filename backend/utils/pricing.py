# -*- coding: utf-8 -*-
def get_price(yearly: bool = False, private: bool = False):
    if not private:
        return 0
    if yearly:
        return 30
    return 3
