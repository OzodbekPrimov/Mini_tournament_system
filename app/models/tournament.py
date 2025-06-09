from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import pytz

BASE = declarative_base()

class Tournament(BASE):
    __tablename__ = "tournaments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    max_players = Column(Integer)
    start_at = Column(DateTime)
    created_at = Column(DateTime, default=lambda: datetime.now(pytz.UTC))
    players = relationship("Player", back_populates="tournament")


class Player(BASE):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    tournament_id = relationship("Tournament", back_populates="players")
