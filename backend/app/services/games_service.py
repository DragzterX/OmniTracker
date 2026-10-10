from typing import List, Optional
import httpx
from ..models.media import MediaItem, MediaType
from ..services.providers import generate_provider_links
from .cache import cache

# Global Top 10 Trending Games
GLOBAL_TRENDING_GAMES = [
    {
        "id": "steam_1245620",
        "title": "Elden Ring: Shadow of the Erdtree",
        "score": 9.5,
        "cover": "https://cdn.akamai.steamstatic.com/steam/apps/1245620/header.jpg",
        "genres": ["Action RPG", "Open World", "Dark Fantasy"],
        "desc": "Guided by Empyrean Miquella, players explore the Realm of Shadow filled with mystery and perilous dungeons.",
        "release": "Latest Update 1.14",
        "rel_num": 1.14,
        "country": "JP"
    },
    {
        "id": "steam_2358720",
        "title": "Black Myth: Wukong",
        "score": 9.2,
        "cover": "https://cdn.akamai.steamstatic.com/steam/apps/2358720/header.jpg",
        "genres": ["Action", "Mythology", "Souls-like"],
        "desc": "An action RPG rooted in Chinese mythology where you set out as the Destined One to uncover the truth.",
        "release": "Patch 1.0.9",
        "rel_num": 1.09,
        "country": "CN"
    },
    {
        "id": "steam_1086940",
        "title": "Baldur's Gate 3",
        "score": 9.6,
        "cover": "https://cdn.akamai.steamstatic.com/steam/apps/1086940/header.jpg",
        "genres": ["RPG", "Turn-Based", "Story Rich"],
        "desc": "Gather your party and return to the Forgotten Realms in a tale of fellowship and betrayal.",
        "release": "Patch 7 - Official Modding",
        "rel_num": 7.0,
        "country": "US"
    },
    {
        "id": "steam_553850",
        "title": "Helldivers 2",
        "score": 8.8,
        "cover": "https://cdn.akamai.steamstatic.com/steam/apps/553850/header.jpg",
        "genres": ["Co-op Shooter", "Third-Person", "Sci-Fi"],
        "desc": "Join the Helldivers and fight for Freedom across a hostile galaxy in fast, frantic third-person shooter action.",
        "release": "Chemical Agents Warbond",
        "rel_num": 4.0,
        "country": "US"
    },
    {
        "id": "steam_1145360",
        "title": "Hades II",
        "score": 9.3,
        "cover": "https://cdn.akamai.steamstatic.com/steam/apps/1145360/header.jpg",
        "genres": ["Roguelike", "Action", "Mythology"],
        "desc": "Battle beyond the Underworld using dark sorcery to take on the Titan of Time in this bewitching sequel.",
        "release": "Olympic Update",
        "rel_num": 2.0,
        "country": "US"
    },
    {
        "id": "steam_1623730",
        "title": "Palworld",
        "score": 8.7,
        "cover": "https://cdn.akamai.steamstatic.com/steam/apps/1623730/header.jpg",
        "genres": ["Survival", "Open World", "Creature Collector"],
        "desc": "Fight, farm, build and work alongside mysterious creatures called 'Pals' in this open-world survival game.",
        "release": "Sakurajima Update",
        "rel_num": 0.3,
        "country": "JP"
    },
    {
        "id": "steam_1091500",
        "title": "Cyberpunk 2077: Phantom Liberty",
        "score": 9.1,
        "cover": "https://cdn.akamai.steamstatic.com/steam/apps/1091500/header.jpg",
        "genres": ["Open World", "Cyberpunk", "RPG"],
        "desc": "As cyber-enhanced mercenary V, join secret agent Solomon Reed to unravel a web of shattered loyalties.",
        "release": "Update 2.13",
        "rel_num": 2.13,
        "country": "PL"
    },
    {
        "id": "steam_2246340",
        "title": "Monster Hunter Wilds",
        "score": 9.0,
        "cover": "https://cdn.akamai.steamstatic.com/steam/apps/2246340/header.jpg",
        "genres": ["Hunting", "Action RPG", "Multiplayer"],
        "desc": "The dynamic natural worlds of the Forbidden Lands await. Track monstrous beasts in living ecosystems.",
        "release": "Open Beta & Pre-release",
        "rel_num": 1.0,
        "country": "JP"
    },
    {
        "id": "steam_730",
        "title": "Counter-Strike 2",
        "score": 8.9,
        "cover": "https://cdn.akamai.steamstatic.com/steam/apps/730/header.jpg",
        "genres": ["Competitive FPS", "Tactical", "Esports"],
        "desc": "The next era of Counter-Strike powered by the Source 2 engine with dynamic smoke and responsive ticks.",
        "release": "The Armory Update",
        "rel_num": 2.0,
        "country": "US"
    },
    {
        "id": "steam_271590",
        "title": "Grand Theft Auto V",
        "score": 9.4,
        "cover": "https://cdn.akamai.steamstatic.com/steam/apps/271590/header.jpg",
        "genres": ["Action", "Open World", "Multiplayer"],
        "desc": "Experience the critically acclaimed open-world adventures of Michael, Franklin and Trevor in Los Santos.",
        "release": "Bottom Dollar Bounties",
        "rel_num": 1.68,
        "country": "US"
    }
]

