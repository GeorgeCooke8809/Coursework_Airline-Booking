from flask import Blueprint, redirect, render_template, session, url_for, request
import logging
from datetime import date
from models import VALID_SEAT_IDS

from flights import (
    search_for_flight,
    calculate_seat_price
)

from seats import (
    get_available_seats
)

from bookings import (
    get_booking_flight,
    get_booking_details,
)

from users import (
    get_guest_favourite_companion,
    get_all_guest_companions
)

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

@guest_portal.route("/flight-search", methods=["GET"])
def flight_search_page():
    origin = request.args.get('orig')
    destination = request.args.get('dest')
    flight_date = date.strptime(request.args.get('date'), "%Y%m%d")

    return render_template("flight-search.html",
                           flights = search_for_flight(origin, destination, flight_date)
                        )

@guest_portal.route("/seat-select/<booking_id>", methods=["GET"])
def seat_selection_page(booking_id: int):
    flight_id = get_booking_flight(booking_id)

    return render_template("seat-selection.html",
                           bookingID=booking_id,
                           all_seats=VALID_SEAT_IDS,
                           available_seats=get_available_seats(flight_id),
                           favourite_companion=get_guest_favourite_companion(session["user_id"]),
                           all_companions=get_all_guest_companions(session["user_id"])
                        )

@guest_portal.route("/pay-booking/<booking_id>", methods=["GET"])
def pay_for_booking(booking_id: int):
    flight_id = get_booking_flight(booking_id)
    price = f"£{calculate_seat_price(flight_id, len(get_booking_details(booking_id)["companions"])):,.2f}"

    return render_template("pay-booking.html",
                            bookingID=booking_id,
                            price=price
                        )