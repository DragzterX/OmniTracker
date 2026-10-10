from typing import List, Optional
import httpx
from ..models.media import MediaItem, MediaType
from ..services.providers import generate_provider_links
from .cache import cache

# Global Top 10 Trending Songs
GLOBAL_TRENDING_SONGS = [
    {
        "id": "itunes_dwas",
        "title": "Die With A Smile",
        "artist": "Lady Gaga & Bruno Mars",
        "score": 9.7,
        "cover": "https://is1-ssl.mzstatic.com/image/thumb/Music211/v4/bf/25/61/bf256191-c1f1-3ec9-8ea3-611979ca6324/24UM1IM11612.rgb.jpg/600x600bb.jpg",
        "genres": ["Pop", "Soul", "Ballad"],
        "desc": "A monumental soul-pop duet blending Bruno Mars' golden vocals with Lady Gaga's theatrical power.",
        "release": "Single Release",
        "rel_num": 1.0,
        "country": "US"
    },
    {
        "id": "itunes_botf",
        "title": "BIRDS OF A FEATHER",
        "artist": "Billie Eilish",
        "score": 9.6,
        "cover": "https://is1-ssl.mzstatic.com/image/thumb/Music211/v4/91/9f/6a/919f6a78-2d2f-124b-ef35-430c7e2b7a95/24UMGIM27993.rgb.jpg/600x600bb.jpg",
        "genres": ["Alternative Pop", "Indie"],
        "desc": "From 'HIT ME HARD AND SOFT', a lush, soaring pop anthem celebrating unconditional devotion.",
        "release": "Hit Me Hard and Soft",
        "rel_num": 4.0,
        "country": "US"
    },
    {
        "id": "itunes_espresso",
        "title": "Espresso",
        "artist": "Sabrina Carpenter",
        "score": 9.4,
        "cover": "https://is1-ssl.mzstatic.com/image/thumb/Music221/v4/05/cf/84/05cf84ae-024b-371d-555e-26f5fa505fc6/24UMGIM41829.rgb.jpg/600x600bb.jpg",
        "genres": ["Disco Pop", "Funk Pop"],
        "desc": "The quintessential summer disco-pop smash hit known for its sparkling bassline and infectious hooks.",
        "release": "Short n' Sweet",
        "rel_num": 1.0,
        "country": "US"
    },
    {
        "id": "itunes_nlu",
        "title": "Not Like Us",
        "artist": "Kendrick Lamar",
        "score": 9.8,
        "cover": "https://is1-ssl.mzstatic.com/image/thumb/Music221/v4/9a/e3/37/9ae33703-99b3-1cb4-0a37-56ec236b2064/24UM1IM45012.rgb.jpg/600x600bb.jpg",
        "genres": ["Hip-Hop", "West Coast Rap"],
        "desc": "Pulitzer-winner Kendrick Lamar's historic, chart-shattering West Coast anthem produced by Mustard.",
        "release": "Single Release",
        "rel_num": 1.0,
        "country": "US"
    },
    {
        "id": "itunes_taste",
        "title": "Taste",
        "artist": "Sabrina Carpenter",
        "score": 9.1,
        "cover": "https://is1-ssl.mzstatic.com/image/thumb/Music221/v4/05/cf/84/05cf84ae-024b-371d-555e-26f5fa505fc6/24UMGIM41829.rgb.jpg/600x600bb.jpg",
        "genres": ["Pop", "Alternative"],
        "desc": "Sharp wit and punchy guitars make this album opener one of the most streamed tracks worldwide.",
        "release": "Short n' Sweet",
        "rel_num": 2.0,
        "country": "US"
    },
    {
        "id": "itunes_glb",
        "title": "Good Luck, Babe!",
        "artist": "Chappell Roan",
        "score": 9.5,
        "cover": "https://is1-ssl.mzstatic.com/image/thumb/Music211/v4/d9/39/3a/d9393a56-0275-c548-ebcc-fe8944510b64/24UMGIM39281.rgb.jpg/600x600bb.jpg",
        "genres": ["Synth Pop", "80s Pop"],
        "desc": "Breakout powerhouse Chappell Roan channels Kate Bush and Cyndi Lauper in this soaring vocal triumph.",
        "release": "Single Release",
        "rel_num": 1.0,
        "country": "US"
    },
    {
        "id": "itunes_bthings",
        "title": "Beautiful Things",
        "artist": "Benson Boone",
        "score": 9.2,
        "cover": "https://is1-ssl.mzstatic.com/image/thumb/Music116/v4/fa/5e/50/fa5e5094-1a3b-fe61-9c3f-c9603ca91c7a/093624856016.jpg/600x600bb.jpg",
        "genres": ["Pop Rock", "Acoustic"],
        "desc": "A dynamic crescendo from tender acoustic reflection into full-throttle rock explosion.",
        "release": "Fireworks & Rollerblades",
        "rel_num": 1.0,
        "country": "US"
    },
    {
        "id": "itunes_ditf",
        "title": "Dancing In The Flames",
        "artist": "The Weeknd",
        "score": 9.3,
        "cover": "https://is1-ssl.mzstatic.com/image/thumb/Music211/v4/c3/b2/80/c3b280b5-7798-8e6f-ef0d-be9d7c0410ff/24UM1IM74593.rgb.jpg/600x600bb.jpg",
        "genres": ["Synthwave", "R&B"],
        "desc": "The lead single from 'Hurry Up Tomorrow' blending signature retro synthesizers with euphoric hooks.",
        "release": "Hurry Up Tomorrow",
        "rel_num": 1.0,
        "country": "CA"
    },
    {
        "id": "itunes_idol",
        "title": "Idol (アイドル)",
        "artist": "YOASOBI",
        "score": 9.6,
        "cover": "https://is1-ssl.mzstatic.com/image/thumb/Music116/v4/4e/ff/34/4eff343e-7c57-61c0-aa95-9ff0ef81fc8a/197188185856.jpg/600x600bb.jpg",
        "genres": ["J-Pop", "Anime OST"],
        "desc": "Record-breaking anime anthem for Oshi no Ko that reached #1 on the Billboard Global Excl. US chart.",
        "release": "Single Release",
        "rel_num": 1.0,
        "country": "JP"
    },
    {
        "id": "itunes_supernova",
        "title": "Supernova",
        "artist": "aespa",
        "score": 9.4,
        "cover": "https://is1-ssl.mzstatic.com/image/thumb/Music211/v4/ad/7d/df/ad7ddfb1-2a4b-9e45-f0ba-cf3b2a59e933/8809989422003.jpg/600x600bb.jpg",
        "genres": ["K-Pop", "Hyperpop", "Electropop"],
        "desc": "The hypnotic, genre-bending mega hit from aespa featuring futuristic beats and immaculate production.",
        "release": "Armageddon Album",
        "rel_num": 1.0,
        "country": "KR"
    }
]

