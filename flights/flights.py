from models.base import with_session
from sqlalchemy.orm import Session

@with_session
def get_airport_flights(Session: Session):
    pass

@with_session
def change_flight_status(Session: Session):
    pass

@with_session
def get_flight_details(Session: Session):
    pass

@with_session
def get_route_flights(Session: Session):
    pass

@with_session
def edit_flight_departure_time(Session: Session):
    pass

@with_session
def add_new_flight(Session: Session):
    pass

@with_session
def batch_generate_scheduled_flights(Session: Session):
    pass

@with_session
def search_for_flight(Session: Session):
    pass