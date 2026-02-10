from datetime import datetime
import math
import os
import random
import string

import shopify

from nationbuilder_api import NationBuilderClient
from nationbuilder_api.resp_procs import payload_filter
from worker import queue

from . import session
from .worker import CreateDiscountTask, lock


@queue.task(base=CreateDiscountTask)
@lock
@session
def create_discount(person_id):
    with NationBuilderClient() as nb:
        person = nb.people.get(
            person_id,
            resp_proc=payload_filter(
                ["capital_amount_in_cents", os.environ["SHOP_PENDING_FIELD"]]
            ),
        )
        nb.people.update({os.environ["SHOP_PENDING_FIELD"]: None}, person_id)

        redemption = float(person[os.environ["SHOP_PENDING_FIELD"]])
        capital = int(person["capital_amount_in_cents"]) / 100

        if 0 < redemption <= capital:
            try:
                price_rule = shopify.PriceRule.create(
                    {
                        "title": f"NB_{person_id}_"
                        + "".join(
                            random.choice(string.ascii_uppercase + string.digits)
                            for _ in range(int(os.getenv("SHOP_DISCOUNT_LEN", 10)))
                        ),
                        "target_type": "line_item",
                        "target_selection": "all",
                        "allocation_method": "across",
                        "value_type": "fixed_amount",
                        "value": -(
                            math.floor(
                                redemption
                                * float(os.environ["SHOP_EXCHANGE_RATE"])
                                * 100
                            )
                            / 100
                        ),
                        "customer_selection": "all",
                        "starts_at": datetime.now()
                        .replace(microsecond=0)
                        .astimezone()
                        .isoformat(),
                        "usage_limit": 1,
                    }
                )

                price_rule.add_discount_code(
                    shopify.DiscountCode({"code": price_rule.title})
                )

                nb.people.add_capital(
                    person_id,
                    {
                        "amount_in_cents": -round(redemption * 100),
                        "content": "[Capital Redemption] "
                        + os.getenv("SHOP_CURRENCY", "$")
                        + format(float(price_rule.value[1:]), ".2f")
                        + " "
                        + os.getenv("SHOP_DISCOUNT_PREFIX", "Shopify Credit")
                        + f": {price_rule.title}",
                    },
                    resp_proc=payload_filter("id"),
                )

            except Exception:
                try:
                    price_rule.destroy()
                except NameError:
                    pass
                finally:
                    nb.people.update({os.environ["SHOP_PENDING_FIELD"]: redemption}, person_id)

                raise
