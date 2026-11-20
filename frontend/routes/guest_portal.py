from flask import Blueprint, redirect, render_template, session, url_for
import logging

LOGGER = logging.getLogger(__name__)

guest_portal = Blueprint("pages", __name__)

LOGGER.info("Website blueprint created")

# !=============== Login ===============
@guest_portal.route("/login", methods = ["GET"])
def login_page():
    return render_template(
        "login.html",
    )

@guest_portal.route("/create-new-account", methods = ["GET"])
def create_account_page():
    return render_template(
        "create-account.html",
    )

@guest_portal.route("/logout", methods = ["GET"])
def log_out():
    session.pop("user_id")
    session.pop("user_type")

    return redirect("/")

# !=============== Main Portal ===============
@guest_portal.route("/", methods = ["GET"])
def home_page():
    return render_template(
        "index.html"
    )