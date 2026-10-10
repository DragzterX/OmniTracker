from typing import List
import urllib.parse
from ..models.media import MediaType, ProviderLink

def generate_provider_links(media_type: MediaType, title: str, original_id: str = "") -> List[ProviderLink]:
    """
    Generates 5-10 authoritative, verified, high-rating sources/websites for any media item
    so that users can easily re-route to stream, read, play, listen, or view details.
    """
    clean_title = title.strip()
    encoded = urllib.parse.quote_plus(clean_title)
    providers: List[ProviderLink] = []

    if media_type == MediaType.ANIME:
        providers = [
            ProviderLink(name="Crunchyroll", url=f"https://www.crunchyroll.com/search?q={encoded}"),
            ProviderLink(name="AniList", url=f"https://anilist.co/search/anime?search={encoded}"),
            ProviderLink(name="MyAnimeList", url=f"https://myanimelist.net/anime.php?q={encoded}"),
            ProviderLink(name="Anime-Planet", url=f"https://www.anime-planet.com/anime/all?name={encoded}"),
            ProviderLink(name="LiveChart.me", url=f"https://www.livechart.me/search?q={encoded}"),
            ProviderLink(name="Kitsu", url=f"https://kitsu.app/anime?text={encoded}"),
            ProviderLink(name="Netflix", url=f"https://www.netflix.com/search?q={encoded}"),
            ProviderLink(name="HIDIVE", url=f"https://www.hidive.com/search?q={encoded}")
        ]
    elif media_type == MediaType.MANGA:
        providers = [
            ProviderLink(name="MangaDex", url=f"https://mangadex.org/search?q={encoded}"),
            ProviderLink(name="MangaPlus", url=f"https://mangaplus.shueisha.co.jp/search?keyword={encoded}"),
            ProviderLink(name="MyAnimeList Manga", url=f"https://myanimelist.net/manga.php?q={encoded}"),
            ProviderLink(name="AniList Manga", url=f"https://anilist.co/search/manga?search={encoded}"),
            ProviderLink(name="MangaUpdates", url=f"https://www.mangaupdates.com/series.html?search={encoded}"),
            ProviderLink(name="Viz Media", url=f"https://www.viz.com/search?search={encoded}"),
            ProviderLink(name="BookWalker", url=f"https://global.bookwalker.jp/search/?word={encoded}"),
            ProviderLink(name="Comic-Walker", url=f"https://comic-walker.com/search/?q={encoded}")
        ]
    elif media_type == MediaType.MANHWA:
        providers = [
            ProviderLink(name="Webtoons", url=f"https://www.webtoons.com/en/search?keyword={encoded}"),
            ProviderLink(name="Tappytoon", url=f"https://www.tappytoon.com/en/search?queryString={encoded}"),
            ProviderLink(name="Tapas", url=f"https://tapas.io/search?q={encoded}"),
            ProviderLink(name="MangaDex", url=f"https://mangadex.org/search?q={encoded}"),
            ProviderLink(name="Lezhin Comics", url=f"https://www.lezhinus.com/en/search?q={encoded}"),
            ProviderLink(name="Anime-Planet Manhwa", url=f"https://www.anime-planet.com/manga/all?name={encoded}&type=manhwa"),
            ProviderLink(name="MangaUpdates", url=f"https://www.mangaupdates.com/series.html?search={encoded}"),
            ProviderLink(name="Pocket Comics", url=f"https://www.pocketcomics.com/search?q={encoded}")
        ]
    elif media_type == MediaType.TV:
        providers = [
            ProviderLink(name="TMDb", url=f"https://www.themoviedb.org/search?query={encoded}"),
            ProviderLink(name="IMDb", url=f"https://www.imdb.com/find/?q={encoded}"),
            ProviderLink(name="JustWatch", url=f"https://www.justwatch.com/us/search?q={encoded}"),
            ProviderLink(name="Rotten Tomatoes", url=f"https://www.rottentomatoes.com/search?search={encoded}"),
            ProviderLink(name="Trakt.tv", url=f"https://trakt.tv/search?query={encoded}"),
            ProviderLink(name="TV Time", url=f"https://www.tvtime.com/en/search?q={encoded}"),
            ProviderLink(name="Metacritic TV", url=f"https://www.metacritic.com/search/{encoded}/?category=1"),
            ProviderLink(name="Reelgood", url=f"https://reelgood.com/search?q={encoded}")
        ]
    elif media_type == MediaType.MOVIE:
        providers = [
            ProviderLink(name="TMDb", url=f"https://www.themoviedb.org/search?query={encoded}"),
            ProviderLink(name="IMDb", url=f"https://www.imdb.com/find/?q={encoded}"),
            ProviderLink(name="Letterboxd", url=f"https://letterboxd.com/search/{encoded}/"),
            ProviderLink(name="Rotten Tomatoes", url=f"https://www.rottentomatoes.com/search?search={encoded}"),
            ProviderLink(name="JustWatch", url=f"https://www.justwatch.com/us/search?q={encoded}"),
            ProviderLink(name="Metacritic Movies", url=f"https://www.metacritic.com/search/{encoded}/?category=2"),
            ProviderLink(name="Trakt.tv", url=f"https://trakt.tv/search?query={encoded}"),
            ProviderLink(name="Box Office Mojo", url=f"https://www.boxofficemojo.com/search/?q={encoded}")
        ]
    elif media_type == MediaType.GAME:
        steam_url = f"https://store.steampowered.com/search/?term={encoded}"
        if original_id.startswith("steam_"):
            steam_app_id = original_id.replace("steam_", "")
            if steam_app_id.isdigit():
                steam_url = f"https://store.steampowered.com/app/{steam_app_id}/"

        providers = [
            ProviderLink(name="Steam", url=steam_url),
            ProviderLink(name="Epic Games Store", url=f"https://store.epicgames.com/en-US/browse?q={encoded}"),
            ProviderLink(name="GOG.com", url=f"https://www.gog.com/en/games?query={encoded}"),
            ProviderLink(name="Itch.io", url=f"https://itch.io/search?q={encoded}"),
            ProviderLink(name="Metacritic Games", url=f"https://www.metacritic.com/search/{encoded}/?category=13"),
            ProviderLink(name="HowLongToBeat", url=f"https://howlongtobeat.com/?q={encoded}"),
            ProviderLink(name="IGDB", url=f"https://www.igdb.com/search?utf8=%E2%9C%93&q={encoded}"),
            ProviderLink(name="PCGamingWiki", url=f"https://www.pcgamingwiki.com/w/index.php?search={encoded}")
        ]
    elif media_type == MediaType.SONG:
        providers = [
            ProviderLink(name="Spotify", url=f"https://open.spotify.com/search/{encoded}"),
            ProviderLink(name="YouTube Music", url=f"https://music.youtube.com/search?q={encoded}"),
            ProviderLink(name="YouTube", url=f"https://www.youtube.com/results?search_query={encoded}"),
            ProviderLink(name="Apple Music", url=f"https://music.apple.com/us/search?term={encoded}"),
            ProviderLink(name="SoundCloud", url=f"https://soundcloud.com/search?q={encoded}"),
            ProviderLink(name="Deezer", url=f"https://www.deezer.com/search/{encoded}"),
            ProviderLink(name="Genius (Lyrics)", url=f"https://genius.com/search?q={encoded}"),
            ProviderLink(name="Last.fm", url=f"https://www.last.fm/search?q={encoded}")
        ]
    else:
        providers = [
            ProviderLink(name="Google Search", url=f"https://www.google.com/search?q={encoded}")
        ]

    return providers
