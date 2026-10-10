from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from .media import MediaItem, MediaType

class UserTrackedItem(BaseModel):
    mediaId: str
    mediaItem: MediaItem
    userProgress: float = Field(0.0, description="Current episode or chapter user has completed")
    isPinned: bool = Field(False, description="Whether pinned to top of tracker")
    notes: Optional[str] = Field(None, description="Personal user notes")
    lastUpdated: str = Field(..., description="ISO 8601 timestamp of last user interaction")

class CustomFeedRecord(BaseModel):
    id: str
    name: str
    url: str
    mediaType: MediaType = MediaType.CUSTOM_FEED
    lastFetched: Optional[str] = None

class AppSettings(BaseModel):
    theme: str = Field("dark", description="'dark', 'light', or 'system'")
    autoCheckIntervalMinutes: int = Field(60, description="Auto-check frequency in minutes")
    guestMode: bool = Field(False, description="Temporary in-memory mode")

class OmniTrackStorage(BaseModel):
    version: str = Field("1.0.0", description="Data format version")
    lastModified: str = Field(..., description="ISO 8601 timestamp")
    settings: AppSettings = Field(default_factory=AppSettings)
    customFeeds: List[CustomFeedRecord] = Field(default_factory=list)
    trackedItems: Dict[str, UserTrackedItem] = Field(default_factory=dict)
