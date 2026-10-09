from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date
from models.base import Base

if TYPE_CHECKING:
    from models.guest import Guest
    from models.booking_seat import BookingSeat

STATUS_OPTIONS = ("active", "inactive")
SEX_OPTIONS = ("M", "F", "X")

class Companion(Base):
    __tablename__ = "companions"
    __table_args__ = (
        CheckConstraint(
            f"status IN {STATUS_OPTIONS}",
            name="ck_status_correct"
        ),
        CheckConstraint(
            f"sex IN {SEX_OPTIONS}",
            name="ck_sex_correct"
        ),
    )

    companion_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    guest_id: Mapped[int] = mapped_column(ForeignKey("guests.guest_id"))
    guest: Mapped["Guest"] = relationship(back_populates="companions")

    passport_name: Mapped[str] = mapped_column(String(38))
    passport_number: Mapped[str] = mapped_column(String(9))
    passport_expiry: Mapped[date]
    nationality: Mapped[str]
    passport_issue_authority: Mapped[str]
    date_of_birth: Mapped[date]
    sex: Mapped[str] = mapped_column(String(0))
    status: Mapped[str]
    favorite: Mapped[bool]

    seats: Mapped[list["BookingSeat"]] = relationship(back_populates="companion")

    def __repr__(self):
        return f"<Companion: companion_id = {self.companion_id}, guest_id = {self.guest_id}, passport_name = {self.passport_name}>"