# All-Time Top 10 Games
GLOBAL_ALL_TIME_GAMES = [
    {
        "id": "steam_292030",
        "title": "The Witcher 3: Wild Hunt",
        "score": 9.8,
        "cover": "https://cdn.akamai.steamstatic.com/steam/apps/292030/header.jpg",
        "genres": ["Masterpiece", "Story Rich", "Open World"],
        "desc": "Track down the Child of Prophecy across a war-torn fantasy world as the monster hunter Geralt of Rivia.",
        "release": "Next-Gen Complete Edition",
        "rel_num": 4.04,
        "country": "PL"
    },
    {
        "id": "steam_1174180",
        "title": "Red Dead Redemption 2",
        "score": 9.7,
        "cover": "https://cdn.akamai.steamstatic.com/steam/apps/1174180/header.jpg",
        "genres": ["Western", "Atmospheric", "Masterpiece"],
        "desc": "America, 1899. Arthur Morgan and the Van der Linde gang are outlaws on the run across the rugged heartland.",
        "release": "Ultimate Edition",
        "rel_num": 1.32,
        "country": "US"
    },
    {
        "id": "steam_1245620_all",
        "title": "Elden Ring",
        "score": 9.6,
        "cover": "https://cdn.akamai.steamstatic.com/steam/apps/1245620/header.jpg",
        "genres": ["Action RPG", "Souls-like", "Open World"],
        "desc": "Rise, Tarnished, and be guided by grace to brandish the power of the Elden Ring and become Elden Lord.",
        "release": "GOTY Edition",
        "rel_num": 1.10,
        "country": "JP"
    },
    {
        "id": "steam_620",
        "title": "Portal 2",
        "score": 9.8,
        "cover": "https://cdn.akamai.steamstatic.com/steam/apps/620/header.jpg",
        "genres": ["Puzzle", "Comedy", "Co-op"],
        "desc": "The 'Perpetual Testing Initiative' has been expanded allowing you to design co-op puzzles for friends!",
        "release": "Complete Version",
        "rel_num": 2.0,
        "country": "US"
    },
    {
        "id": "steam_220",
        "title": "Half-Life 2",
        "score": 9.7,
        "cover": "https://cdn.akamai.steamstatic.com/steam/apps/220/header.jpg",
        "genres": ["FPS", "Sci-Fi", "Classic"],
        "desc": "By taking the realism and responsiveness of the original Half-Life, Half-Life 2 opened doors to world physics.",
        "release": "20th Anniversary Edition",
        "rel_num": 2.2,
        "country": "US"
    },
    {
        "id": "steam_1593500",
        "title": "God of War",
        "score": 9.6,
        "cover": "https://cdn.akamai.steamstatic.com/steam/apps/1593500/header.jpg",
        "genres": ["Action", "Mythology", "Cinematic"],
        "desc": "His vengeance against the Gods of Olympus years behind him, Kratos now lives as a man in the realm of Norse Gods.",
        "release": "Enhanced Edition",
        "rel_num": 1.0,
        "country": "US"
    },
    {
        "id": "steam_489830",
        "title": "The Elder Scrolls V: Skyrim Special Edition",
        "score": 9.5,
        "cover": "https://cdn.akamai.steamstatic.com/steam/apps/489830/header.jpg",
        "genres": ["Open World", "RPG", "Fantasy"],
        "desc": "Winner of more than 200 Game of the Year Awards, Skyrim reimagines and revolutionizes the open-world epic.",
        "release": "Anniversary Edition",
        "rel_num": 1.6,
        "country": "US"
    },
    {
        "id": "steam_1113560",
        "title": "Persona 5 Royal",
        "score": 9.6,
        "cover": "https://cdn.akamai.steamstatic.com/steam/apps/1113560/header.jpg",
        "genres": ["JRPG", "Turn-Based", "Anime"],
        "desc": "Don the mask of Joker and join the Phantom Thieves of Hearts as they break the chains of modern society.",
        "release": "Definitive Edition",
        "rel_num": 1.0,
        "country": "JP"
    },
    {
        "id": "steam_367520",
        "title": "Hollow Knight",
        "score": 9.5,
        "cover": "https://cdn.akamai.steamstatic.com/steam/apps/367520/header.jpg",
        "genres": ["Metroidvania", "Difficult", "Atmospheric"],
        "desc": "Forge your own path in Hollow Knight! An epic action adventure through a vast ruined kingdom of insects.",
        "release": "Voidheart Edition",
        "rel_num": 1.5,
        "country": "AU"
    },
    {
        "id": "steam_268910",
        "title": "Cuphead",
        "score": 9.4,
        "cover": "https://cdn.akamai.steamstatic.com/steam/apps/268910/header.jpg",
        "genres": ["Run & Gun", "Hand-drawn", "Soundtrack"],
        "desc": "Cuphead is a classic run and gun action game heavily focused on boss battles inspired by 1930s cartoons.",
        "release": "The Delicious Last Course",
        "rel_num": 1.3,
        "country": "CA"
    }
]

