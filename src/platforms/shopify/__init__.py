import os
from functools import wraps

import shopify


def session(f):
    @wraps(f)
    def dec_f(*args, **kwargs):
        with shopify.Session.temp(
            os.environ["SHOP_NAME"] + ".myshopify.com",
            os.getenv("SHOP_API_VERSION", "2021-01"),
            os.environ["SHOP_PASSWORD"],
        ):
            return f(*args, **kwargs)

    return dec_f
