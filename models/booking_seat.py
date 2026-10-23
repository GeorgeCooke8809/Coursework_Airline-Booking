from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey, Integer, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base

if TYPE_CHECKING:
    from models.booking import Booking
    from models.companion import Companion

VALID_SEAT_IDS = (
    "1A", "1B", "1C",
    "2A", "2B", "2C",
    "3A", "3B", "3C",
    "4A", "4B", "4C",
    "5A", "5B", "5C",
    "6A", "6B", "6C",
    "7A", "7B", "7C",
    "8A", "8B", "8C",
    "9A", "9B", "9C",
    "10A", "10B", "10C"
)

VALID_PASSENGER_STATUS = ("not arrived", "checked", "boarded")

class BookingSeat(Base):
    __tablename__ = "booking_seats"
    __table_args__ = (
        UniqueConstraint("seat_id", "booking_id"),
        CheckConstraint(
                        f"seat_id IN {VALID_SEAT_IDS}",
                        name="ck_seat_id_correct",
                    ),
        CheckConstraint(
                        f"status IN {VALID_PASSENGER_STATUS}",
                        name="ck_status_correct",
                    ),
    )

    booking_seat_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    booking_id: Mapped[int] = mapped_column(Integer, ForeignKey("bookings.booking_id"))
    booking: Mapped["Booking"] = relationship(back_populates="seats")

    companion_id: Mapped[int] = mapped_column(Integer, ForeignKey("companions.companion_id"))
    companion: Mapped["Companion"] = relationship(back_populates="seats")

    seat_id: Mapped[str] = mapped_column(String(2))

    status: Mapped[str]

    def __repr__(self):
        return f"<SeatBooking: id = {self.booking_seat_id}, booking_id = {self.booking_id}, companion_id = {self.companion_id}, seat_id = {self.seat_id}>"