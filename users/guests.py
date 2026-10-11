from models.base import with_session
from sqlalchemy.orm import Session

@with_session
def get_all_guest_users(Session: Session):
    pass

@with_session
def get_guest_details(Session: Session):
    pass

@with_session
def get_guest_support_representative(Session: Session):
    pass

@with_session
def add_guest(Session: Session):
    pass

@with_session
def edit_guest(Session: Session):
    pass

@with_session
def delete_guest(Session: Session):
    pass