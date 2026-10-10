import { useState, useEffect, type FormEvent } from 'react';
import { Search, Loader2 } from 'lucide-react';
import type { MediaItem } from '../types/media';
import type { OmniTrackStorage } from '../types/storage';
import { searchMedia, getRecommendations } from '../services/api';
import { MediaCard } from '../components/media/MediaCard';

interface HomePageProps {
  storage: OmniTrackStorage;
  onTrackMedia: (media: MediaItem) => void;
  onUpdateProgress: (mediaId: string, delta: number) => void;
  onTogglePin: (mediaId: string) => void;
}

export function HomePage({
  storage,
  onTrackMedia,
  onUpdateProgress,
  onTogglePin,
}: HomePageProps) {
  const [query, setQuery] = useState('');
  const [activeFilter, setActiveFilter] = useState<'all' | 'anime' | 'manhwa' | 'tv' | 'movie' | 'game' | 'song'>('all');
  const [items, setItems] = useState<MediaItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [isSearching, setIsSearching] = useState(false);

  // Load trending spotlight on mount if no search query
  useEffect(() => {
    let isMounted = true;
    async function loadTrending() {
      setLoading(true);
      const data = await getRecommendations(activeFilter);
      if (isMounted) {
        setItems(data.slice(0, 12));
        setLoading(false);
      }
    }
    if (!query.trim()) {
      setIsSearching(false);
      loadTrending();
    }
    return () => {
      isMounted = false;
    };
  }, [activeFilter, query]);

  const handleSearch = async (e?: FormEvent) => {
    if (e) e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    setIsSearching(true);
    const results = await searchMedia(query, activeFilter);
    setItems(results);
    setLoading(false);
  };

  const filterChips = [
    { label: 'All Media', value: 'all' },
    { label: 'Anime', value: 'anime' },
    { label: 'Manga / Manhwa', value: 'manhwa' },
    { label: 'TV Shows', value: 'tv' },
    { label: 'Movies', value: 'movie' },
    { label: 'Games', value: 'game' },
    { label: 'Music & Songs', value: 'song' },
  ];

  return (
    <div>
      <div className="home-hero">
        <h1 className="home-logo-large">OmniTracker</h1>
        <p className="home-subtitle">
          Instant release schedules for TV Shows, Anime, Movies, Manga, Games, and Music. Stored securely on your device.
        </p>

        <form className="search-box-wrapper" onSubmit={handleSearch}>
          <div className="search-input-group">
            <Search className="search-icon" size={20} />
            <input
              id="omni-search-input"
              type="text"
              className="search-input"
              placeholder="Search your media..."
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              autoComplete="off"
            />
            <button type="submit" className="search-submit-btn">
              Search
            </button>
          </div>

          <div className="filter-chips">
            {filterChips.map((chip) => (
              <button
                key={chip.value}
                type="button"
                className={`chip ${activeFilter === chip.value ? 'active' : ''}`}
                onClick={() => setActiveFilter(chip.value as any)}
              >
                {chip.label}
              </button>
            ))}
          </div>
        </form>
      </div>

      <div style={{ marginTop: '2rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1rem' }}>
          <h2 style={{ fontSize: '1.25rem', fontWeight: 700 }}>
            {isSearching ? `Search Results for "${query}"` : 'Trending Releases'}
          </h2>
          <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>
            {items.length} {items.length === 1 ? 'title' : 'titles'} found
          </span>
        </div>

        {loading ? (
          <div style={{ display: 'flex', justifyContent: 'center', padding: '3rem' }}>
            <Loader2 size={32} className="spin" color="var(--accent-primary)" />
          </div>
        ) : items.length === 0 ? (
          <div className="empty-state">
            <Search size={40} />
            <div className="empty-title">No releases found</div>
            <div className="empty-desc">
              Try searching with a different keyword or select another category filter.
            </div>
          </div>
        ) : (
          <div className="media-grid">
            {items.map((media) => (
              <MediaCard
                key={media.id}
                media={media}
                tracked={storage.trackedItems[media.id]}
                onTrack={onTrackMedia}
                onUpdateProgress={onUpdateProgress}
                onTogglePin={onTogglePin}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
