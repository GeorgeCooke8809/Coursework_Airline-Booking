from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base

if TYPE_CHECKING:
    from models.airport import Airport
    from models.service import Service

class Route(Base):
    __tablename__ = "routes"
    __table_args__ = (
        UniqueConstraint("origin_icao", "destination_icao")
    )

    route_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    origin_icao: Mapped[str] = mapped_column(String(3), ForeignKey("airports.icao"))
    origin: Mapped["Airport"] = relationship(back_populates="departures")

    destination_icao: Mapped[str] = mapped_column(String(3), ForeignKey("airports.icao"))
    destination: Mapped["Airport"] = relationship(back_populates="arrivals")

    services: Mapped[list["Service"]] = relationship(back_populates="route")

    def __repr__(self) -> str:
        return f"<Route: id = {self.route_id}, origin = {self.origin_icao}, destination = {self.destination_icao}>"