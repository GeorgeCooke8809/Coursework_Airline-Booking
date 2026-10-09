from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base

if TYPE_CHECKING:
    from models.booking import Booking
    from models.companion import Companion

class BookingSeat(Base):
    __tablename__ = "booking_seats"
    __table_args__ = (
        UniqueConstraint("seat_id", "booking_id"),
    )

    booking_seat_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    booking_id: Mapped[int] = mapped_column(Integer, ForeignKey("bookings.booking_id"))
    booking: Mapped["Booking"] = relationship(back_populates="seats")

    companion_id: Mapped[int] = mapped_column(Integer, ForeignKey("companions.companion_id"))
    companion: Mapped["Companion"] = relationship(back_populates="seats")

    seat_id: Mapped[str] = mapped_column(String(2))

    def __repr__(self):
        return f"<SeatBooking: id = {self.booking_seat_id}, booking_id = {self.booking_id}, companion_id = {self.companion_id}, seat_id = {self.seat_id}>"