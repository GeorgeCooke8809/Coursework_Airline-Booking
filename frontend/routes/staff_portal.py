from flask import Blueprint, render_template, session, redirect
from datetime import datetime
import logging

from users import (
    get_all_staff_users
)

from flights import (
    get_all_routes,
    get_route_flights,
    get_route_schedules,
    get_route_name,
    get_airport_flights,
    get_flight_details
)

from utils import (
    get_staff_airport
)

from seats import (
    get_flight_passengers
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
        route_schedules = get_route_schedules(route_id),
        route_id = route_id
    )


# ! =============== GATE/CHECK PORTAL ===============
@staff_portal.route("/gate-check-flights", methods=["GET"])
def gate_and_check_flights_page():
    if "user_type" not in session or session["user_type"] not in ["check-in", "gate"]:
        return redirect("/")

    airport = get_staff_airport(session["user_id"])
    return render_template("gate-check-flights-list.html",
                           flights=get_airport_flights(airport) # TODO: Make this show delayed flights as well even if from the past
    )

@staff_portal.route("/gate-check-flight-details/<flight_id>", methods=["GET"])
def gate_and_check_flight_details_page(flight_id: int):
    if "user_type" not in session or session["user_type"] not in ["check-in", "gate"]:
        return redirect("/")

    return render_template("gate-check-flight-details.html",
                           flight_id=flight_id,
                           passengers=get_flight_passengers(flight_id, session["user_id"]),
                           user_type=session["user_type"],
                           flight_details=get_flight_details(flight_id, session["user_id"])
    )