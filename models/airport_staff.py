from typing import TYPE_CHECKING

from sqlalchemy import Boolean, CheckConstraint, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base

if TYPE_CHECKING:
    from models.airport import Airport

AIRPORT_STAFF_TYPES = ("gate", "check-in")

class AirportStaff(Base):
    __tablename__ = "airport_staff"
    __table_args__ = (
        CheckConstraint(
            f"staff_type IN {AIRPORT_STAFF_TYPES}",
            name="ck_airport_staff_type_correct",
        ),
    )

    airport_staff_id: mapped_column[int] = mapped_column(primary_key=True, autoincrement=True)
    first_name: mapped_column[str] = mapped_column(String(34))
    last_name: mapped_column[str] = mapped_column(String(34))
    email: mapped_column[str] = mapped_column(String(124))
    password: mapped_column[str]
    staff_type: mapped_column[str]

    assigned_airport_icao: mapped_column[str] = mapped_column(String(3), ForeignKey("airlines.icao")) # TODO: Make relationship between assigned airport ICAO and airports
    airport: Mapped["Airport"] = relationship(back_populates="staff")

    def __repr__(self) -> str:
        return f"<AirportStaff: id = {self.airport_staff_id}, first name = {self.first_name}, last name = {self.last_name}, email = {self.email}, password = {self.password}, staff type = {self.staff_type}>"