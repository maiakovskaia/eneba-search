from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.connection import Base


class Games(Base):
    __tablename__ = "games"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(nullable=True)
    image_url: Mapped[str] = mapped_column(nullable=True)

    offers: Mapped[list["GameOffers"]] = relationship(back_populates="game")


class GamePlatforms(Base):
    __tablename__ = "platforms"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(nullable=True)
    icon_url: Mapped[str] = mapped_column(nullable=True)

    offers: Mapped[list["GameOffers"]] = relationship(back_populates="platform")


class GameOffers(Base):
    __tablename__ = "game_offers"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    game_id: Mapped[int] = mapped_column(ForeignKey("games.id"), nullable=True)
    platform_id: Mapped[int] = mapped_column(ForeignKey("platforms.id"), nullable=True)
    region: Mapped[str]
    edition: Mapped[str | None]
    likes_count: Mapped[int] = mapped_column(default=0, nullable=True)
    full_price: Mapped[float]
    discount_percent: Mapped[int | None]
    cashback_amount: Mapped[float | None]

    game: Mapped["Games"] = relationship(back_populates="offers")
    platform: Mapped["GamePlatforms"] = relationship(back_populates="offers")
