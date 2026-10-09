from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, String, ForeignKey, UniqueConstraint
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
        UniqueConstraint("email"),
    )

    airport_staff_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(34))
    last_name: Mapped[str] = mapped_column(String(34))
    email: Mapped[str] = mapped_column(String(124))
    password: Mapped[str]
    staff_type: Mapped[str]

    assigned_airport_icao: Mapped[str] = mapped_column(String(3), ForeignKey("airports.icao"))
    airport: Mapped["Airport"] = relationship(back_populates="staff")

    def __repr__(self) -> str:
        return f"<AirportStaff: id = {self.airport_staff_id}, first name = {self.first_name}, last name = {self.last_name}, email = {self.email}, password = {self.password}, staff type = {self.staff_type}>"