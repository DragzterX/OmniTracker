from datetime import datetime, timezone
from typing import List, Optional
import httpx
from ..core.config import settings
from ..models.media import MediaItem, MediaType
from .cache import cache
from .providers import generate_provider_links

ANILIST_SEARCH_QUERY = """
query ($search: String, $page: Int, $perPage: Int) {
  Page(page: $page, perPage: $perPage) {
    media(search: $search, type: ANIME) {
      id
      title {
        romaji
        english
        native
      }
      coverImage {
        extraLarge
        large
      }
      bannerImage
      description(asHtml: false)
      genres
      status
      episodes
      nextAiringEpisode {
        airingAt
        timeUntilAiring
        episode
      }
      averageScore
      siteUrl
    }
  }
}
"""

ANILIST_TRENDING_QUERY = """
query ($page: Int, $perPage: Int) {
  Page(page: $page, perPage: $perPage) {
    media(type: ANIME, sort: TRENDING_DESC) {
      id
      title {
        romaji
        english
        native
      }
      coverImage {
        extraLarge
        large
      }
      bannerImage
      description(asHtml: false)
      genres
      status
      episodes
      nextAiringEpisode {
        airingAt
        timeUntilAiring
        episode
      }
      averageScore
      siteUrl
    }
  }
}
"""

ANILIST_TOP_RATED_QUERY = """
query ($page: Int, $perPage: Int) {
  Page(page: $page, perPage: $perPage) {
    media(type: ANIME, sort: [SCORE_DESC, POPULARITY_DESC]) {
      id
      title {
        romaji
        english
        native
      }
      coverImage {
        extraLarge
        large
      }
      bannerImage
      description(asHtml: false)
      genres
      status
      episodes
      nextAiringEpisode {
        airingAt
        timeUntilAiring
        episode
      }
      averageScore
      siteUrl
    }
  }
}
"""

# Static emergency fallback list (used strictly if AniList API is offline)
CURATED_TOP_ANIME = [
    {"id": "anilist_5114", "title": "Fullmetal Alchemist: Brotherhood", "score": 9.9, "cover": "https://placehold.co/400x600/18181b/f59e0b?text=FMAB", "genres": ["Action", "Adventure", "Fantasy"], "desc": "Edward and Alphonse Elric search for the Philosopher's Stone to restore their bodies.", "release": "Episode 64 (Finale)", "rel_num": 64.0},
    {"id": "anilist_16498", "title": "Attack on Titan", "score": 9.8, "cover": "https://placehold.co/400x600/0a0d14/ef4444?text=Attack+on+Titan", "genres": ["Action", "Mystery", "Drama"], "desc": "Eren Jaeger vows to eradicate humanity's monstrous predators after his home is breached.", "release": "The Final Chapters", "rel_num": 89.0},
    {"id": "anilist_145064", "title": "Jujutsu Kaisen Season 2", "score": 9.7, "cover": "https://placehold.co/400x600/111726/6366f1?text=Jujutsu+Kaisen", "genres": ["Action", "Supernatural"], "desc": "The past of Satoru Gojo and the catastrophic Shibuya Incident unfold.", "release": "Episode 23 (Finale)", "rel_num": 47.0},
    {"id": "anilist_154587", "title": "Frieren: Beyond Journey's End", "score": 9.8, "cover": "https://placehold.co/400x600/18181b/38bdf8?text=Frieren", "genres": ["Adventure", "Fantasy"], "desc": "An elven mage reflects on human connections after defeating the Demon King.", "release": "Episode 28 (Finale)", "rel_num": 28.0},
    {"id": "anilist_113415", "title": "Jujutsu Kaisen", "score": 9.5, "cover": "https://placehold.co/400x600/1e293b/818cf8?text=JJK+S1", "genres": ["Action", "Fantasy"], "desc": "A boy with immense physical strength swallowed Ryomen Sukuna's cursed finger.", "release": "Episode 24 (Finale)", "rel_num": 24.0}
]

def normalize_anilist_media(raw: dict, rank: Optional[int] = None) -> MediaItem:
    title_data = raw.get("title", {}) or {}
    title = title_data.get("english") or title_data.get("romaji") or title_data.get("native") or "Untitled Anime"
    original_title = title_data.get("native")
    
    cover_data = raw.get("coverImage", {}) or {}
    cover_image = cover_data.get("extraLarge") or cover_data.get("large") or ""
    banner_image = raw.get("bannerImage")
    
    raw_status = (raw.get("status") or "RELEASING").upper()
    status_map = {
        "RELEASING": "ongoing",
        "FINISHED": "completed",
        "NOT_YET_RELEASED": "upcoming",
        "CANCELLED": "completed",
        "HIATUS": "hiatus"
    }
    status = status_map.get(raw_status, "ongoing")
    
    total_episodes = raw.get("episodes")
    next_airing = raw.get("nextAiringEpisode")
    
    latest_release = ""
    latest_num = 0.0
    next_release_date = None
    
    if next_airing:
        next_ep = next_airing.get("episode", 1)
        latest_num = max(0.0, float(next_ep - 1))
        latest_release = f"Episode {int(latest_num)}" if latest_num > 0 else "Premiere Upcoming"
        airing_at = next_airing.get("airingAt")
        if airing_at:
            next_release_date = datetime.fromtimestamp(airing_at, tz=timezone.utc).isoformat()
    elif status == "completed" and total_episodes:
        latest_num = float(total_episodes)
        latest_release = f"Episode {total_episodes} (Finale)"
    elif total_episodes:
        latest_num = float(total_episodes)
        latest_release = f"Episode {total_episodes}"
    else:
        latest_release = "Airing"
    
    providers = generate_provider_links(MediaType.ANIME, title, original_id=f"anilist_{raw.get('id')}")

    desc = raw.get("description") or ""
    desc = desc.replace("<br>", "\n").replace("<i>", "").replace("</i>", "")
    if len(desc) > 400:
        desc = desc[:397] + "..."

    score_val = raw.get("averageScore")
    score = float(score_val) / 10.0 if score_val else None

    return MediaItem(
        id=f"anilist_{raw.get('id')}",
        source="anilist",
        mediaType=MediaType.ANIME,
        title=title,
        originalTitle=original_title,
        coverImage=cover_image or "https://placehold.co/400x600/18181b/ffffff?text=Anime",
        bannerImage=banner_image,
        description=desc,
        genres=raw.get("genres", []) or [],
        status=status,
        latestRelease=latest_release,
        latestReleaseNumber=latest_num,
        latestReleaseDate=None,
        nextReleaseDate=next_release_date,
        totalReleases=total_episodes,
        officialProviders=providers,
        score=score,
        rank=rank,
        country="JP"
    )

