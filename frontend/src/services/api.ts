import type { MediaItem, SearchResponse, FeedParseResponse } from '../types/media';

const API_BASE = '/api';

export async function searchMedia(query: string, mediaType: string = 'all'): Promise<MediaItem[]> {
  if (!query.trim()) return [];
  try {
    const params = new URLSearchParams({ q: query.trim(), type: mediaType });
    const res = await fetch(`${API_BASE}/search?${params.toString()}`);
    if (!res.ok) {
      throw new Error(`Search request failed with status: ${res.status}`);
    }
    const data: SearchResponse = await res.json();
    return data.items || [];
  } catch (error) {
    console.error('API search error:', error);
    return [];
  }
}

export async function getRecommendations(mediaType: string = 'all'): Promise<MediaItem[]> {
  try {
    const params = new URLSearchParams({ type: mediaType });
    const res = await fetch(`${API_BASE}/recommendations?${params.toString()}`);
    if (!res.ok) {
      throw new Error(`Recommendations request failed with status: ${res.status}`);
    }
    const data: MediaItem[] = await res.json();
    return data || [];
  } catch (error) {
    console.error('API recommendations error:', error);
    return [];
  }
}

export async function parseFeed(url: string, mediaType: string = 'custom_feed'): Promise<FeedParseResponse> {
  const res = await fetch(`${API_BASE}/feeds/parse`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ url: url.trim(), mediaType }),
  });
  if (!res.ok) {
    const errData = await res.json().catch(() => ({}));
    throw new Error(errData.detail || `Feed parsing failed with status: ${res.status}`);
  }
  return res.json();
}

export interface RankingsData {
  mode: string;
  country: string;
  anime: MediaItem[];
  tv: MediaItem[];
  movie: MediaItem[];
  manga: MediaItem[];
  manhwa: MediaItem[];
  game: MediaItem[];
  song: MediaItem[];
}

export async function getRankings(mode: string = 'trending', country: string = 'global'): Promise<RankingsData | null> {
  try {
    const params = new URLSearchParams({ mode, country });
    const res = await fetch(`${API_BASE}/rankings?${params.toString()}`);
    if (!res.ok) {
      throw new Error(`Rankings request failed with status: ${res.status}`);
    }
    return await res.json();
  } catch (error) {
    console.error('API rankings error:', error);
    return null;
  }
}

export async function checkBackendHealth(): Promise<{ status: string; tmdb_configured: boolean }> {
  try {
    const res = await fetch(`${API_BASE}/health`, { signal: AbortSignal.timeout(3000) });
    if (res.ok) {
      return await res.json();
    }
  } catch {
    // Backend offline / disconnected
  }
  return { status: 'offline', tmdb_configured: false };
}

