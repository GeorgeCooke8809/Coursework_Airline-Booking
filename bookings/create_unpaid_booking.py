from models.base import with_session
from sqlalchemy.orm import Session
from models import Guest, Flight, Booking

@with_session
def create_unpaid_booking(Session: Session, guest_id: int, flight_id: int):
    pass