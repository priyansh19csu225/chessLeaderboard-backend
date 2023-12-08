from fastapi import APIRouter, HTTPException , Response , Depends
from app.services import get_top_players,fetch_player_rating_history , generate_50_players_ratings_csv
from app.db import get_db
from cachetools.func import TTLCache
from sqlalchemy.orm import Session

router = APIRouter()
csv_content_cache = TTLCache(maxsize=1, ttl=3600)

@router.get("/top-players")
async def top_players():
    players_data = await get_top_players()
    if not players_data:
        raise HTTPException(status_code=500, detail="Failed to fetch players data")    
    return players_data

@router.get("/player/{username}/rating-history")
async def get_player_rating_history(username: str,db: Session = Depends(get_db)):
    rating_history = await fetch_player_rating_history(username,db)

    if not rating_history:
        raise HTTPException(status_code=404, detail="Player rating history for 30 days not found")
    
    return rating_history


async def cached_generate_rating_history_csv(db):
    if 'csv_content' not in csv_content_cache:
        top_50_players = await get_top_players()
        if not top_50_players:
            raise HTTPException(status_code=404, detail="Top 50 classical players not found")
        
        csv_content_cache['csv_content'] = await generate_50_players_ratings_csv(top_50_players,db)
    return csv_content_cache['csv_content']


@router.get("/players/rating-history-csv")
async def generate_rating_history_csv(db: Session = Depends(get_db)):
    csv_content = await cached_generate_rating_history_csv(db)

    response = Response(content=csv_content, media_type="text/csv")
    response.headers["Content-Disposition"] = 'attachment; filename="rating_history.csv"'

    return response