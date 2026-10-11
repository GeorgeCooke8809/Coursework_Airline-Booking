from models.base import with_session
from sqlalchemy.orm import Session

@with_session
def get_route_schedules(Session: Session):
    pass

@with_session
def add_schedule(Session: Session):
    pass

@with_session
def edit_schedule(Session: Session):
    pass

@with_session
def delete_schedule(Session: Session):
    pass