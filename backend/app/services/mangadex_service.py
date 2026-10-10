from typing import List, Optional
import httpx
from ..core.config import settings
from ..models.media import MediaItem, MediaType
from .cache import cache
from .providers import generate_provider_links

# Curated fallback/ranking data for Manga
TOP_TRENDING_MANGA = [
    {"id": "manga_op", "title": "One Piece", "score": 9.7, "cover": "https://placehold.co/400x600/18181b/f59e0b?text=One+Piece", "genres": ["Adventure", "Fantasy"], "desc": "Monkey D. Luffy sails the Grand Line in search of the legendary treasure.", "release": "Chapter 1130", "rel_num": 1130.0, "country": "JP"},
    {"id": "manga_jjk", "title": "Jujutsu Kaisen", "score": 9.3, "cover": "https://placehold.co/400x600/0a0d14/6366f1?text=Jujutsu+Kaisen", "genres": ["Action", "Supernatural"], "desc": "Yuji Itadori swallows a cursed finger and enters the lethal world of Jujutsu Sorcery.", "release": "Chapter 271 (Finale)", "rel_num": 271.0, "country": "JP"},
    {"id": "manga_csm", "title": "Chainsaw Man", "score": 9.2, "cover": "https://placehold.co/400x600/18181b/ef4444?text=Chainsaw+Man", "genres": ["Action", "Dark Fantasy"], "desc": "Denji lives as a devil hunter alongside Pochita in a world ravaged by fears.", "release": "Chapter 180", "rel_num": 180.0, "country": "JP"},
    {"id": "manga_berserk", "title": "Berserk", "score": 9.8, "cover": "https://placehold.co/400x600/18181b/38bdf8?text=Berserk", "genres": ["Dark Fantasy", "Tragedy"], "desc": "The Black Swordsman Guts brandishes the Dragonslayer against cosmic apostles.", "release": "Chapter 376", "rel_num": 376.0, "country": "JP"},
    {"id": "manga_spx", "title": "Spy x Family", "score": 9.1, "cover": "https://placehold.co/400x600/18181b/10b981?text=Spy+x+Family", "genres": ["Comedy", "Action"], "desc": "A master spy, an assassin, and a telepathic orphan form a secret fake family.", "release": "Chapter 105", "rel_num": 105.0, "country": "JP"},
    {"id": "manga_dandadan", "title": "Dandadan", "score": 9.4, "cover": "https://placehold.co/400x600/111726/c084fc?text=Dandadan", "genres": ["Sci-Fi", "Supernatural", "Comedy"], "desc": "Ghosts, aliens, and romance collide in frantic supernatural escapades.", "release": "Chapter 170", "rel_num": 170.0, "country": "JP"},
    {"id": "manga_sakamoto", "title": "Sakamoto Days", "score": 9.3, "cover": "https://placehold.co/400x600/18181b/f43f5e?text=Sakamoto+Days", "genres": ["Action", "Comedy"], "desc": "The ultimate legendary hitman retires to run a local convenience store.", "release": "Chapter 185", "rel_num": 185.0, "country": "JP"},
    {"id": "manga_mha", "title": "My Hero Academia", "score": 8.9, "cover": "https://placehold.co/400x600/1e293b/38bdf8?text=MHA", "genres": ["Superhero", "Action"], "desc": "Izuku Midoriya inherits One For All in a world where everyone possesses Quirks.", "release": "Chapter 430 (Finale)", "rel_num": 430.0, "country": "JP"},
    {"id": "manga_bluebox", "title": "Blue Box", "score": 9.0, "cover": "https://placehold.co/400x600/0f172a/818cf8?text=Blue+Box", "genres": ["Romance", "Sports"], "desc": "Badminton and basketball intertwine in this delicate high school sports romance.", "release": "Chapter 168", "rel_num": 168.0, "country": "JP"},
    {"id": "manga_kagurabachi", "title": "Kagurabachi", "score": 9.2, "cover": "https://placehold.co/400x600/18181b/fbbf24?text=Kagurabachi", "genres": ["Action", "Supernatural"], "desc": "Armed with enchanted katana forged by his late father, Chihiro seeks retribution.", "release": "Chapter 55", "rel_num": 55.0, "country": "JP"}
]

