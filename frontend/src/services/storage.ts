import type { OmniTrackStorage, StorageMode } from '../types/storage';

const LOCAL_STORAGE_KEY = 'omnitrack_user_data_v1';
const BACKUP_STORAGE_KEY = 'omnitrack_user_data_backup';

export const DEFAULT_STORAGE: OmniTrackStorage = {
  version: '1.0.0',
  lastModified: new Date().toISOString(),
  settings: {
    theme: 'dark',
    autoCheckIntervalMinutes: 60,
    guestMode: false,
  },
  customFeeds: [],
  trackedItems: {},
};

// Global file handle reference for File System Access API
let fileHandle: any = null;
let currentMode: StorageMode = 'local_storage';

export function getStorageMode(): StorageMode {
  return currentMode;
}

export function setStorageMode(mode: StorageMode) {
  currentMode = mode;
}

export function getFileHandle() {
  return fileHandle;
}

export function isFileSystemApiSupported(): boolean {
  return typeof window !== 'undefined' && 'showOpenFilePicker' in window && 'showSaveFilePicker' in window;
}

/**
 * Loads storage data.
 * Checks fileHandle if active, else falls back to LocalStorage.
 */
export async function loadStorageData(): Promise<OmniTrackStorage> {
  if (currentMode === 'guest') {
    return { ...DEFAULT_STORAGE, settings: { ...DEFAULT_STORAGE.settings, guestMode: true } };
  }

  // Attempt File System Handle read if connected
  if (fileHandle && currentMode === 'local_file') {
    try {
      const file = await fileHandle.getFile();
      const text = await file.text();
      if (text.trim()) {
        const parsed = JSON.parse(text);
        return validateAndUpgradeStorage(parsed);
      }
    } catch (err) {
      console.warn('Failed to read from linked local file. Falling back to LocalStorage:', err);
    }
  }

  // LocalStorage read
  try {
    const raw = localStorage.getItem(LOCAL_STORAGE_KEY);
    if (raw) {
      const parsed = JSON.parse(raw);
      return validateAndUpgradeStorage(parsed);
    }
  } catch (err) {
    console.error('Error reading localStorage:', err);
  }

  return { ...DEFAULT_STORAGE };
}

/**
 * Persists storage data to connected local file and LocalStorage.
 */
export async function persistStorageData(data: OmniTrackStorage): Promise<boolean> {
  if (currentMode === 'guest' || data.settings.guestMode) {
    return true; // No disk persistence in guest mode
  }

  const updated: OmniTrackStorage = {
    ...data,
    lastModified: new Date().toISOString(),
  };

  const serialized = JSON.stringify(updated, null, 2);

  // 1. Save to connected local file via File System Access API
  if (fileHandle && currentMode === 'local_file') {
    try {
      const writable = await fileHandle.createWritable();
      await writable.write(serialized);
      await writable.close();
    } catch (err) {
      console.error('Error writing to linked local file:', err);
    }
  }

  // 2. Always maintain redundant local cache & backup in LocalStorage
  try {
    const previous = localStorage.getItem(LOCAL_STORAGE_KEY);
    if (previous) {
      localStorage.setItem(BACKUP_STORAGE_KEY, previous);
    }
    localStorage.setItem(LOCAL_STORAGE_KEY, serialized);
    return true;
  } catch (err) {
    console.error('Failed to write to LocalStorage:', err);
    return false;
  }
}

/**
 * Connects directly to an existing local omnitrack_data.json on the user's computer.
 */
export async function linkExistingLocalFile(): Promise<OmniTrackStorage | null> {
  if (!isFileSystemApiSupported()) {
    throw new Error('Your browser does not support the File System Access API. Please use JSON Import/Export instead.');
  }

  try {
    const [handle] = await (window as any).showOpenFilePicker({
      types: [
        {
          description: 'OmniTrack Data JSON',
          accept: { 'application/json': ['.json'] },
        },
      ],
      multiple: false,
    });

    fileHandle = handle;
    currentMode = 'local_file';

    const file = await fileHandle.getFile();
    const text = await file.text();
    const parsed = text.trim() ? JSON.parse(text) : DEFAULT_STORAGE;
    const validated = validateAndUpgradeStorage(parsed);
    
    // Sync to local cache
    localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(validated));
    return validated;
  } catch (err: any) {
    if (err.name !== 'AbortError') {
      console.error('File link aborted or failed:', err);
    }
    return null;
  }
}

/**
 * Creates and links a new omnitrack_data.json file at a location chosen by the user.
 */
export async function createNewLocalFile(currentData: OmniTrackStorage): Promise<boolean> {
  if (!isFileSystemApiSupported()) {
    throw new Error('Your browser does not support the File System Access API.');
  }

  try {
    const handle = await (window as any).showSaveFilePicker({
      suggestedName: 'omnitrack_data.json',
      types: [
        {
          description: 'OmniTracker Data JSON',
          accept: { 'application/json': ['.json'] },
        },
      ],
    });

    fileHandle = handle;
    currentMode = 'local_file';

    const serialized = JSON.stringify(currentData, null, 2);
    const writable = await fileHandle.createWritable();
    await writable.write(serialized);
    await writable.close();

    return true;
  } catch (err: any) {
    if (err.name !== 'AbortError') {
      console.error('Save file picker failed:', err);
    }
    return false;
  }
}

/**
 * Disconnects the local file handle and returns to standard local storage.
 */
export function unlinkLocalFile() {
  fileHandle = null;
  currentMode = 'local_storage';
}

/**
 * Export JSON file as a standard browser download.
 */
export function exportDataAsJson(data: OmniTrackStorage) {
  const jsonStr = JSON.stringify(data, null, 2);
  const blob = new Blob([jsonStr], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `omnitrack_data_${new Date().toISOString().slice(0, 10)}.json`;
  a.click();
  URL.revokeObjectURL(url);
}

/**
 * Parse uploaded JSON file and return storage structure.
 */
export function parseImportedJson(jsonText: string): OmniTrackStorage {
  const parsed = JSON.parse(jsonText);
  return validateAndUpgradeStorage(parsed);
}

function validateAndUpgradeStorage(data: any): OmniTrackStorage {
  return {
    version: data?.version || '1.0.0',
    lastModified: data?.lastModified || new Date().toISOString(),
    settings: {
      theme: data?.settings?.theme || 'dark',
      autoCheckIntervalMinutes: data?.settings?.autoCheckIntervalMinutes || 60,
      guestMode: Boolean(data?.settings?.guestMode),
    },
    customFeeds: Array.isArray(data?.customFeeds) ? data.customFeeds : [],
    trackedItems: data?.trackedItems && typeof data.trackedItems === 'object' ? data.trackedItems : {},
  };
}
