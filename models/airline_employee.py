from typing import TYPE_CHECKING

from sqlalchemy import String, CheckConstraint, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base

if TYPE_CHECKING:
    from models.guest import Guest

AIRLINE_EMPLOYEE_TYPES = ("support", "admin", "operations")

class AirlineEmployee(Base):
    __tablename__ = "airline_employees"
    __table_args__ = (
        CheckConstraint(
            f"employee_type IN {AIRLINE_EMPLOYEE_TYPES}",
            name="ck_employee_type_correct"
        ),
        UniqueConstraint("email"),
    )

    airline_employee_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(34))
    last_name: Mapped[str] = mapped_column(String(34))
    email: Mapped[str] = mapped_column(String(124))
    phone: Mapped[str] = mapped_column(String(14))
    employee_type: Mapped[str]

    guests: Mapped[list["Guest"]] = relationship(back_populates="customer_support_rep")

    def __repr__(self):
        return f"<AirlineEmployee: airline_employee_id = {self.airline_employee_id}, first_name = {self.first_name}, last_name = {self.last_name}, employee_type = {self.employee_type}>"