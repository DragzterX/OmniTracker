import asyncio
from typing import Optional, List, Dict, Any, Set
from fastapi import APIRouter, Query
from pydantic import BaseModel
from ..models.media import MediaItem
from ..services.anilist_service import get_top_anime
from ..services.mangadex_service import get_top_manga, get_top_manhwa
from ..services.tmdb_service import get_top_tmdb
from ..services.games_service import get_top_games
from ..services.music_service import get_top_songs

router = APIRouter(tags=["Recommendations & Rankings"])

class RankingsResponse(BaseModel):
    mode: str
    country: str
    anime: List[MediaItem]
    tv: List[MediaItem]
    movie: List[MediaItem]
    manga: List[MediaItem]
    manhwa: List[MediaItem]
    game: List[MediaItem]
    song: List[MediaItem]

@router.get("/rankings", response_model=RankingsResponse)
async def get_all_rankings(
    mode: str = Query("trending", description="Ranking mode: trending or top_rated"),
    country: str = Query("global", description="Country code e.g. global, jp, kr, us, gb, fr, de")
):
    selected_mode = mode.lower() if mode in ("trending", "top_rated") else "trending"
    selected_country = country.lower()

    # Fetch Top 10 for each category concurrently
    anime_task = get_top_anime(mode=selected_mode, country=selected_country, limit=10)
    tv_task = get_top_tmdb(media_type="tv", mode=selected_mode, country=selected_country, limit=10)
    movie_task = get_top_tmdb(media_type="movie", mode=selected_mode, country=selected_country, limit=10)
    manga_task = get_top_manga(mode=selected_mode, country=selected_country, limit=10)
    manhwa_task = get_top_manhwa(mode=selected_mode, country=selected_country, limit=10)
    game_task = get_top_games(mode=selected_mode, country=selected_country, limit=10)
    song_task = get_top_songs(mode=selected_mode, country=selected_country, limit=10)

    results = await asyncio.gather(
        anime_task, tv_task, movie_task, manga_task, manhwa_task, game_task, song_task,
        return_exceptions=True
    )

    def extract(idx: int) -> List[MediaItem]:
        res = results[idx]
        return res if isinstance(res, list) else []

    return RankingsResponse(
        mode=selected_mode,
        country=selected_country,
        anime=extract(0),
        tv=extract(1),
        movie=extract(2),
        manga=extract(3),
        manhwa=extract(4),
        game=extract(5),
        song=extract(6)
    )

@router.get("/recommendations", response_model=List[MediaItem])
async def get_recommendations(
    type: Optional[str] = Query("all", description="Media type filter: comma-separated or single"),
    mode: str = Query("trending", description="Ranking mode: trending or top_rated"),
    country: str = Query("global", description="Country filter: global, jp, kr, us, etc.")
):
    raw_type = (type or "all").lower()
    type_tokens: Set[str] = {t.strip() for t in raw_type.split(",") if t.strip()}
    is_all = "all" in type_tokens or not type_tokens

    selected_mode = mode.lower() if mode in ("trending", "top_rated") else "trending"
    selected_country = country.lower()

    tasks = []
    if is_all or "anime" in type_tokens:
        tasks.append(get_top_anime(mode=selected_mode, country=selected_country, limit=10))
    if is_all or "manga" in type_tokens:
        tasks.append(get_top_manga(mode=selected_mode, country=selected_country, limit=10))
    if is_all or "manhwa" in type_tokens:
        tasks.append(get_top_manhwa(mode=selected_mode, country=selected_country, limit=10))
    if is_all or "tv" in type_tokens:
        tasks.append(get_top_tmdb(media_type="tv", mode=selected_mode, country=selected_country, limit=10))
    if is_all or "movie" in type_tokens:
        tasks.append(get_top_tmdb(media_type="movie", mode=selected_mode, country=selected_country, limit=10))
    if is_all or "game" in type_tokens or "games" in type_tokens:
        tasks.append(get_top_games(mode=selected_mode, country=selected_country, limit=10))
    if is_all or "song" in type_tokens or "songs" in type_tokens or "music" in type_tokens:
        tasks.append(get_top_songs(mode=selected_mode, country=selected_country, limit=10))

    batches = await asyncio.gather(*tasks, return_exceptions=True)
    combined: List[MediaItem] = []
    for b in batches:
        if isinstance(b, list):
            combined.extend(b)

    return combined
