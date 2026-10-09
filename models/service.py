from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date, time
from models.base import Base

if TYPE_CHECKING:
    from models.route import Route
    from models.flight import Flight

REPEAT_TYPES = ("daily", "weekly", "monthly")

class Service(Base):
    __tablename__ = "services"
    __table_args__ = (
            CheckConstraint(
                "end_date >= start_date",
                name="ck_end_date_start_date_correct",
            ),
            CheckConstraint(
                f"repeat_type IN {REPEAT_TYPES}",
                name="ck_repeat_type_correct",
            ),
        )

    service_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    route_id: Mapped[int] = mapped_column(Integer,ForeignKey("routes.route_id"))
    route: Mapped["Route"] = relationship(back_populates="services")

    start_date: Mapped[date]
    end_date: Mapped[date]
    repeat_type: Mapped[str]
    repeats_on: Mapped[int]
    repeat_time_utc: Mapped[time]
    repeat_frequency: Mapped[int]
    shown_in_list: Mapped[bool]

    flights: Mapped[list["Flight"]] = relationship(back_populates="service")

    def __repr__(self):
        return f"<Service: id = {self.service_id}, route id = {self.route_id}, start date = {self.start_date}, end date = {self.end_date}, repeat type = {self.repeat_type}, repeats on = {self.repeats_on}, time = {self.repeat_time_utc}, repeat frequency = {self.repeat_frequency}, shown in list = {self.shown_in_list}>"