# All-Time Top 10 Songs
GLOBAL_ALL_TIME_SONGS = [
    {
        "id": "itunes_queen_br",
        "title": "Bohemian Rhapsody",
        "artist": "Queen",
        "score": 9.9,
        "cover": "https://is1-ssl.mzstatic.com/image/thumb/Music115/v4/37/10/7c/37107c1b-f975-f350-f8ca-36e2f18579ad/00602527718029.rgb.jpg/600x600bb.jpg",
        "genres": ["Rock Opera", "Progressive Rock"],
        "desc": "Freddie Mercury's six-minute opus spanning ballad, opera, and hard rock is widely deemed the greatest song ever recorded.",
        "release": "A Night at the Opera",
        "rel_num": 1.0,
        "country": "GB"
    },
    {
        "id": "itunes_mj_bj",
        "title": "Billie Jean",
        "artist": "Michael Jackson",
        "score": 9.9,
        "cover": "https://is1-ssl.mzstatic.com/image/thumb/Music115/v4/4a/01/a0/4a01a070-df85-a77d-7888-038b3c37e5c6/074643811224.jpg/600x600bb.jpg",
        "genres": ["Pop", "Post-Disco", "Funk"],
        "desc": "Driven by the greatest bassline in music history, Michael Jackson's masterpiece redefined modern pop.",
        "release": "Thriller",
        "rel_num": 1.0,
        "country": "US"
    },
    {
        "id": "itunes_nirvana_slt",
        "title": "Smells Like Teen Spirit",
        "artist": "Nirvana",
        "score": 9.8,
        "cover": "https://is1-ssl.mzstatic.com/image/thumb/Music115/v4/4e/77/6d/4e776d65-3850-8b6b-4e67-d86b97f0a88a/00720642442524.rgb.jpg/600x600bb.jpg",
        "genres": ["Grunge", "Alternative Rock"],
        "desc": "The generational anthem that ushered alternative rock into mainstream consciousness in 1991.",
        "release": "Nevermind",
        "rel_num": 1.0,
        "country": "US"
    },
    {
        "id": "itunes_weeknd_bl",
        "title": "Blinding Lights",
        "artist": "The Weeknd",
        "score": 9.7,
        "cover": "https://is1-ssl.mzstatic.com/image/thumb/Music115/v4/6c/e0/75/6ce075d9-4b8c-529a-5431-7b06b009e99a/19UMGIM92569.rgb.jpg/600x600bb.jpg",
        "genres": ["Synthwave", "Pop"],
        "desc": "Billboard's #1 Greatest Hot 100 Hit of All Time, a relentless neon synthpop adrenaline rush.",
        "release": "After Hours",
        "rel_num": 1.0,
        "country": "CA"
    },
    {
        "id": "itunes_eagles_hc",
        "title": "Hotel California",
        "artist": "Eagles",
        "score": 9.8,
        "cover": "https://is1-ssl.mzstatic.com/image/thumb/Music115/v4/37/74/61/3774614a-115f-5136-12aa-59422df595ae/081227961602.jpg/600x600bb.jpg",
        "genres": ["Classic Rock"],
        "desc": "An allegorical masterwork with the twin-guitar solo that defined rock grandeur.",
        "release": "Hotel California",
        "rel_num": 1.0,
        "country": "US"
    },
    {
        "id": "itunes_ledzep_stair",
        "title": "Stairway to Heaven",
        "artist": "Led Zeppelin",
        "score": 9.8,
        "cover": "https://is1-ssl.mzstatic.com/image/thumb/Music115/v4/80/7e/61/807e615f-fa2c-7b44-fb4b-0143a5796245/081227965761.jpg/600x600bb.jpg",
        "genres": ["Hard Rock", "Folk Rock"],
        "desc": "Jimmy Page and Robert Plant's acoustic-to-electric crescendo that stands as rock's holy grail.",
        "release": "Led Zeppelin IV",
        "rel_num": 1.0,
        "country": "GB"
    },
    {
        "id": "itunes_lennon_img",
        "title": "Imagine",
        "artist": "John Lennon",
        "score": 9.7,
        "cover": "https://is1-ssl.mzstatic.com/image/thumb/Music115/v4/13/c6/16/13c616fc-0c0d-d4a8-f865-ec12a14ae4dc/00602567997934.rgb.jpg/600x600bb.jpg",
        "genres": ["Soft Rock", "Peace Anthem"],
        "desc": "A timeless plea for peace and humanity, anchored by John Lennon's tender piano chords.",
        "release": "Imagine",
        "rel_num": 1.0,
        "country": "GB"
    },
    {
        "id": "itunes_adele_ritd",
        "title": "Rolling in the Deep",
        "artist": "Adele",
        "score": 9.6,
        "cover": "https://is1-ssl.mzstatic.com/image/thumb/Music115/v4/c6/3f/8e/c63f8ec4-511d-ca82-df75-b3848b8cf92c/886443314541.jpg/600x600bb.jpg",
        "genres": ["Soul", "Blues Pop"],
        "desc": "Adele's thunderous stomp and unstoppable heartbreak vocals that conquered the globe.",
        "release": "21 Album",
        "rel_num": 1.0,
        "country": "GB"
    },
    {
        "id": "itunes_sheeran_soy",
        "title": "Shape of You",
        "artist": "Ed Sheeran",
        "score": 9.5,
        "cover": "https://is1-ssl.mzstatic.com/image/thumb/Music115/v4/80/7e/17/807e1744-8cb3-c1f9-f538-2d8c366ff407/190295851286.jpg/600x600bb.jpg",
        "genres": ["Pop", "Tropical House"],
        "desc": "One of the most streamed songs in Spotify history with over 4 billion plays.",
        "release": "Divide (÷)",
        "rel_num": 1.0,
        "country": "GB"
    },
    {
        "id": "itunes_fleetwood_dreams",
        "title": "Dreams",
        "artist": "Fleetwood Mac",
        "score": 9.7,
        "cover": "https://is1-ssl.mzstatic.com/image/thumb/Music115/v4/8c/d7/68/8cd768f5-9b2f-2d93-1383-74ea547565be/081227970871.jpg/600x600bb.jpg",
        "genres": ["Soft Rock", "Classic"],
        "desc": "Stevie Nicks' ethereal masterpiece that continues to captivate generations across decades.",
        "release": "Rumours",
        "rel_num": 1.0,
        "country": "US"
    }
]

