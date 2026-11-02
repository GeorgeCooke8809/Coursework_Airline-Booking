from models.base import with_session
from sqlalchemy.orm import Session

from models import AirportStaff, AirlineEmployee, Guest

@with_session
def check_email_already_in_use(session: Session, email: str) -> bool:
    for model in (AirlineEmployee, AirportStaff, Guest):
        user = (
            session.query(model)
            .filter(model.email == email)
        ).first()

        if user != None:
            return True

    return False

    