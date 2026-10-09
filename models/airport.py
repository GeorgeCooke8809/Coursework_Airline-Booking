from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base

if TYPE_CHECKING:
    from models.airport_staff import AirportStaff

class Airport(Base):
    __tablename__ = "airports"

    icao: Mapped[str] = mapped_column(String(4), primary_key=True)
    iata: Mapped[str | None] = mapped_column(String(3), unique=True, index=True)
    name: Mapped[str]
    city: Mapped[str]
    country: Mapped[str]
    latitude: Mapped[float]
    longitude: Mapped[float]
    timezone: Mapped[str]

    staff: Mapped[list["AirportStaff"]] = relationship(back_populates="airport")

    def __repr__(self):
        return f"<Airport: icao = {self.icao}, latitude = {self.latitude}, longitude = {self.longitude}, timezone = {self.timezone}>"