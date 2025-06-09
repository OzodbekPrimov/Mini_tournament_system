from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.db import get_db
from app.schemas.tournament import TournamentCreate, Tournament, PlayerCreate, Player
from app.services.tournament import create_tournament_service, register_player_service, get_players_service
from structlog import get_logger

logger = get_logger()

router = APIRouter(prefix="/tournaments", tags=["tournaments"])

@router.post("/", response_model=Tournament, status_code=status.HTTP_201_CREATED)
async def create_tournament(tournament: TournamentCreate, db: AsyncSession = Depends(get_db)):
    return await create_tournament_service(db, tournament)

@router.post("/{tournament_id}/register", response_model=Player, status_code=status.HTTP_201_CREATED)
async def register_player(tournament_id: int, player: PlayerCreate, db: AsyncSession = Depends(get_db)):
    return await register_player_service(db, tournament_id, player)

@router.get("/{tournament_id}/players", response_model=List[Player])
async def get_players(tournament_id: int, db: AsyncSession = Depends(get_db)):
    return await get_players_service(db, tournament_id)