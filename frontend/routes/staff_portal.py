from flask import Blueprint, render_template, session
from datetime import datetime
import logging

LOGGER = logging.getLogger(__name__)

staff_portal = Blueprint("staff_portal", __name__)

LOGGER.info("Staff blueprint created")

# ! =============== ADMIN PORTAL ===============
@staff_portal.route("/admin", methods = ["GET"])
def admin_page():
    return render_template(
        "admin-page.html"
    )