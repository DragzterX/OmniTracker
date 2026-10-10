import { useState } from 'react';
import { Bookmark, Calendar, Trash2 } from 'lucide-react';
import type { OmniTrackStorage } from '../types/storage';
import type { MediaItem } from '../types/media';
import { MediaCard } from '../components/media/MediaCard';

interface ProfileTrackerPageProps {
  storage: OmniTrackStorage;
  onTrackMedia: (media: MediaItem) => void;
  onUntrackMedia: (mediaId: string) => void;
  onUpdateProgress: (mediaId: string, delta: number) => void;
  onTogglePin: (mediaId: string) => void;
}

export function ProfileTrackerPage({
  storage,
  onTrackMedia,
  onUntrackMedia,
  onUpdateProgress,
  onTogglePin,
}: ProfileTrackerPageProps) {
  const [filter, setFilter] = useState<'all' | 'pinned' | 'unread' | 'completed'>('all');
  const [mediaTypeFilter, setMediaTypeFilter] = useState<string>('all');
  const [showCalendar, setShowCalendar] = useState(false);

  const trackedList = Object.values(storage.trackedItems);

  // Sorting: Pinned first, then recently updated
  const sortedList = [...trackedList].sort((a, b) => {
    if (a.isPinned !== b.isPinned) return a.isPinned ? -1 : 1;
    return new Date(b.lastUpdated).getTime() - new Date(a.lastUpdated).getTime();
  });

  const filteredList = sortedList.filter((item) => {
    if (mediaTypeFilter !== 'all' && item.mediaItem.mediaType !== mediaTypeFilter) {
      return false;
    }
    if (filter === 'pinned') return item.isPinned;
    if (filter === 'unread') return item.mediaItem.latestReleaseNumber > item.userProgress;
    if (filter === 'completed') return item.mediaItem.status === 'completed';
    return true;
  });

  // Calculate upcoming releases for the release schedule
  const upcomingReleases = trackedList
    .filter((item) => item.mediaItem.nextReleaseDate)
    .sort(
      (a, b) =>
        new Date(a.mediaItem.nextReleaseDate!).getTime() - new Date(b.mediaItem.nextReleaseDate!).getTime()
    );

  return (
    <div>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1.5rem', flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <h1 style={{ fontSize: '1.75rem', fontWeight: 800 }}>Profile & Watchlist</h1>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>
            Tracking {trackedList.length} titles. Progress is saved directly to your local file.
          </p>
        </div>

        <button
          className="btn-secondary"
          onClick={() => setShowCalendar(!showCalendar)}
          style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', padding: '0.6rem 1rem' }}
        >
          <Calendar size={16} />
          <span>{showCalendar ? 'Hide Release Schedule' : 'View Release Schedule'}</span>
        </button>
      </div>

      {showCalendar && (
        <div
          style={{
            background: 'var(--bg-card)',
            border: '1px solid var(--border-subtle)',
            borderRadius: 'var(--radius-lg)',
            padding: '1.25rem',
            marginBottom: '2rem',
          }}
        >
          <h2 style={{ fontSize: '1.1rem', fontWeight: 700, marginBottom: '0.75rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Calendar size={18} color="var(--accent-secondary)" />
            Upcoming Airing / Chapter Schedule
          </h2>

          {upcomingReleases.length === 0 ? (
            <div style={{ color: 'var(--text-muted)', fontSize: '0.875rem' }}>
              No scheduled upcoming releases detected for your currently tracked shows.
            </div>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
              {upcomingReleases.map((item) => {
                const date = new Date(item.mediaItem.nextReleaseDate!);
                return (
                  <div
                    key={item.mediaId}
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'space-between',
                      background: 'rgba(255, 255, 255, 0.03)',
                      padding: '0.75rem 1rem',
                      borderRadius: 'var(--radius-md)',
                      border: '1px solid var(--border-subtle)',
                    }}
                  >
                    <div>
                      <div style={{ fontWeight: 600, fontSize: '0.95rem' }}>{item.mediaItem.title}</div>
                      <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
                        {item.mediaItem.latestRelease} → Next Release Scheduled
                      </div>
                    </div>
                    <div style={{ textAlign: 'right' }}>
                      <div style={{ fontWeight: 700, color: 'var(--accent-secondary)', fontSize: '0.9rem' }}>
                        {date.toLocaleDateString(undefined, { weekday: 'short', month: 'short', day: 'numeric' })}
                      </div>
                      <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                        {date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>
      )}

      {/* Filters Bar */}
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          flexWrap: 'wrap',
          gap: '1rem',
          marginBottom: '1.5rem',
        }}
      >
        <div style={{ display: 'flex', gap: '0.4rem', flexWrap: 'wrap' }}>
          {[
            { label: 'All Tracked', val: 'all' },
            { label: 'Pinned', val: 'pinned' },
            { label: 'Unread / Behind', val: 'unread' },
            { label: 'Completed', val: 'completed' },
          ].map((f) => (
            <button
              key={f.val}
              className={`chip ${filter === f.val ? 'active' : ''}`}
              onClick={() => setFilter(f.val as any)}
            >
              {f.label}
            </button>
          ))}
        </div>

        <select
          className="form-select"
          value={mediaTypeFilter}
          onChange={(e) => setMediaTypeFilter(e.target.value)}
          style={{ width: 'auto', padding: '0.4rem 0.8rem' }}
        >
          <option value="all">All Media Types</option>
          <option value="anime">Anime</option>
          <option value="manhwa">Manga / Manhwa</option>
          <option value="tv">TV Shows</option>
          <option value="movie">Movies</option>
          <option value="game">Games</option>
          <option value="song">Music & Songs</option>
          <option value="custom_feed">Custom Feeds</option>
        </select>
      </div>

      {filteredList.length === 0 ? (
        <div className="empty-state">
          <Bookmark size={40} />
          <div className="empty-title">No tracked titles here</div>
          <div className="empty-desc">
            Head over to the <strong>Home</strong> tab to search and add your favorite TV shows, anime, movies, and manga.
          </div>
        </div>
      ) : (
        <div className="media-grid">
          {filteredList.map((item) => (
            <div key={item.mediaId} style={{ position: 'relative' }}>
              <MediaCard
                media={item.mediaItem}
                tracked={item}
                onTrack={onTrackMedia}
                onUpdateProgress={onUpdateProgress}
                onTogglePin={onTogglePin}
              />
              <button
                onClick={() => onUntrackMedia(item.mediaId)}
                title="Remove from tracking"
                style={{
                  position: 'absolute',
                  bottom: '1rem',
                  right: '3.75rem',
                  background: 'transparent',
                  border: 'none',
                  color: 'var(--text-muted)',
                  cursor: 'pointer',
                  padding: '0.35rem',
                  display: 'flex',
                  alignItems: 'center',
                }}
              >
                <Trash2 size={14} />
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
