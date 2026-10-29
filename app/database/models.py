from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database.connection import Base


class Games(Base):
    __tablename__ = "games"

    id: int = Column(Integer, primary_key=True, index=True)
    title: str = Column(String)
    image_url: str = Column(String)

    offers = relationship("GameOffers", back_populates="game")


class GamePlatforms(Base):
    __tablename__ = "platforms"

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String)
    icon_url: str = Column(String)

    offers = relationship("GameOffers", back_populates="platform")


class GameOffers(Base):
    __tablename__ = "game_offers"

    id: int = Column(Integer, primary_key=True, index=True)
    game_id: int = Column(Integer, ForeignKey("games.id"))
    platform_id: int = Column(Integer, ForeignKey("platforms.id"))
    region: str = Column(String, nullable=False)
    edition: str | None = Column(String, nullable=True)
    likes_count: int = Column(Integer, default=0)
    full_price: float = Column(Float, nullable=False)
    discount_percent: int | None = Column(Integer, default=None, nullable=True)
    cashback_amount: float | None = Column(Float, default=None, nullable=True)

    game = relationship("Games", back_populates="offers")
    platform = relationship("GamePlatforms", back_populates="offers")
