from models.base import with_session
from sqlalchemy.orm import Session

@with_session
def check_login_details(Session: Session):
    pass