# Country specific popular music charts
COUNTRY_SONGS = {
    "jp": [
        {"title": "Idol (アイドル)", "artist": "YOASOBI", "score": 9.8, "cover": "https://is1-ssl.mzstatic.com/image/thumb/Music116/v4/4e/ff/34/4eff343e-7c57-61c0-aa95-9ff0ef81fc8a/197188185856.jpg/600x600bb.jpg", "genres": ["J-Pop", "Anime"], "desc": "Record-breaking anime anthem from Oshi no Ko.", "release": "Single", "rel_num": 1.0},
        {"title": "KICK BACK", "artist": "Kenshi Yonezu", "score": 9.7, "cover": "https://placehold.co/600x600/18181b/f59e0b?text=KICK+BACK", "genres": ["J-Rock", "Anime"], "desc": "The high-voltage Chainsaw Man opening song.", "release": "Single", "rel_num": 1.0},
        {"title": "SPECIALZ", "artist": "King Gnu", "score": 9.6, "cover": "https://placehold.co/600x600/0a0d14/6366f1?text=SPECIALZ", "genres": ["Alternative Rock"], "desc": "Jujutsu Kaisen Shibuya Incident iconic opening.", "release": "Single", "rel_num": 1.0},
        {"title": "Bling-Bang-Bang-Born", "artist": "Creepy Nuts", "score": 9.5, "cover": "https://placehold.co/600x600/18181b/10b981?text=Bling-Bang", "genres": ["Hip-Hop", "Anime"], "desc": "Viral Mashle Season 2 sensation worldwide.", "release": "Single", "rel_num": 1.0},
        {"title": "Shinunoga E-Wa", "artist": "Fujii Kaze", "score": 9.5, "cover": "https://placehold.co/600x600/2a1b1b/f43f5e?text=Fujii+Kaze", "genres": ["R&B", "J-Pop"], "desc": "Soulful global viral smash hit.", "release": "HELP EVER HURT NEVER", "rel_num": 1.0},
        {"title": "Gurenge (紅蓮華)", "artist": "LiSA", "score": 9.6, "cover": "https://placehold.co/600x600/18181b/ef4444?text=Gurenge", "genres": ["J-Rock"], "desc": "Demon Slayer opening that took the world by storm.", "release": "LEO-NiNE", "rel_num": 1.0},
        {"title": "New Genesis (新時代)", "artist": "Ado", "score": 9.6, "cover": "https://placehold.co/600x600/1e1b4b/38bdf8?text=New+Genesis", "genres": ["J-Pop", "EDM"], "desc": "One Piece Film: Red theme composed by Yasutaka Nakata.", "release": "Uta's Songs", "rel_num": 1.0},
        {"title": "Subtitle", "artist": "Official HIGE DANdism", "score": 9.4, "cover": "https://placehold.co/600x600/111726/818cf8?text=Subtitle", "genres": ["J-Pop"], "desc": "Emotional winter drama ballad.", "release": "Single", "rel_num": 1.0},
        {"title": "Kaikai Kitan", "artist": "Eve", "score": 9.4, "cover": "https://placehold.co/600x600/0f172a/06b6d4?text=Eve", "genres": ["Rock", "Anime"], "desc": "Jujutsu Kaisen Season 1 opening theme.", "release": "Kaizin", "rel_num": 1.0},
        {"title": "One Last Kiss", "artist": "Hikaru Utada", "score": 9.7, "cover": "https://placehold.co/600x600/18181b/ffffff?text=Hikaru+Utada", "genres": ["Synthpop"], "desc": "Evangelion 3.0+1.0 Thrice Upon a Time theme.", "release": "EP", "rel_num": 1.0}
    ],
    "kr": [
        {"title": "Supernova", "artist": "aespa", "score": 9.6, "cover": "https://is1-ssl.mzstatic.com/image/thumb/Music211/v4/ad/7d/df/ad7ddfb1-2a4b-9e45-f0ba-cf3b2a59e933/8809989422003.jpg/600x600bb.jpg", "genres": ["K-Pop", "Hyperpop"], "desc": "Hypnotic synth lines and supreme vocals.", "release": "Armageddon", "rel_num": 1.0},
        {"title": "Chk Chk Boom", "artist": "Stray Kids", "score": 9.5, "cover": "https://placehold.co/600x600/18181b/ef4444?text=Stray+Kids", "genres": ["K-Pop", "Latin Trap"], "desc": "High energy Latin rhythm fusion.", "release": "ATE", "rel_num": 1.0},
        {"title": "Super Shy", "artist": "NewJeans", "score": 9.6, "cover": "https://placehold.co/600x600/1e293b/38bdf8?text=NewJeans", "genres": ["Jersey Club", "K-Pop"], "desc": "Breezy summer club beat that charmed the world.", "release": "Get Up", "rel_num": 1.0},
        {"title": "Dynamite", "artist": "BTS", "score": 9.7, "cover": "https://placehold.co/600x600/1e1b4b/f59e0b?text=BTS+Dynamite", "genres": ["Disco Pop"], "desc": "Historic #1 Billboard hit that sparked joy across the planet.", "release": "BE", "rel_num": 1.0},
        {"title": "How You Like That", "artist": "BLACKPINK", "score": 9.6, "cover": "https://placehold.co/600x600/2a1b1b/f43f5e?text=BLACKPINK", "genres": ["EDM", "Trap"], "desc": "Signature drop and powerhouse choreography.", "release": "THE ALBUM", "rel_num": 1.0},
        {"title": "Love Wins All", "artist": "IU", "score": 9.7, "cover": "https://placehold.co/600x600/111726/c084fc?text=IU+Love+Wins", "genres": ["Ballad"], "desc": "Cinematic vocal masterclass starring V of BTS.", "release": "The Winning", "rel_num": 1.0},
        {"title": "Magnetic", "artist": "ILLIT", "score": 9.4, "cover": "https://placehold.co/600x600/18181b/10b981?text=ILLIT", "genres": ["Pluggnb", "K-Pop"], "desc": "Dreamy viral debut that topped music charts.", "release": "SUPER REAL ME", "rel_num": 1.0},
        {"title": "Perfect Night", "artist": "LE SSERAFIM", "score": 9.4, "cover": "https://placehold.co/600x600/0f172a/818cf8?text=LE+SSERAFIM", "genres": ["2-step", "Pop"], "desc": "Smooth late-night cruising anthem.", "release": "Single", "rel_num": 1.0},
        {"title": "Super", "artist": "SEVENTEEN", "score": 9.5, "cover": "https://placehold.co/600x600/18181b/fbbf24?text=SEVENTEEN", "genres": ["K-Pop", "Trap"], "desc": "Inspired by the Monkey King Sun Wukong.", "release": "FML", "rel_num": 1.0},
        {"title": "I AM", "artist": "IVE", "score": 9.5, "cover": "https://placehold.co/600x600/18181b/ec4899?text=IVE+I+AM", "genres": ["Pop"], "desc": "Soaring chorus celebrating self-confidence.", "release": "I've IVE", "rel_num": 1.0}
    ]
}

