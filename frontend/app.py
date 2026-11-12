from flask import Flask
from .routes import api, guest_portal# , staff_portal
from .routes.staff_portal import staff_portal


def create_app():
    app = Flask(__name__)

    app.register_blueprint(api, url_prefix="/api")
    app.register_blueprint(guest_portal)
    app.register_blueprint(staff_portal, url_prefix="/employee")
    app.secret_key = "5b8a278484b383337eb35486f24418f90e0579aa5495aa3bb6f677cf06c1ca67a4a972e1cdd4b644e08c9cd0e94ed255b1bec1b5d0def424a92014b881817a1cfaf8101df12e8507e7984bc2e24e993bd0abe3d18a8646dcb8c32350cc38d99dd511b8053692fa2fb594b05c005a21f5282cbe5e1e339eb5374b97b85ab5bc0f"

    return app