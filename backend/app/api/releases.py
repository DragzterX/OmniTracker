from typing import List
from fastapi import APIRouter
from ..models.media import MediaItem

router = APIRouter(prefix="/releases", tags=["Releases"])

@router.get("/status")
async def get_release_status():
    """Returns server-time and status for client schedule synchronization."""
    from datetime import datetime, timezone
    return {
        "serverTime": datetime.now(timezone.utc).isoformat(),
        "status": "online"
    }
