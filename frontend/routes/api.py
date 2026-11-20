from flask import Blueprint, jsonify, request, session
from datetime import datetime, date
import logging

from utils import (
    check_email_already_in_use,
    check_airport_exists,
    RouteExistsException
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
)
from flights import (
    create_route,
    add_one_off_flight,
    add_schedule
)

from models import SERVICE_REPEAT_TYPES

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

@api.route("/add-schedule", methods = ["POST"])
def api_add_schedule():
    request_dict = request.get_json()

    # * Validation

    if request_dict["startDate"] < date.today():
        return jsonify({
            "code": 400,
            "message": "Start date must be in the future"
        })

    if request_dict["startDate"] < request_dict["endDate"]:
        return jsonify({
            "code": 400,
            "message": "End date cannot be before start date"
        })

    # * Processing

    try:
        add_schedule(
            request_dict["routeID"],
            request_dict["startDate"],
            request_dict["endDate"],
            request_dict["repeatType"],
            request_dict["frequency"],
            request_dict["repeatTime"],
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