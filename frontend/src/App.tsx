import { useState, useEffect } from 'react';
import './styles/global.css';
import { Navbar } from './components/layout/Navbar';
import { StorageModal } from './components/storage/StorageModal';
import { HomePage } from './pages/HomePage';
import { ProfileTrackerPage } from './pages/ProfileTrackerPage';
import { AddFeedsPage } from './pages/AddFeedsPage';
import { RecommendationsPage } from './pages/RecommendationsPage';
import { RankingsPage } from './pages/RankingsPage';
import type { MediaItem } from './types/media';
import type {
  OmniTrackStorage,
  CustomFeedRecord,
  StorageStatus,
} from './types/storage';
import {
  loadStorageData,
  persistStorageData,
  getStorageMode,
  setStorageMode,
  DEFAULT_STORAGE,
} from './services/storage';

export function App() {
  const [activeTab, setActiveTab] = useState<'home' | 'profile' | 'feeds' | 'recommendations' | 'rankings'>('home');
  const [storage, setStorage] = useState<OmniTrackStorage>(DEFAULT_STORAGE);
  const [isStorageModalOpen, setIsStorageModalOpen] = useState(false);
  const [storageStatus, setStorageStatus] = useState<StorageStatus>({
    mode: 'local_storage',
    fileName: null,
    lastSaved: null,
    isDirty: false,
  });

  // Load storage from disk/cache on initial mount
  useEffect(() => {
    async function initStorage() {
      const data = await loadStorageData();
      setStorage(data);
      setStorageStatus({
        mode: getStorageMode(),
        fileName: getStorageMode() === 'local_file' ? 'omnitrack_data.json' : null,
        lastSaved: data.lastModified,
        isDirty: false,
      });
    }
    initStorage();
  }, []);

  const saveAndSync = async (updated: OmniTrackStorage) => {
    setStorage(updated);
    await persistStorageData(updated);
    setStorageStatus((prev) => ({
      ...prev,
      mode: getStorageMode(),
      lastSaved: new Date().toISOString(),
    }));
  };

  const handleTrackMedia = async (media: MediaItem) => {
    const existing = storage.trackedItems[media.id];
    const updated: OmniTrackStorage = {
      ...storage,
      trackedItems: {
        ...storage.trackedItems,
        [media.id]: {
          mediaId: media.id,
          mediaItem: media,
          userProgress: existing ? existing.userProgress : 0,
          isPinned: existing ? existing.isPinned : false,
          lastUpdated: new Date().toISOString(),
        },
      },
    };
    await saveAndSync(updated);
  };

  const handleUntrackMedia = async (mediaId: string) => {
    const nextTracked = { ...storage.trackedItems };
    delete nextTracked[mediaId];
    const updated: OmniTrackStorage = {
      ...storage,
      trackedItems: nextTracked,
    };
    await saveAndSync(updated);
  };

  const handleUpdateProgress = async (mediaId: string, delta: number) => {
    const item = storage.trackedItems[mediaId];
    if (!item) return;

    const newProgress = Math.max(0, item.userProgress + delta);
    const updated: OmniTrackStorage = {
      ...storage,
      trackedItems: {
        ...storage.trackedItems,
        [mediaId]: {
          ...item,
          userProgress: newProgress,
          lastUpdated: new Date().toISOString(),
        },
      },
    };
    await saveAndSync(updated);
  };

  const handleTogglePin = async (mediaId: string) => {
    const item = storage.trackedItems[mediaId];
    if (!item) return;

    const updated: OmniTrackStorage = {
      ...storage,
      trackedItems: {
        ...storage.trackedItems,
        [mediaId]: {
          ...item,
          isPinned: !item.isPinned,
          lastUpdated: new Date().toISOString(),
        },
      },
    };
    await saveAndSync(updated);
  };

  const handleAddFeed = async (feed: CustomFeedRecord) => {
    const updated: OmniTrackStorage = {
      ...storage,
      customFeeds: [...storage.customFeeds, feed],
    };
    await saveAndSync(updated);
  };

  const handleRemoveFeed = async (feedId: string) => {
    const updated: OmniTrackStorage = {
      ...storage,
      customFeeds: storage.customFeeds.filter((f) => f.id !== feedId),
    };
    await saveAndSync(updated);
  };

  const handleStorageUpdated = async (newData: OmniTrackStorage) => {
    await saveAndSync(newData);
  };

  const handleToggleGuestMode = async (guest: boolean) => {
    setStorageMode(guest ? 'guest' : 'local_storage');
    const updated: OmniTrackStorage = {
      ...storage,
      settings: {
        ...storage.settings,
        guestMode: guest,
      },
    };
    setStorage(updated);
    if (!guest) {
      await persistStorageData(updated);
    }
    setStorageStatus({
      mode: guest ? 'guest' : 'local_storage',
      fileName: null,
      lastSaved: updated.lastModified,
      isDirty: false,
    });
  };

  return (
    <div className="app-container">
      <Navbar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        trackedCount={Object.keys(storage.trackedItems).length}
        feedsCount={storage.customFeeds.length}
        storageStatus={storageStatus}
        onOpenStorageModal={() => setIsStorageModalOpen(true)}
      />

      <main className="main-content">
        {activeTab === 'home' && (
          <HomePage
            storage={storage}
            onTrackMedia={handleTrackMedia}
            onUpdateProgress={handleUpdateProgress}
            onTogglePin={handleTogglePin}
          />
        )}

        {activeTab === 'profile' && (
          <ProfileTrackerPage
            storage={storage}
            onTrackMedia={handleTrackMedia}
            onUntrackMedia={handleUntrackMedia}
            onUpdateProgress={handleUpdateProgress}
            onTogglePin={handleTogglePin}
          />
        )}

        {activeTab === 'feeds' && (
          <AddFeedsPage
            storage={storage}
            onAddFeed={handleAddFeed}
            onRemoveFeed={handleRemoveFeed}
            onTrackMedia={handleTrackMedia}
            onUpdateProgress={handleUpdateProgress}
          />
        )}

        {activeTab === 'recommendations' && (
          <RecommendationsPage
            storage={storage}
            onTrackMedia={handleTrackMedia}
            onUpdateProgress={handleUpdateProgress}
            onTogglePin={handleTogglePin}
          />
        )}

        {activeTab === 'rankings' && (
          <RankingsPage
            storage={storage}
            onTrackMedia={handleTrackMedia}
            onUpdateProgress={handleUpdateProgress}
            onTogglePin={handleTogglePin}
          />
        )}
      </main>

      <StorageModal
        isOpen={isStorageModalOpen}
        onClose={() => setIsStorageModalOpen(false)}
        storage={storage}
        storageStatus={storageStatus}
        onStorageUpdated={handleStorageUpdated}
        onToggleGuestMode={handleToggleGuestMode}
      />
    </div>
  );
}

export default App;
