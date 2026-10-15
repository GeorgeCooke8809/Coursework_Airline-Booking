from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base

from datetime import datetime

if TYPE_CHECKING:
    from models.flight import Flight
    from models.booking_seat import BookingSeat
    from models.guest import Guest

class Booking(Base):
    __tablename__ = "bookings"

    booking_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    guest_id: Mapped[int] = mapped_column(ForeignKey("guests.guest_id"))
    guest: Mapped["Guest"] = relationship(back_populates="bookings")

    flight_id: Mapped[int] = mapped_column(ForeignKey("flights.flight_id"))
    flight: Mapped["Flight"] = relationship(back_populates="bookings")

    datetime_booked: Mapped[datetime]
    payment_cleared: Mapped[bool]

    seats: Mapped[list["BookingSeat"]] = relationship(back_populates="booking")

    def __repr__(self):
        return f"<Booking: id = {self.booking_id}, guest id = {self.guest_id}>"