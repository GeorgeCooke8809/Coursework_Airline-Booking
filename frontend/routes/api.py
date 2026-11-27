from flask import Blueprint, jsonify, request, session
from datetime import datetime, date, time, UTC
import logging

from utils import (
    check_email_already_in_use,
    check_airport_exists,
    RouteExistsException,
    search_airport
)
from users import (
    add_airline_employee,
    delete_airline_employee,
    add_airport_staff,
    delete_airport_staff,
    add_guest,
    delete_guest,
    get_all_guest_users,
    get_all_staff_users,
    check_login_details,
    add_companion,
    get_companion_details
)
from flights import (
    create_route,
    add_one_off_flight,
    add_schedule,
    change_flight_status
)

from bookings import (
    create_unpaid_booking,
    pay_booking
)

from seats import (
    add_booking_seat,
    change_booking_seat_status
)

from models import SERVICE_REPEAT_TYPES, SEX_OPTIONS

# TODO: Add session checks for authorisation on relevant API calls


LOGGER = logging.getLogger(__name__)

api = Blueprint("api", __name__)

LOGGER.info("API blueprint created")

# Admin Portal

@api.route("get-staff-users", methods=["POST"])
def api_get_all_staff_users():
    try:
        staff_users = get_all_staff_users()

        return jsonify({
            "code": 200,
            "message": "",
            "content": staff_users
        })
    except:
        return jsonify({
            "code": 500,
            "message": "Something went wrong, please try again later or contact support."
        })

@api.route("get-guest-users", methods=["POST"])
def api_get_all_guest_users():
    try:
        guest_users = get_all_guest_users()

        return jsonify({
            "code": 200,
            "message": "",
            "content": guest_users
        })
    except:
        return jsonify({
            "code": 500,
            "message": "Something went wrong, please try again later or contact support."
        })

@api.route("add-airline-employee", methods = ["POST"])
def api_add_airline_employee():
    request_dict = request.get_json()

    # * Validation
    if (
        len(request_dict["first_name"]) > 34
        or request_dict["first_name"] == ""
    ):
        return jsonify({
            "code": 400,
            "message": "Invalid first name has been given"
        })

    if (len(request_dict["last_name"]) > 34):
            return jsonify({
                "code": 400,
                "message": "Invalid last name has been given"
            })

    if check_email_already_in_use(request_dict["email"]):
        return jsonify({
            "code": 400,
            "message": "That email is already in use"
        })

    phone = request_dict["phone"].replace(" ", "") # Remove any spaces added to phone number
    
    if not phone.isnumeric():
        return jsonify({
            "code": 400,
            "message": "Phone number must only be numbers"
        })

    if len(phone) > 14:
        return jsonify({
            "code": 400,
            "message": "Phone number is too long"
        })

    
    # * Processing

    try:
        add_airline_employee(
            request_dict["first_name"],
            request_dict["last_name"],
            request_dict["email"],
            request_dict["phone"],
            request_dict["password"],
            request_dict["staff_type"]
        )

        return jsonify({
            "code": 200,
            "message": ""
        })
    except:
        return jsonify({
            "code": 500,
            "message": "Something went wrong. Please try again later or contact support."
        })

@api.route("add-airport-staff", methods = ["POST"])
def api_add_airport_staff():
    request_dict = request.get_json()
    LOGGER.info("made it to start")

    # * Validation
    if (
        len(request_dict["first_name"]) > 34
        or request_dict["first_name"] == ""
    ):
        return jsonify({
            "code": 400,
            "message": "Invalid first name has been given"
        })

    if (len(request_dict["last_name"]) > 34):
            return jsonify({
                "code": 400,
                "message": "Invalid last name has been given"
            })

    if check_email_already_in_use(request_dict["email"]):
        return jsonify({
            "code": 400,
            "message": "That email is already in use"
        })

    if not check_airport_exists(request_dict["airport_icao"].upper()):
        return jsonify({
                    "code": 400,
                    "message": "That airport does not exist"
                })

    
    # * Processing

    try:
        add_airport_staff(
            request_dict["first_name"],
            request_dict["last_name"],
            request_dict["email"],
            request_dict["password"],
            request_dict["staff_type"],
            request_dict["airport_icao"].upper(),
        )

        return jsonify({
            "code": 200,
            "message": ""
        })
    except:
        return jsonify({
            "code": 500,
            "message": "Something went wrong. Please try again later or contact support."
        })

@api.route("delete-guest", methods = ["POST"])
def api_delete_guest():
    request_dict = request.get_json()

    try:
        delete_guest(request_dict["id"])
    except:
        return jsonify({
            "code": 500,
            "message": "Something went wrong, please try again later or contact support"
        })

    return jsonify({
        "code": 200,
        "message": ""
    })

@api.route("delete-staff", methods = ["POST"])
def api_delete_staff():
    request_dict = request.get_json()

    # TODO: Add delete staff endpoint

# Guest Portal

