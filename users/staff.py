from models.base import with_session
from sqlalchemy.orm import Session

@with_session
def get_all_staff_users(Session: Session):
    pass

@with_session
def add_airline_employee(Session: Session):
    pass

@with_session
def edit_airline_employee(Session: Session):
    pass

@with_session
def delete_airline_employee(Session: Session):
    pass

@with_session
def add_airport_staff(Session: Session):
    pass

@with_session
def edit_airport_staff_member(Session: Session):
    pass

@with_session
def delete_airport_staff(Session: Session):
    pass

@with_session
def get_representative_assigned_guests(Session: Session):
    pass