def to_media_item(raw: dict, rank: Optional[int] = None) -> MediaItem:
    song_id = raw.get("id") or f"itunes_{raw.get('trackId', 'song')}"
    title = raw.get("title") or raw.get("trackName", "Untitled Track")
    artist = raw.get("artist") or raw.get("artistName", "Unknown Artist")
    display_title = f"{title} - {artist}" if artist and artist not in title else title
    score = float(raw.get("score", 9.0))
    cover = raw.get("cover") or raw.get("artworkUrl100", "https://placehold.co/600x600/18181b/ffffff?text=Music")
    genres = raw.get("genres", ["Music", "Pop"])
    desc = raw.get("desc", f"Stream '{title}' by {artist} on Spotify, YouTube, Apple Music, and more.")
    latest_rel = raw.get("release", "Available to Stream")
    rel_num = float(raw.get("rel_num", 1.0))
    country = raw.get("country", "US")

    providers = generate_provider_links(MediaType.SONG, f"{title} {artist}", original_id=song_id)

    return MediaItem(
        id=f"song_{song_id}",
        source="itunes",
        mediaType=MediaType.SONG,
        title=display_title,
        originalTitle=title,
        coverImage=cover,
        description=desc,
        genres=genres,
        status="completed",
        latestRelease=latest_rel,
        latestReleaseNumber=rel_num,
        officialProviders=providers,
        score=score,
        rank=rank,
        country=country
    )

