from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from app.models.tournament import Tournament, Player
from app.schemas.tournament import TournamentCreate, PlayerCreate
from structlog import get_logger

logger = get_logger()

async def create_tournament(db: AsyncSession, tournament: TournamentCreate):
    try:
        db_tournament = Tournament(**tournament.dict())
        db.add(db_tournament)
        await db.commit()
        await db.refresh(db_tournament)
        logger.info("Tournament created", tournament_id=db_tournament.id)
        return db_tournament
    except SQLAlchemyError as e:
        logger.error("Failed to create tournament", error=str(e))
        raise

async def get_tournament(db: AsyncSession, tournament_id: int):
    try:
        result = await db.execute(select(Tournament).filter(Tournament.id == tournament_id))
        tournament = result.scalars().first()
        logger.info("Tournament fetched", tournament_id=tournament_id)
        return tournament
    except SQLAlchemyError as e:
        logger.error("Failed to fetch tournament", tournament_id=tournament_id, error=str(e))
        raise

async def create_player(db: AsyncSession, tournament_id: int, player: PlayerCreate):
    try:

        tournament = await get_tournament(db, tournament_id)
        if not tournament:
            logger.warning("Tournament not found", tournament_id=tournament_id)
            return None


        result = await db.execute(select(Player).filter(Player.email == player.email, Player.tournament_id == tournament_id))
        if result.scalars().first():
            logger.warning("Player already registered", email=player.email, tournament_id=tournament_id)
            return None


        result = await db.execute(select(Player).filter(Player.tournament_id == tournament_id))
        current_players = len(result.scalars().all())
        if current_players >= tournament.max_players:
            logger.warning("Max players limit reached", tournament_id=tournament_id)
            return None

        db_player = Player(tournament_id=tournament_id, **player.dict())
        db.add(db_player)
        await db.commit()
        await db.refresh(db_player)
        logger.info("Player registered", player_id=db_player.id, tournament_id=tournament_id)
        return db_player
    except SQLAlchemyError as e:
        logger.error("Failed to register player", tournament_id=tournament_id, error=str(e))
        raise

async def get_players(db: AsyncSession, tournament_id: int):
    try:
        result = await db.execute(select(Player).filter(Player.tournament_id == tournament_id))
        players = result.scalars().all()
        logger.info("Players fetched", tournament_id=tournament_id, count=len(players))
        return players
    except SQLAlchemyError as e:
        logger.error("Failed to fetch players", tournament_id=tournament_id, error=str(e))
        raise