# Country specific popular games
COUNTRY_GAMES = {
    "jp": [
        {"title": "Elden Ring: Shadow of the Erdtree", "id": "steam_1245620", "score": 9.6, "cover": "https://cdn.akamai.steamstatic.com/steam/apps/1245620/header.jpg", "genres": ["Action RPG"], "desc": "FromSoftware dark fantasy epic.", "release": "Update 1.14", "rel_num": 1.14},
        {"title": "Persona 5 Royal", "id": "steam_1113560", "score": 9.6, "cover": "https://cdn.akamai.steamstatic.com/steam/apps/1113560/header.jpg", "genres": ["JRPG", "Anime"], "desc": "Tokyo phantom thieves epic.", "release": "Definitive", "rel_num": 1.0},
        {"title": "Monster Hunter Wilds", "id": "steam_2246340", "score": 9.2, "cover": "https://cdn.akamai.steamstatic.com/steam/apps/2246340/header.jpg", "genres": ["Action RPG"], "desc": "Dynamic hunting action in the Forbidden Lands.", "release": "Latest Pre-release", "rel_num": 1.0},
        {"title": "Final Fantasy VII Rebirth", "id": "steam_ff7r", "score": 9.4, "cover": "https://placehold.co/460x215/1e1b4b/38bdf8?text=FFVII+Rebirth", "genres": ["JRPG"], "desc": "Cloud and friends venture across Gaia.", "release": "Intergrade", "rel_num": 2.0},
        {"title": "Like a Dragon: Infinite Wealth", "id": "steam_2072450", "score": 9.3, "cover": "https://cdn.akamai.steamstatic.com/steam/apps/2072450/header.jpg", "genres": ["RPG", "Story"], "desc": "Two larger-than-life heroes brought together by destiny.", "release": "Patch 1.20", "rel_num": 1.2},
        {"title": "Dark Souls III", "id": "steam_374320", "score": 9.4, "cover": "https://cdn.akamai.steamstatic.com/steam/apps/374320/header.jpg", "genres": ["Souls-like"], "desc": "Fires fade and the world falls into ruin.", "release": "The Ringed City", "rel_num": 1.15},
        {"title": "NieR:Automata", "id": "steam_524220", "score": 9.3, "cover": "https://cdn.akamai.steamstatic.com/steam/apps/524220/header.jpg", "genres": ["Action", "Sci-Fi"], "desc": "Invaders from another world attack without warning.", "release": "Game of the YoRHa", "rel_num": 1.0},
        {"title": "Resident Evil 4 Remake", "id": "steam_2050650", "score": 9.4, "cover": "https://cdn.akamai.steamstatic.com/steam/apps/2050650/header.jpg", "genres": ["Horror", "Survival"], "desc": "Survival is only the beginning. Reimagined classic.", "release": "Separate Ways", "rel_num": 1.1},
        {"title": "Dragon's Dogma 2", "id": "steam_2054970", "score": 8.7, "cover": "https://cdn.akamai.steamstatic.com/steam/apps/2054970/header.jpg", "genres": ["Open World RPG"], "desc": "Narrative-driven action-RPG series that challenges players.", "release": "Patch 1.05", "rel_num": 1.05},
        {"title": "Sekiro: Shadows Die Twice", "id": "steam_814380", "score": 9.5, "cover": "https://cdn.akamai.steamstatic.com/steam/apps/814380/header.jpg", "genres": ["Souls-like", "Ninja"], "desc": "Carve your own clever path to vengeance.", "release": "GOTY Edition", "rel_num": 1.06}
    ],
    "kr": [
        {"title": "Lies of P", "id": "steam_1627720", "score": 9.2, "cover": "https://cdn.akamai.steamstatic.com/steam/apps/1627720/header.jpg", "genres": ["Souls-like", "Dark Fantasy"], "desc": "A thrilling soulslike that turns the story of Pinocchio on its head.", "release": "Overture DLC", "rel_num": 1.5},
        {"title": "Dave the Diver", "id": "steam_1868140", "score": 9.5, "cover": "https://cdn.akamai.steamstatic.com/steam/apps/1868140/header.jpg", "genres": ["Adventure", "Management"], "desc": "Explore the mysterious Blue Hole by day and run an exotic sushi restaurant by night.", "release": "Godzilla Collaboration", "rel_num": 1.0},
        {"title": "PUBG: BATTLEGROUNDS", "id": "steam_578080", "score": 8.5, "cover": "https://cdn.akamai.steamstatic.com/steam/apps/578080/header.jpg", "genres": ["Battle Royale", "Shooter"], "desc": "Land, loot and outwit your opponents to become the lone survivor.", "release": "Update 32.1", "rel_num": 32.1},
        {"title": "Stellar Blade", "id": "steam_stellar_blade", "score": 9.0, "cover": "https://placehold.co/460x215/090d16/38bdf8?text=Stellar+Blade", "genres": ["Action", "Sci-Fi"], "desc": "Reclaim Earth for humankind in this high-octane post-apocalyptic spectacle.", "release": "Photo Mode & Boss Challenge", "rel_num": 1.2},
        {"title": "Black Desert", "id": "steam_582660", "score": 8.4, "cover": "https://cdn.akamai.steamstatic.com/steam/apps/582660/header.jpg", "genres": ["MMORPG", "Open World"], "desc": "Played by over 20 million Adventurers - experience fast-paced action combat.", "release": "Land of the Morning Light 2", "rel_num": 2.0},
        {"title": "The First Descendant", "id": "steam_2074920", "score": 8.3, "cover": "https://cdn.akamai.steamstatic.com/steam/apps/2074920/header.jpg", "genres": ["Looter Shooter", "Co-op"], "desc": "Third-person looter shooter powered by Unreal Engine 5.", "release": "Season 1: Invasion", "rel_num": 1.1},
        {"title": "Library of Ruina", "id": "steam_1256670", "score": 9.3, "cover": "https://cdn.akamai.steamstatic.com/steam/apps/1256670/header.jpg", "genres": ["Deckbuilding", "Story Rich"], "desc": "Library battle simulation. Welcome to the Library, where books contain the souls of guests.", "release": "Complete", "rel_num": 1.0},
        {"title": "Dungeon & Fighter", "id": "steam_dnf", "score": 8.6, "cover": "https://placehold.co/460x215/1e1b4b/f43f5e?text=Dungeon+%26+Fighter", "genres": ["2D Beat'em Up", "Action"], "desc": "Fast action arcade brawler with deep class progression.", "release": "Bakun Raid", "rel_num": 1.0},
        {"title": "Lost Ark", "id": "steam_1158310", "score": 8.5, "cover": "https://cdn.akamai.steamstatic.com/steam/apps/1158310/header.jpg", "genres": ["ARPG", "MMORPG"], "desc": "Embark on an odyssey for the Lost Ark in a vast, vibrant world.", "release": "Tier 4 Kurzan", "rel_num": 4.0},
        {"title": "Skul: The Hero Slayer", "id": "steam_1147560", "score": 9.2, "cover": "https://cdn.akamai.steamstatic.com/steam/apps/1147560/header.jpg", "genres": ["Action Roguelite", "Pixel Graphics"], "desc": "Guide a lone skeleton warrior to rescue his Demon King from the Imperial army.", "release": "Mythology Pack", "rel_num": 1.8}
    ]
}

