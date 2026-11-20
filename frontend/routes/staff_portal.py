from flask import Blueprint, render_template, session
from datetime import datetime
import logging

from users import (
    get_all_staff_users
)

from flights import (
    get_all_routes,
    get_route_flights,
    get_route_schedules,
    get_route_name
)

LOGGER = logging.getLogger(__name__)

staff_portal = Blueprint("staff_portal", __name__)

LOGGER.info("Staff blueprint created")

# ! =============== ADMIN PORTAL ===============
@staff_portal.route("/admin", methods = ["GET"])
def admin_page():
    return render_template(
        "admin-page.html",
        staff_users = get_all_staff_users()
    )


# ! =============== OPERATIONS PORTAL ===============
@staff_portal.route("/operations", methods = ["GET"])
def operations_routes_page():
    return render_template(
        "flight-ops-routes.html",
        routes = get_all_routes()
    )

@staff_portal.route("/operations/route-details/<route_id>", methods = ["GET"])
def operations_routes_details(route_id):
    return render_template(
        "flight-ops-route-details.html",
        route_name = get_route_name(route_id),
        route_flights = get_route_flights(route_id),
        route_schedules = get_route_schedules(route_id)
    )