@api.route("check-login", methods = ["POST"])
def api_check_login_details():
    request_dict = request.get_json()

    details_status = check_login_details(request_dict["email"], request_dict["password"])

    if details_status is None:
        return jsonify({
            "code": 400,
            "message": "Those login details are not correct"
        })

    session["user_id"] = details_status["id"]
    session["user_type"] = details_status["user_type"]

    return jsonify({
        "code": 200,
        "message": "",
        "page": details_status["user_type"] # "guest" | "support" | "operations" | "admin" | "gate" | "check-in"
    })

@api.route("add-guest", methods = ["POST"])
def api_add_guest():
    request_dict = request.get_json()

    # * Validation
    if len(request_dict["first_name"]) > 34 or request_dict["first_name"] == "":
        return ({
            "code": 400,
            "message": "The first name given is invalid"
        })

    if len(request_dict["last_name"]) > 34:
            return ({
                "code": 400,
                "message": "The last name given is invalid"
            })

    phone = request_dict["phone"].replace(" ", "") # Remove any spaces added to phone number
    
    if not phone.isnumeric():
        return ({
            "code": 400,
            "message": "Phone numbers must be numeric"
        })

    if len(phone) > 14:
        return ({
            "code": 400,
            "message": "Phone number is too long"
        })

    if check_email_already_in_use(request_dict["email"]):
        return ({
            "code": 400,
            "message": "That email is already in use"
        })

    if request_dict["password"] == "":
        return ({
            "code": 400,
            "message": "Please enter a phone number"
        })
    # * Processing
    try:
        add_guest(request_dict["first_name"], request_dict["last_name"], request_dict["email"], request_dict["phone"], request_dict["password"])


        return jsonify({
            "code": 200,
            "message": "",
        })
    
    except:
        return jsonify({
            "code": 500,
            "message": "Something went wrong, please try again later or contact support."
        })


# Operations Portal

@api.route("add-route", methods = ["POST"])
def api_add_route():
    request_dict = request.get_json()

    LOGGER.debug(f"{request_dict = }")

    if check_airport_exists(request_dict["origin"]) != True:
        return jsonify({
            "code": 400, 
            "message": "Invalid origin airport given"
        })

    if check_airport_exists(request_dict["destination"]) != True:
            return jsonify({
                "code": 400, 
                "message": "Invalid destination airport given"
            })

    if float(request_dict["price"]) < 0:
        return jsonify({
            "code": 400,
            "message": "Invalid price given"
        })

    try:
        create_route(request_dict["origin"], request_dict["destination"], float(request_dict["price"]))
    except RouteExistsException:
        return jsonify({
            "code": 400,
            "message": "Route already exists"
        })
    except:
        return jsonify({
            "code": 500,
            "message": "Something went wrong, please try again later or contact support."
        })

    return jsonify({
        "code": 200,
        "message": ""
    })

@api.route("/add-one-off-flight", methods = ["POST"])
def api_add_one_off_flight():
    request_dict = request.get_json()

    LOGGER.info("add-one-off-flight API request received")
    LOGGER.debug(f"{request_dict = }")

    departure_time = datetime.strptime(request_dict["departureDatetime"], "%Y-%m-%dT%H:%M").replace(tzinfo=UTC) # String Format: '2026-11-20T12:08'

    # * Validation
    if departure_time < datetime.now(tz=UTC):
        return jsonify({
            "code": 400,
            "message": "Flight departure datetime must be in the future"
        })

    # * Processing
    
    try:
        add_one_off_flight(
            request_dict["routeID"],
            departure_time
        )
    except:
        return jsonify({
            "code": 500,
            "message": "Something went wrong, please try again later or contact support."
        })

    return jsonify({
        "code": 200,
        "message": ""
    })

@api.route("/add-schedule", methods = ["POST"])
def api_add_schedule():
    request_dict = request.get_json()

    LOGGER.debug(f"{request_dict = }")

    start_date = date.strptime(request_dict["startDate"], "%Y-%m-%d")
    end_date = date.strptime(request_dict["endDate"], "%Y-%m-%d")
    schedule_time = time.strptime(request_dict["repeatTime"], "%H:%M")

    # * Validation

    if start_date < date.today():
        return jsonify({
            "code": 400,
            "message": "Start date must be in the future"
        })

    if start_date > end_date:
        return jsonify({
            "code": 400,
            "message": "End date cannot be before start date"
        })

    # * Processing

    try:
        add_schedule(
            request_dict["routeID"],
            start_date,
            end_date,
            request_dict["repeatType"],
            request_dict["frequency"],
            schedule_time,
            request_dict["repeatsOn"]
        )
    except:
        return jsonify({
            "code": 500,
            "message": "Something went wrong, please try again later or contact support."
        })

    return jsonify({
        "code": 200,
        "message": ""
    })

@api.route("search-airport", methods = ["POST"])
def api_search_airport():
    request_dict = request.get_json()

    try:
        airports = search_airport(request_dict["airportSearch"])
    except:
        return jsonify({
            "code": 500,
            "message": "Something went wrong, please try again later or contact support"
        })

    return jsonify({
        "code": 200,
        "message": "",
        "content": airports
    })