def to_media_item(raw: dict, rank: Optional[int] = None) -> MediaItem:
    media_id = raw.get("id") or f"steam_{raw.get('steam_appid', 'custom')}"
    title = raw.get("title") or raw.get("name", "Untitled Game")
    score = float(raw.get("score", 8.8))
    cover = raw.get("cover") or raw.get("header_image") or raw.get("tiny_image") or "https://placehold.co/460x215/18181b/ffffff?text=Game"
    genres = raw.get("genres", ["Gaming", "Action"])
    desc = raw.get("desc", f"Explore and play {title} across leading PC and console platforms.")
    latest_rel = raw.get("release", "Available Now")
    rel_num = float(raw.get("rel_num", 1.0))
    country = raw.get("country", "US")

    providers = generate_provider_links(MediaType.GAME, title, original_id=media_id)

    return MediaItem(
        id=f"game_{media_id}",
        source="steam",
        mediaType=MediaType.GAME,
        title=title,
        coverImage=cover,
        description=desc,
        genres=genres,
        status="ongoing",
        latestRelease=latest_rel,
        latestReleaseNumber=rel_num,
        officialProviders=providers,
        score=score,
        rank=rank,
        country=country
    )

async def search_games(query: str, limit: int = 10) -> List[MediaItem]:
    cache_key = f"games_search_{query.lower()}_{limit}"
    cached = cache.get(cache_key)
    if cached:
        return cached

    results: List[MediaItem] = []

    # 1. Live search via Steam Store API (free, reliable)
    try:
        url = f"https://store.steampowered.com/api/storesearch/?term={httpx.URL(query).raw_path.decode('utf-8', 'ignore')}&l=english&cc=US"
        async with httpx.AsyncClient(timeout=6.0) as client:
            resp = await client.get(f"https://store.steampowered.com/api/storesearch/?term={query}&l=english&cc=US")
            if resp.status_code == 200:
                data = resp.json()
                items = data.get("items", [])
                for item in items[:limit]:
                    appid = str(item.get("id", ""))
                    name = item.get("name", "")
                    cover = item.get("tiny_image", "").replace("capsule_sm_120.jpg", "header.jpg")
                    price_data = item.get("price") or {}
                    final_price = price_data.get("final", 0) / 100.0 if price_data else 0.0
                    rel_label = f"${final_price:.2f}" if final_price > 0 else "Free to Play"

                    providers = generate_provider_links(MediaType.GAME, name, original_id=f"steam_{appid}")
                    results.append(MediaItem(
                        id=f"game_steam_{appid}",
                        source="steam",
                        mediaType=MediaType.GAME,
                        title=name,
                        coverImage=cover,
                        description=f"Action and adventures in {name}. Available on PC via Steam and partner storefronts.",
                        genres=["Game", "Action"],
                        status="ongoing",
                        latestRelease=rel_label,
                        latestReleaseNumber=1.0,
                        officialProviders=providers,
                        score=8.9
                    ))
    except Exception as exc:
        print(f"Steam API query error: {exc}")

    # Fallback to matching curated lists if external query returned few results
    if len(results) < limit:
        q_lower = query.lower()
        all_curated = GLOBAL_TRENDING_GAMES + GLOBAL_ALL_TIME_GAMES
        for item in all_curated:
            if q_lower in item["title"].lower():
                if not any(r.title.lower() == item["title"].lower() for r in results):
                    results.append(to_media_item(item))

    cache.set(cache_key, results, ttl=60)
    return results[:limit]

async def get_top_games(mode: str = "trending", country: str = "global", limit: int = 10) -> List[MediaItem]:
    cache_key = f"games_top_{mode}_{country.lower()}_{limit}"
    cached = cache.get(cache_key)
    if cached:
        return cached

    c_lower = country.lower()
    items: List[dict] = []

    if c_lower in COUNTRY_GAMES and COUNTRY_GAMES[c_lower]:
        items = COUNTRY_GAMES[c_lower]
    elif mode == "top_rated":
        items = GLOBAL_ALL_TIME_GAMES
    else:
        items = GLOBAL_TRENDING_GAMES

    results = [to_media_item(item, rank=idx + 1) for idx, item in enumerate(items[:limit])]
    cache.set(cache_key, results, ttl=60)
    return results
