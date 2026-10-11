from models.base import with_session
from sqlalchemy.orm import Session

@with_session
def pay_booking(Session: Session):
    pass