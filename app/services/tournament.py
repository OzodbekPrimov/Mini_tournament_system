from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.tournament import create_tournament, get_tournament, create_player, get_players
from app.schemas.tournament import TournamentCreate, PlayerCreate, Tournament, Player
from structlog import get_logger

logger = get_logger()

async def create_tournament_service(db: AsyncSession, tournament: TournamentCreate) -> Tournament:
    db_tournament = await create_tournament(db, tournament)
    return db_tournament

async def register_player_service(db: AsyncSession, tournament_id: int, player: PlayerCreate) -> Player:
    db_player = await create_player(db, tournament_id, player)
    if not db_player:
        if not await get_tournament(db, tournament_id):
            raise HTTPException(status_code=404, detail="Tournament not found")
        if await db.execute(select(Player).filter(Player.email == player.email, Player.tournament_id == tournament_id)).first():
            raise HTTPException(status_code=400, detail="Player already registered")
        raise HTTPException(status_code=400, detail="Max players limit reached")
    return db_player

async def get_players_service(db: AsyncSession, tournament_id: int) -> list[Player]:
    if not await get_tournament(db, tournament_id):
        raise HTTPException(status_code=404, detail="Tournament not found")
    return await get_players(db, tournament_id)