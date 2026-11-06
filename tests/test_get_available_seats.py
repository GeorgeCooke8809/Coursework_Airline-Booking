import pytest
from pytest import raises

from users import add_airline_employee, add_guest
from bookings import create_unpaid_booking
from flights import create_route, add_one_off_flight
from seats import get_available_seats, add_booking_seat

from sqlalchemy.orm import Session
from datetime import datetime, timedelta, date, time, UTC
import logging

from models import Booking, Flight

from utils.exceptions import ExistenceException, InvalidDateException

LOGGER = logging.getLogger(__name__)