# Curated fallback/ranking data for Manhwa
TOP_TRENDING_MANHWA = [
    {"id": "manhwa_sl", "title": "Solo Leveling: Ragnarok", "score": 9.6, "cover": "https://placehold.co/400x600/0a0d14/38bdf8?text=Solo+Leveling", "genres": ["Action", "Fantasy", "System"], "desc": "Sung Su-ho inherits the monarch power of his father, the Shadow Monarch.", "release": "Chapter 36", "rel_num": 36.0, "country": "KR"},
    {"id": "manhwa_orv", "title": "Omniscient Reader's Viewpoint", "score": 9.7, "cover": "https://placehold.co/400x600/111726/6366f1?text=ORV", "genres": ["Apocalypse", "Fantasy", "Psychological"], "desc": "Kim Dokja was the only reader who finished the web novel. Then the world became it.", "release": "Chapter 230", "rel_num": 230.0, "country": "KR"},
    {"id": "manhwa_tbate", "title": "The Beginning After the End", "score": 9.4, "cover": "https://placehold.co/400x600/18181b/f59e0b?text=TBATE", "genres": ["Isekai", "Magic", "Action"], "desc": "King Grey is reborn into a magical new world filled with monsters and wonders.", "release": "Chapter 190", "rel_num": 190.0, "country": "KR"},
    {"id": "manhwa_nano", "title": "Nano Machine", "score": 9.3, "cover": "https://placehold.co/400x600/18181b/10b981?text=Nano+Machine", "genres": ["Murim", "Sci-Fi", "Action"], "desc": "Cheon Yeo-woon receives a nanotech injection from a future descendant.", "release": "Chapter 226", "rel_num": 226.0, "country": "KR"},
    {"id": "manhwa_tower", "title": "Tower of God", "score": 9.5, "cover": "https://placehold.co/400x600/1e293b/38bdf8?text=Tower+of+God", "genres": ["Fantasy", "Mystery", "Action"], "desc": "What do you desire? Climb the Tower to attain whatever you wish.", "release": "Season 3 Chapter 212", "rel_num": 630.0, "country": "KR"},
    {"id": "manhwa_lookism", "title": "Lookism", "score": 9.2, "cover": "https://placehold.co/400x600/18181b/f43f5e?text=Lookism", "genres": ["Action", "Martial Arts", "Drama"], "desc": "Park Hyung Suk wakes up in a second, tall and incredibly handsome body.", "release": "Chapter 520", "rel_num": 520.0, "country": "KR"},
    {"id": "manhwa_estate", "title": "The Greatest Estate Developer", "score": 9.7, "cover": "https://placehold.co/400x600/18181b/fbbf24?text=Estate+Dev", "genres": ["Comedy", "Fantasy", "Kingdom Building"], "desc": "Civil engineering student wakes up in a fantasy noble family deeply in debt.", "release": "Chapter 160", "rel_num": 160.0, "country": "KR"},
    {"id": "manhwa_mount_hua", "title": "Return of the Blossoming Blade", "score": 9.6, "cover": "https://placehold.co/400x600/111726/ec4899?text=Mount+Hua", "genres": ["Murim", "Comedy", "Martial Arts"], "desc": "Chung Myung, the Plum Blossom Sword Saint, wakes up a century later to revive his sect.", "release": "Chapter 142", "rel_num": 142.0, "country": "KR"},
    {"id": "manhwa_sss", "title": "SSS-Class Suicide Hunter", "score": 9.5, "cover": "https://placehold.co/400x600/0f172a/818cf8?text=Suicide+Hunter", "genres": ["Tower", "Psychological", "Action"], "desc": "Gong-ja copies the skill of anyone who kills him, but dies in the process.", "release": "Chapter 115", "rel_num": 115.0, "country": "KR"},
    {"id": "manhwa_mercenary", "title": "Teenage Mercenary", "score": 9.2, "cover": "https://placehold.co/400x600/18181b/ffffff?text=Teen+Mercenary", "genres": ["Action", "Military", "School"], "desc": "Sole survivor of an airplane crash returns home after years as an elite mercenary.", "release": "Chapter 205", "rel_num": 205.0, "country": "KR"}
]

