import type { MediaItem } from './media';

export interface UserTrackedItem {
  mediaId: string;
  mediaItem: MediaItem;
  userProgress: number;
  isPinned: boolean;
  notes?: string;
  lastUpdated: string; // ISO 8601
}

export interface CustomFeedRecord {
  id: string;
  name: string;
  url: string;
  mediaType: string;
  lastFetched?: string;
}

export interface AppSettings {
  theme: 'dark' | 'light' | 'system';
  autoCheckIntervalMinutes: number;
  guestMode: boolean;
}

export interface OmniTrackStorage {
  version: string;
  lastModified: string;
  settings: AppSettings;
  customFeeds: CustomFeedRecord[];
  trackedItems: Record<string, UserTrackedItem>;
}

export type StorageMode = 'local_file' | 'local_storage' | 'guest';

export interface StorageStatus {
  mode: StorageMode;
  fileName: string | null;
  lastSaved: string | null;
  isDirty: boolean;
}
