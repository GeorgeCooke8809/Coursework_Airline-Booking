from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base

if TYPE_CHECKING:
    from models.companion import Companion
    from models.booking import Booking
    from models.airline_employee import AirlineEmployee

class Guest(Base):
    __tablename__ = "guests"
    __table_args__ = (
        UniqueConstraint("email"),
    )

    guest_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    airline_employee_id: Mapped[int] = mapped_column(ForeignKey("airline_employees.airline_employee_id"))
    customer_support_rep: Mapped["AirlineEmployee"] = relationship(back_populates="guests")

    first_name: Mapped[str] = mapped_column(String(34))
    last_name: Mapped[str] = mapped_column(String(34))
    email: Mapped[str] = mapped_column(String(124))
    phone: Mapped[str] = mapped_column(String(14))
    password: Mapped[str]

    companions: Mapped[list["Companion"]] = relationship(back_populates="guest")

    bookings: Mapped[list["Booking"]] = relationship(back_populates="guest")

    def __repr__(self):
        return f"<Guest: guest_id = {self.guest_id}, airline_employee_id = {self.airline_employee_id}, first_name = {self.first_name}, last_name = {self.last_name}>"