async def search_anime(query: str, limit: int = 10) -> List[MediaItem]:
    clean_query = query.strip()
    if not clean_query:
        return []

    cache_key = f"anilist_search_{clean_query.lower()}_{limit}"
    cached = cache.get(cache_key)
    if cached:
        return cached

    graphql_url = getattr(settings, "ANILIST_GRAPHQL_URL", "https://graphql.anilist.co") or "https://graphql.anilist.co"

    payload = {
        "query": ANILIST_SEARCH_QUERY,
        "variables": {"search": clean_query, "page": 1, "perPage": limit}
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                graphql_url, 
                json=payload, 
                headers={"Content-Type": "application/json", "Accept": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                media_list = data.get("data", {}).get("Page", {}).get("media", [])
                results = [normalize_anilist_media(m) for m in media_list]
                
                if results:
                    cache.set(cache_key, results, ttl=60)
                    return results
            else:
                print(f"AniList Search HTTP {response.status_code}: {response.text}")
    except Exception as exc:
        print(f"Error fetching search from AniList: {exc}")
    
    # Emergency fallback match
    q_lower = clean_query.lower()
    q_words = [w for w in q_lower.split() if len(w) > 2]
    
    matches = []
    for c in CURATED_TOP_ANIME:
        title_lower = c["title"].lower()
        if q_lower in title_lower or any(w in title_lower for w in q_words):
            matches.append(
                MediaItem(
                    id=c["id"],
                    source="anilist",
                    mediaType=MediaType.ANIME,
                    title=c["title"],
                    coverImage=c["cover"],
                    description=c["desc"],
                    genres=c["genres"],
                    status="ongoing",
                    latestRelease=c["release"],
                    latestReleaseNumber=c["rel_num"],
                    officialProviders=generate_provider_links(MediaType.ANIME, c["title"], original_id=c["id"]),
                    score=c["score"],
                    country="JP"
                )
            )
            
    return matches[:limit]

async def get_trending_anime(limit: int = 12) -> List[MediaItem]:
    return await get_top_anime(mode="trending", limit=limit)

async def get_top_anime(mode: str = "trending", country: str = "global", limit: int = 10) -> List[MediaItem]:
    cache_key = f"anilist_top_{mode}_{country.lower()}_{limit}"
    cached = cache.get(cache_key)
    if cached:
        return cached

    graphql_url = getattr(settings, "ANILIST_GRAPHQL_URL", "https://graphql.anilist.co") or "https://graphql.anilist.co"
    query_str = ANILIST_TOP_RATED_QUERY if mode == "top_rated" else ANILIST_TRENDING_QUERY
    payload = {
        "query": query_str,
        "variables": {"page": 1, "perPage": limit}
    }

    results: List[MediaItem] = []
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                graphql_url, 
                json=payload, 
                headers={"Content-Type": "application/json", "Accept": "application/json"}
            )
            if response.status_code == 200:
                data = response.json()
                media_list = data.get("data", {}).get("Page", {}).get("media", [])
                for idx, m in enumerate(media_list):
                    results.append(normalize_anilist_media(m, rank=idx + 1))
            else:
                print(f"AniList Top/Trending HTTP {response.status_code}: {response.text}")
    except Exception as exc:
        print(f"Error fetching top anime from AniList: {exc}")

    # FIX: Only fallback to curated data if the live API returned NO results at all
    if not results:
        results = [
            MediaItem(
                id=c["id"],
                source="anilist",
                mediaType=MediaType.ANIME,
                title=c["title"],
                coverImage=c["cover"],
                description=c["desc"],
                genres=c["genres"],
                status="ongoing",
                latestRelease=c["release"],
                latestReleaseNumber=c["rel_num"],
                officialProviders=generate_provider_links(MediaType.ANIME, c["title"], original_id=c["id"]),
                score=c["score"],
                rank=idx + 1,
                country="JP"
            )
            for idx, c in enumerate(CURATED_TOP_ANIME[:limit])
        ]

    # Set cache with 5-minute TTL so trending lists update regularly
    cache.set(cache_key, results, ttl=300)
    return results[:limit]