def extract_title(attributes: dict) -> str:
    titles = attributes.get("title", {}) or {}
    if "en" in titles:
        return titles["en"]
    if titles:
        return next(iter(titles.values()))
    alt_titles = attributes.get("altTitles", []) or []
    for alt in alt_titles:
        if "en" in alt:
            return alt["en"]
    return "Untitled Comic"

def extract_cover_filename(relationships: list) -> Optional[str]:
    for rel in relationships:
        if rel.get("type") == "cover_art":
            return rel.get("attributes", {}).get("fileName")
    return None

def normalize_mangadex_manga(item: dict, forced_type: Optional[MediaType] = None) -> MediaItem:
    manga_id = item.get("id", "")
    attributes = item.get("attributes", {}) or {}
    relationships = item.get("relationships", []) or []
    
    title = extract_title(attributes)
    orig_lang = attributes.get("originalLanguage", "ja").lower()

    if forced_type:
        media_type = forced_type
    elif orig_lang == "ko":
        media_type = MediaType.MANHWA
    elif orig_lang in ("zh", "zh-hk"):
        media_type = MediaType.MANHWA
    else:
        media_type = MediaType.MANGA
        
    country_code = "KR" if orig_lang == "ko" else ("CN" if orig_lang in ("zh", "zh-hk") else "JP")
    
    cover_file = extract_cover_filename(relationships)
    cover_url = f"https://uploads.mangadex.org/covers/{manga_id}/{cover_file}.512.jpg" if cover_file else "https://placehold.co/400x600/18181b/ffffff?text=No+Cover"
    
    desc_map = attributes.get("description", {}) or {}
    desc = desc_map.get("en") or (next(iter(desc_map.values())) if desc_map else "")
    if len(desc) > 400:
        desc = desc[:397] + "..."
        
    genres = []
    for tag in attributes.get("tags", []):
        name = tag.get("attributes", {}).get("name", {}).get("en")
        if name:
            genres.append(name)
            
    status_raw = attributes.get("status", "ongoing")
    status = "completed" if status_raw == "completed" else "ongoing"
    
    last_chapter_str = attributes.get("lastChapter")
    latest_num = 0.0
    latest_release = "Ongoing"
    if last_chapter_str:
        try:
            latest_num = float(last_chapter_str)
            latest_release = f"Chapter {last_chapter_str}"
        except ValueError:
            latest_release = f"Chapter {last_chapter_str}"
            
    providers = generate_provider_links(media_type, title, original_id=f"mangadex_{manga_id}")
    
    return MediaItem(
        id=f"mangadex_{manga_id}",
        source="mangadex",
        mediaType=media_type,
        title=title,
        coverImage=cover_url,
        description=desc,
        genres=genres[:5],
        status=status,
        latestRelease=latest_release,
        latestReleaseNumber=latest_num,
        totalReleases=int(latest_num) if latest_num > 0 and status == "completed" else None,
        officialProviders=providers,
        score=9.1,
        country=country_code
    )

def to_curated_item(raw: dict, media_type: MediaType, rank: Optional[int] = None) -> MediaItem:
    title = raw["title"]
    providers = generate_provider_links(media_type, title, original_id=raw["id"])
    return MediaItem(
        id=f"{media_type.value}_{raw['id']}",
        source="mangadex",
        mediaType=media_type,
        title=title,
        coverImage=raw["cover"],
        description=raw["desc"],
        genres=raw["genres"],
        status="ongoing",
        latestRelease=raw["release"],
        latestReleaseNumber=raw["rel_num"],
        officialProviders=providers,
        score=raw["score"],
        rank=rank,
        country=raw.get("country", "JP" if media_type == MediaType.MANGA else "KR")
    )