async def search_songs(query: str, limit: int = 10) -> List[MediaItem]:
    cache_key = f"music_search_{query.lower()}_{limit}"
    cached = cache.get(cache_key)
    if cached:
        return cached

    results: List[MediaItem] = []

    # 1. Live search via iTunes Search API (completely free, no API key required)
    try:
        url = "https://itunes.apple.com/search"
        params = {
            "term": query,
            "entity": "song",
            "limit": limit
        }
        async with httpx.AsyncClient(timeout=6.0) as client:
            resp = await client.get(url, params=params)
            if resp.status_code == 200:
                data = resp.json()
                items = data.get("results", [])
                for item in items:
                    track_name = item.get("trackName", "")
                    artist_name = item.get("artistName", "")
                    collection = item.get("collectionName", "")
                    track_id = str(item.get("trackId", ""))
                    artwork = item.get("artworkUrl100", "")
                    if artwork:
                        artwork = artwork.replace("100x100bb", "600x600bb")

                    genre = item.get("primaryGenreName", "Music")
                    display_title = f"{track_name} - {artist_name}"

                    providers = generate_provider_links(MediaType.SONG, f"{track_name} {artist_name}", original_id=f"itunes_{track_id}")

                    results.append(MediaItem(
                        id=f"song_itunes_{track_id}",
                        source="itunes",
                        mediaType=MediaType.SONG,
                        title=display_title,
                        originalTitle=track_name,
                        coverImage=artwork or "https://placehold.co/600x600/18181b/ffffff?text=Music",
                        description=f"From the album '{collection}'. Stream '{track_name}' by {artist_name} across music platforms.",
                        genres=[genre, "Single"],
                        status="completed",
                        latestRelease="Available Now",
                        latestReleaseNumber=1.0,
                        officialProviders=providers,
                        score=9.0
                    ))
    except Exception as exc:
        print(f"iTunes API query error: {exc}")

    # Fallback to curated match if needed
    if len(results) < limit:
        q_lower = query.lower()
        all_curated = GLOBAL_TRENDING_SONGS + GLOBAL_ALL_TIME_SONGS
        for item in all_curated:
            if q_lower in item["title"].lower() or q_lower in item["artist"].lower():
                if not any(item["title"].lower() in r.title.lower() for r in results):
                    results.append(to_media_item(item))

    cache.set(cache_key, results, ttl=60)
    return results[:limit]

async def get_top_songs(mode: str = "trending", country: str = "global", limit: int = 10) -> List[MediaItem]:
    cache_key = f"music_top_{mode}_{country.lower()}_{limit}"
    cached = cache.get(cache_key)
    if cached:
        return cached

    c_lower = country.lower()
    items: List[dict] = []

    if c_lower in COUNTRY_SONGS and COUNTRY_SONGS[c_lower]:
        items = COUNTRY_SONGS[c_lower]
    elif mode == "top_rated":
        items = GLOBAL_ALL_TIME_SONGS
    else:
        items = GLOBAL_TRENDING_SONGS

    results = [to_media_item(item, rank=idx + 1) for idx, item in enumerate(items[:limit])]
    cache.set(cache_key, results, ttl=60)
    return results
