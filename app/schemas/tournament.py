
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime

class TournamentBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    max_players: int = Field(..., ge=1)
    start_at: datetime = Field(...)

class TournamentCreate(TournamentBase):
    pass

class Tournament(TournamentBase):
    id: int
    created_at: datetime
    registered_players: int = 0

    class Config:
        from_attributes = True

class PlayerBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=70)
    email: EmailStr

class PlayerCreate(PlayerBase):
    pass

class Player(PlayerBase):
    id: int
    tournament_id: int
    created_at: datetime

    class Config:
        from_attributes = True

