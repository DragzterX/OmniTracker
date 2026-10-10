from fastapi import APIRouter, HTTPException
from ..models.media import FeedParseRequest, FeedParseResponse
from ..services.feed_service import parse_custom_feed

router = APIRouter(prefix="/feeds", tags=["Custom Feeds"])

@router.post("/parse", response_model=FeedParseResponse)
async def parse_feed_endpoint(req: FeedParseRequest):
    if not req.url or not req.url.startswith(("http://", "https://")):
        raise HTTPException(status_code=400, detail="Invalid feed URL. Must begin with http:// or https://")
        
    try:
        parsed = await parse_custom_feed(req.url, req.mediaType)
        return parsed
    except Exception as exc:
        raise HTTPException(status_code=422, detail=f"Failed to fetch or parse feed: {str(exc)}")
