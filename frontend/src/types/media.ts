export type MediaType = 'all' | 'tv' | 'movie' | 'anime' | 'manga' | 'manhwa' | 'game' | 'song' | 'custom_feed';

export interface ProviderLink {
  name: string;
  url: string;
}

export interface MediaItem {
  id: string;
  source: string;
  mediaType: MediaType;
  title: string;
  originalTitle?: string;
  coverImage: string;
  bannerImage?: string;
  description: string;
  genres: string[];
  status: 'ongoing' | 'completed' | 'upcoming' | 'hiatus';
  latestRelease: string;
  latestReleaseNumber: number;
  latestReleaseDate?: string;
  nextReleaseDate?: string;
  totalReleases?: number;
  officialProviders: ProviderLink[];
  score?: number;
  rank?: number;
  country?: string;
}

export interface SearchResponse {
  query: string;
  mediaType?: string;
  total: number;
  items: MediaItem[];
}

export interface FeedParseResponse {
  feedTitle: string;
  feedUrl: string;
  description?: string;
  items: MediaItem[];
}
