import asyncio
from typing import Optional, List, Set
from fastapi import APIRouter, Query
from ..models.media import SearchResponse, MediaItem
from ..services.anilist_service import search_anime
from ..services.mangadex_service import search_manga, search_manhwa
from ..services.tmdb_service import search_tmdb
from ..services.games_service import search_games
from ..services.music_service import search_songs

router = APIRouter(prefix="/search", tags=["Search"])

@router.get("", response_model=SearchResponse)
async def universal_search(
    q: str = Query(..., min_length=1, description="Search term"),
    type: Optional[str] = Query("all", description="Filter by comma-separated: all, anime, manga, manhwa, tv, movie, game, song")
):
    raw_type = (type or "all").lower()
    type_tokens: Set[str] = {t.strip() for t in raw_type.split(",") if t.strip()}
    
    is_all = "all" in type_tokens or not type_tokens
    tasks = []

    limit_per_category = 15 if len(type_tokens) == 1 and not is_all else 8

    if is_all or "anime" in type_tokens:
        tasks.append(search_anime(q, limit=limit_per_category))
    if is_all or "manga" in type_tokens:
        tasks.append(search_manga(q, limit=limit_per_category))
    if is_all or "manhwa" in type_tokens:
        tasks.append(search_manhwa(q, limit=limit_per_category))
    if is_all or "tv" in type_tokens:
        tasks.append(search_tmdb(q, media_type="tv"))
    if is_all or "movie" in type_tokens:
        tasks.append(search_tmdb(q, media_type="movie"))
    if is_all or "game" in type_tokens or "games" in type_tokens:
        tasks.append(search_games(q, limit=limit_per_category))
    if is_all or "song" in type_tokens or "songs" in type_tokens or "music" in type_tokens:
        tasks.append(search_songs(q, limit=limit_per_category))

    all_batches = await asyncio.gather(*tasks, return_exceptions=True)
    
    results: List[MediaItem] = []
    seen_ids = set()
    for batch in all_batches:
        if isinstance(batch, list):
            for item in batch:
                if item.id not in seen_ids:
                    seen_ids.add(item.id)
                    results.append(item)

    return SearchResponse(
        query=q,
        mediaType=",".join(sorted(type_tokens)) if not is_all else "all",
        total=len(results),
        items=results
    )
