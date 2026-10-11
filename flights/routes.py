from models.base import with_session
from sqlalchemy.orm import Session

@with_session
def create_route(Session: Session):
    pass

@with_session
def get_all_routes(Session: Session):
    pass

@with_session
def generate_route_statistics(Session: Session):
    pass