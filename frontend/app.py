from flask import Flask
from .routes import api, guest_portal# , staff_portal
from .routes.staff_portal import staff_portal


def create_app():
    app = Flask(__name__)

    app.register_blueprint(api, url_prefix="/api")
    app.register_blueprint(guest_portal)
    app.register_blueprint(staff_portal, url_prefix="/employee")

    return app