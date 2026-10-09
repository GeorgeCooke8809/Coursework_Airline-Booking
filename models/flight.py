from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey, Integer, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base

from datetime import datetime

if TYPE_CHECKING:
    from models.service import Service
    from models.booking import Booking

FLIGHT_STATUS_OPTIONS = ("scheduled", "departed", "cancelled")

class Flight(Base):
    __tablename__ = "flights"
    __table_args__ = (
            CheckConstraint(
                f"status IN {FLIGHT_STATUS_OPTIONS}",
                name="ck_flight_status_correct",
            ),
        )

    flight_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    service_id: Mapped[int] = mapped_column(Integer, ForeignKey("services.service_id"))
    service: Mapped["Service"] = relationship(back_populates="flights")

    flight_number: Mapped[str] = mapped_column(String(3))
    scheduled_departure_datetime_utc: Mapped[datetime]
    datetime_created_utc: Mapped[datetime]
    status: Mapped[str]

    bookings: Mapped[list["Booking"]] = relationship(back_populates="flight")

    def __repr__(self):
        return f"<Flight: id = {self.flight_id}, service id = {self.service_id}, flight number = {self.flight_number}, scheduled departure utc = {self.scheduled_departure_datetime_utc}, created = {self.datetime_created_utc}, status = {self.status}>"