import os

from flask import Flask

from platforms.shopify.web import bp as shopify_bp


app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]

app.register_blueprint(shopify_bp)
