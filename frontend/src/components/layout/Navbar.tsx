import { Search, BookmarkCheck, Rss, Compass, Trophy, HardDrive, Shield } from 'lucide-react';
import type { StorageStatus } from '../../types/storage';

interface NavbarProps {
  activeTab: 'home' | 'profile' | 'feeds' | 'recommendations' | 'rankings';
  setActiveTab: (tab: 'home' | 'profile' | 'feeds' | 'recommendations' | 'rankings') => void;
  trackedCount: number;
  feedsCount: number;
  storageStatus: StorageStatus;
  onOpenStorageModal: () => void;
}

export function Navbar({
  activeTab,
  setActiveTab,
  trackedCount,
  feedsCount,
  storageStatus,
  onOpenStorageModal,
}: NavbarProps) {
  return (
    <header className="top-header">
      <div className="brand-section">
        <div className="brand-logo">Ω</div>
        <div>
          <span className="brand-title">OmniTracker</span>
        </div>
        <span className="brand-badge">Local-First</span>
      </div>

      <nav className="nav-tabs" aria-label="Main Navigation">
        <button
          id="nav-tab-home"
          className={`tab-btn ${activeTab === 'home' ? 'active' : ''}`}
          onClick={() => setActiveTab('home')}
        >
          <Search size={16} />
          <span>Home</span>
        </button>

        <button
          id="nav-tab-profile"
          className={`tab-btn ${activeTab === 'profile' ? 'active' : ''}`}
          onClick={() => setActiveTab('profile')}
        >
          <BookmarkCheck size={16} />
          <span>Profile</span>
          {trackedCount > 0 && <span className="tab-badge">{trackedCount}</span>}
        </button>

        <button
          id="nav-tab-feeds"
          className={`tab-btn ${activeTab === 'feeds' ? 'active' : ''}`}
          onClick={() => setActiveTab('feeds')}
        >
          <Rss size={16} />
          <span>Add Search Websites</span>
          {feedsCount > 0 && <span className="tab-badge">{feedsCount}</span>}
        </button>

        <button
          id="nav-tab-recommendations"
          className={`tab-btn ${activeTab === 'recommendations' ? 'active' : ''}`}
          onClick={() => setActiveTab('recommendations')}
        >
          <Compass size={16} />
          <span>Recommendations</span>
        </button>

        <button
          id="nav-tab-rankings"
          className={`tab-btn ${activeTab === 'rankings' ? 'active' : ''}`}
          onClick={() => setActiveTab('rankings')}
        >
          <Trophy size={16} />
          <span>Rankings</span>
        </button>
      </nav>

      <div className="header-actions">
        <button
          id="storage-status-btn"
          className="storage-status-pill"
          onClick={onOpenStorageModal}
          title="Click to manage disk persistence and backups"
        >
          {storageStatus.mode === 'local_file' ? (
            <>
              <span className="storage-dot connected" />
              <HardDrive size={13} />
              <span>Linked to Disk</span>
            </>
          ) : storageStatus.mode === 'guest' ? (
            <>
              <span className="storage-dot guest" />
              <Shield size={13} />
              <span>Guest Mode</span>
            </>
          ) : (
            <>
              <span className="storage-dot cached" />
              <HardDrive size={13} />
              <span>Browser Cache</span>
            </>
          )}
        </button>
      </div>
    </header>
  );
}