# Guest Booking Flow
@api.route("/add-unpaid-booking", methods=["POST"])
def api_add_unpaid_booking():
    request_dict = request.get_json()

    if "user_id" not in session:
        return jsonify({
            "code": 401,
            "message": "You must be logged in to make a booking"
        })

    guest_id = session["user_id"]

    if session["user_type"] != "guest":
        return jsonify({
            "code": 401,
            "message": "Can only make bookings as a guest"
        })

    try:
        booking_id = create_unpaid_booking(guest_id, request_dict["flightID"])
    except:
        return jsonify({
            "code": 500,
            "message": "Something went wrong, please try again later or contact support."
        })

    return jsonify({
        "code": 200,
        "message": "",
        "content": booking_id
    })

@api.route("/create-companion", methods=["POST"])
def api_create_companion():
    # TODO: Will need to take in guest ID instead of taking from session as an argument for when support does it for them
    request_dict = request.get_json()

    LOGGER.debug(f"{request_dict = }")

    # * Validation
    if len(request_dict["passport_name"]) > 38 or request_dict["passport_name"] == "":
        return jsonify({
            "code": 400,
            "message": "Passport name must be given and under 38 characters"
        })

    passport_expiry = date.strptime(request_dict["passport_expiry"], "%Y-%m-%d")

    if passport_expiry < date.today():
        return jsonify({
            "code": 400,
            "message": "Passport expiry must be after today."
        })

    if len(request_dict["passport_number"]) > 9 or request_dict["passport_number"] == "":
        return jsonify({
            "code": 400,
            "message": "Passport number must be given and fewer than 9 characters."
        })

    dob = date.strptime(request_dict["dob"], "%Y-%m-%d")

    if dob > date.today():
        return jsonify({
            "code": 400,
            "message": "Date of birth cannot be after today."
        })

    if request_dict["nationality"] == "":
        return jsonify({
            "code": 400,
            "message": "Nationality must be provided."
        })

    if request_dict["passport_authority"] == "":
        return jsonify({
            "code": 400,
            "message": "Passport authority must be provided."
        })

    if request_dict["passport_sex"] not in SEX_OPTIONS:
            return jsonify({
                "code": 400,
                "message": "Passport sex must be 'X', 'F', or 'M'."
            })

    # * Processing

    try:
        new_companion_id = add_companion(
            session["user_id"],
            request_dict["passport_name"],
            passport_expiry,
            request_dict["passport_number"],
            dob,
            request_dict["nationality"],
            request_dict["passport_sex"],
            request_dict["passport_authority"]
        )
    except:
        return jsonify({
            "code": 500,
            "message": "Something went wrong, please try again later or contact support."
        })

    return jsonify({
        "code": 200,
        "message": "",
        "content": new_companion_id
    })

@api.route("/get-companion-details", methods=["POST"])
def api_get_companion_details():
    companion_id = int(request.get_json()["companionID"])

    return jsonify({
        "code": 200,
        "message": "",
        "content": get_companion_details(companion_id)
    })

@api.route("/add-initial-companions", methods=["POST"])
def api_add_initial_companions():
    request_dict = request.get_json()
    # TODO: Will need validation of session user_id and booking ownership

    try:
        for companion in request_dict["companions_list"]:
            add_booking_seat(request_dict["bookingID"], companion[1], companion[2]) # Ignores companion[0] as that is just used for styling in the web page
    except:
        return jsonify({
            "code": 500,
            "message": "Something went wrong, please try again later or contact support"
        })

    return jsonify({
        "code": 200,
        "message": ""
    })

@api.route("/pay-booking", methods=["POST"])
def api_pay_booking():
    booking_id = request.get_json()["bookingID"]

    try:
        pay_booking(booking_id)
    except:
        return jsonify({
            "code": 500,
            "message": "Something went wrong. Please try again later or contact support."
        })

    return jsonify({
        "code": 200,
        "message": ""
    })

# Check-In / Gate Portal
@api.route("/depart-aircraft", methods=["POST"])
def api_depart_aircraft():
    flight_id = request.get_json()["flightID"]

    try:
        change_flight_status(flight_id, "departed")
    except:
        return jsonify({
            "code": 500,
            "message": "Something went wrong, please try again later or contact support."
        })

    return jsonify({
        "code": 200,
        "message": ""
    })

@api.route("/board-seat", methods=["POST"])
def api_mark_boarded():
    flight_id = request.get_json()["bookingSeatID"]

    try:
        change_booking_seat_status(flight_id, "boarded")
    except:
        return jsonify({
            "code": 500,
            "message": "Something went wrong, please try again later or contact support."
        })

    return jsonify({
        "code": 200,
        "message": ""
    })

@api.route("/arrive-seat", methods=["POST"])
def api_mark_arrived():
    flight_id = request.get_json()["bookingSeatID"]

    try:
        change_booking_seat_status(flight_id, "checked")
    except:
        return jsonify({
            "code": 500,
            "message": "Something went wrong, please try again later or contact support."
        })

    return jsonify({
        "code": 200,
        "message": ""
    })