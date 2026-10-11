from models.base import with_session
from sqlalchemy.orm import Session

@with_session
def get_all_guest_companions(Session: Session):
    pass

@with_session
def add_companion(Session: Session):
    pass

@with_session
def edit_companion(Session: Session):
    pass

@with_session
def disable_companion(Session: Session):
    pass

@with_session
def favorite_companion(Session: Session):
    pass