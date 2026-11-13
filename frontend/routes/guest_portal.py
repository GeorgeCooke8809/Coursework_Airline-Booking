from flask import Blueprint, redirect, render_template, session
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