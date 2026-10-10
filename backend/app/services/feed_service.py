import hashlib
from datetime import datetime
from typing import Optional, List
import httpx
import feedparser
from ..models.media import MediaItem, MediaType, ProviderLink, FeedParseResponse

async def parse_custom_feed(url: str, default_media_type: MediaType = MediaType.CUSTOM_FEED) -> FeedParseResponse:
    headers = {
        "User-Agent": "OmniTracker/1.0 (Feed Ingestion Service; +https://github.com/omnitracker)"
    }
    
    async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
        resp = await client.get(url, headers=headers)
        resp.raise_for_status()
        raw_xml = resp.text

    parsed = feedparser.parse(raw_xml)
    
    feed_title = parsed.feed.get("title", "Custom Web Feed")
    feed_desc = parsed.feed.get("description", "")
    
    items: List[MediaItem] = []
    
    for entry in parsed.entries[:20]:
        title = entry.get("title", "Untitled Update")
        link = entry.get("link", url)
        summary = entry.get("summary") or entry.get("description") or ""
        
        # Strip simple HTML
        clean_summary = summary.replace("<p>", "").replace("</p>", "\n")
        if len(clean_summary) > 300:
            clean_summary = clean_summary[:297] + "..."
            
        published_parsed = entry.get("published_parsed") or entry.get("updated_parsed")
        release_date = None
        if published_parsed:
            try:
                release_date = datetime(*published_parsed[:6]).isoformat()
            except Exception:
                pass

        # Hash ID for consistent identification
        entry_hash = hashlib.md5(f"{url}_{title}".encode()).hexdigest()[:12]
        
        items.append(
            MediaItem(
                id=f"feed_{entry_hash}",
                source="custom",
                mediaType=default_media_type,
                title=title,
                coverImage="https://placehold.co/400x600/1e293b/94a3b8?text=Custom+Feed",
                description=clean_summary,
                genres=["Custom Feed"],
                status="ongoing",
                latestRelease="Latest Post / Update",
                latestReleaseNumber=1.0,
                latestReleaseDate=release_date,
                nextReleaseDate=None,
                officialProviders=[
                    ProviderLink(name=feed_title[:20], url=link)
                ],
                score=None
            )
        )
        
    return FeedParseResponse(
        feedTitle=feed_title,
        feedUrl=url,
        description=feed_desc,
        items=items
    )
