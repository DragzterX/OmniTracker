from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field

class MediaType(str, Enum):
    TV = "tv"
    MOVIE = "movie"
    ANIME = "anime"
    MANGA = "manga"
    MANHWA = "manhwa"
    GAME = "game"
    SONG = "song"
    CUSTOM_FEED = "custom_feed"

class ProviderLink(BaseModel):
    name: str
    url: str

class MediaItem(BaseModel):
    id: str = Field(..., description="Unique media identifier e.g. anilist_21 or tmdb_tv_1399")
    source: str = Field(..., description="Data source: tmdb, anilist, mangadex, steam, itunes, custom")
    mediaType: MediaType = Field(..., description="Classification: tv, movie, anime, manga, manhwa, game, song, custom_feed")
    title: str = Field(..., description="Primary display title")
    originalTitle: Optional[str] = Field(None, description="Original non-English title if available")
    coverImage: str = Field(..., description="URL to high-res poster/cover image")
    bannerImage: Optional[str] = Field(None, description="URL to landscape banner image")
    description: str = Field("", description="Synopsis / plot summary")
    genres: List[str] = Field(default_factory=list, description="List of genres")
    status: str = Field("ongoing", description="Release status: ongoing, completed, upcoming, hiatus")
    
    # Release progress & tracking
    latestRelease: str = Field("", description="Latest release label e.g. Episode 12 or Chapter 104")
    latestReleaseNumber: float = Field(0.0, description="Normalized numeric representation of latest release")
    latestReleaseDate: Optional[str] = Field(None, description="ISO 8601 release timestamp of latest item")
    nextReleaseDate: Optional[str] = Field(None, description="ISO 8601 timestamp of upcoming release if known")
    totalReleases: Optional[int] = Field(None, description="Total expected episodes or chapters if known")
    
    # Provider availability
    officialProviders: List[ProviderLink] = Field(default_factory=list, description="Official legal streaming / reading / buying links")
    score: Optional[float] = Field(None, description="Aggregate score out of 10 or 100")
    rank: Optional[int] = Field(None, description="Ranking position (1-10) in charts")
    country: Optional[str] = Field(None, description="Country of origin / market code")

class SearchResponse(BaseModel):
    query: str
    mediaType: Optional[str] = None
    total: int
    items: List[MediaItem]

class FeedParseRequest(BaseModel):
    url: str
    mediaType: Optional[MediaType] = MediaType.CUSTOM_FEED

class FeedParseResponse(BaseModel):
    feedTitle: str
    feedUrl: str
    description: Optional[str] = None
    items: List[MediaItem]