async def search_manga_or_manhwa(query: str, category: str = "all", limit: int = 10) -> List[MediaItem]:
    cache_key = f"mangadex_search_{category}_{query}_{limit}"
    cached = cache.get(cache_key)
    if cached:
        return cached

    url = f"{settings.MANGADEX_BASE_URL}/manga"
    params = [
        ("title", query),
        ("limit", str(limit)),
        ("includes[]", "cover_art"),
        ("contentRating[]", "safe"),
        ("contentRating[]", "suggestive"),
        ("order[relevance]", "desc")
    ]

    if category == "manga":
        params.append(("originalLanguage[]", "ja"))
    elif category == "manhwa":
        params.append(("originalLanguage[]", "ko"))

    results: List[MediaItem] = []
    try:
        async with httpx.AsyncClient(timeout=8.0) as client:
            response = await client.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                data_list = data.get("data", [])
                results = [normalize_mangadex_manga(item) for item in data_list]
    except Exception as exc:
        print(f"Error fetching from MangaDex: {exc}")

    # Fallback to curated if empty
    if not results:
        pool = TOP_TRENDING_MANGA if category == "manga" else (TOP_TRENDING_MANHWA if category == "manhwa" else TOP_TRENDING_MANGA + TOP_TRENDING_MANHWA)
        q_lower = query.lower()
        for c in pool:
            if q_lower in c["title"].lower():
                m_type = MediaType.MANGA if c in TOP_TRENDING_MANGA else MediaType.MANHWA
                results.append(to_curated_item(c, m_type))

    cache.set(cache_key, results, ttl=60)
    return results

async def search_manga(query: str, limit: int = 10) -> List[MediaItem]:
    return await search_manga_or_manhwa(query, category="manga", limit=limit)

async def search_manhwa(query: str, limit: int = 10) -> List[MediaItem]:
    return await search_manga_or_manhwa(query, category="manhwa", limit=limit)

async def get_popular_manga(limit: int = 10) -> List[MediaItem]:
    return await get_top_manga(mode="trending", limit=limit)

async def get_top_manga(mode: str = "trending", country: str = "global", limit: int = 10) -> List[MediaItem]:
    cache_key = f"manga_top_{mode}_{country.lower()}_{limit}"
    cached = cache.get(cache_key)
    if cached:
        return cached

    # Attempt to query MangaDex for top manga
    order_key = "followedCount" if mode == "top_rated" else "rating"
    url = f"{settings.MANGADEX_BASE_URL}/manga"
    params = [
        ("limit", str(limit)),
        ("includes[]", "cover_art"),
        ("originalLanguage[]", "ja"),
        ("contentRating[]", "safe"),
        ("contentRating[]", "suggestive"),
        (f"order[{order_key}]", "desc")
    ]
    results: List[MediaItem] = []
    try:
        async with httpx.AsyncClient(timeout=8.0) as client:
            resp = await client.get(url, params=params)
            if resp.status_code == 200:
                data = resp.json().get("data", [])
                for idx, item in enumerate(data):
                    norm = normalize_mangadex_manga(item, forced_type=MediaType.MANGA)
                    norm.rank = idx + 1
                    results.append(norm)
    except Exception as exc:
        print(f"MangaDex top error: {exc}")

    if len(results) < limit:
        results = [to_curated_item(item, MediaType.MANGA, rank=idx + 1) for idx, item in enumerate(TOP_TRENDING_MANGA[:limit])]

    cache.set(cache_key, results, ttl=60)
    return results[:limit]

async def get_top_manhwa(mode: str = "trending", country: str = "global", limit: int = 10) -> List[MediaItem]:
    cache_key = f"manhwa_top_{mode}_{country.lower()}_{limit}"
    cached = cache.get(cache_key)
    if cached:
        return cached

    order_key = "followedCount" if mode == "top_rated" else "rating"
    url = f"{settings.MANGADEX_BASE_URL}/manga"
    params = [
        ("limit", str(limit)),
        ("includes[]", "cover_art"),
        ("originalLanguage[]", "ko"),
        ("contentRating[]", "safe"),
        ("contentRating[]", "suggestive"),
        (f"order[{order_key}]", "desc")
    ]
    results: List[MediaItem] = []
    try:
        async with httpx.AsyncClient(timeout=8.0) as client:
            resp = await client.get(url, params=params)
            if resp.status_code == 200:
                data = resp.json().get("data", [])
                for idx, item in enumerate(data):
                    norm = normalize_mangadex_manga(item, forced_type=MediaType.MANHWA)
                    norm.rank = idx + 1
                    results.append(norm)
    except Exception as exc:
        print(f"MangaDex manhwa top error: {exc}")

    if len(results) < limit:
        results = [to_curated_item(item, MediaType.MANHWA, rank=idx + 1) for idx, item in enumerate(TOP_TRENDING_MANHWA[:limit])]

    cache.set(cache_key, results, ttl=60)
    return results[:limit]
