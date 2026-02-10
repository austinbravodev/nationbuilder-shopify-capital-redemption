import os

from flask import Blueprint
from flask_cors import cross_origin

from .tasks import create_discount


bp = Blueprint("shopify", __name__, url_prefix="/shopify")


@bp.route("/capital_redemption/<person_id>")
@cross_origin(
    origins=[origin.strip() for origin in os.environ["NB_ORIGINS"].split(",")]
)
def capital_redemption(person_id):
    create_discount.apply_async((person_id,), countdown=2)
    return "", 204
