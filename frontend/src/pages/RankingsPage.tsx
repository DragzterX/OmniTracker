import { useState, useEffect } from 'react';
import { Trophy, Globe, Flame, Star, Loader2 } from 'lucide-react';
import type { OmniTrackStorage } from '../types/storage';
import type { MediaItem } from '../types/media';
import { getRankings, type RankingsData } from '../services/api';
import { MediaCard } from '../components/media/MediaCard';

interface RankingsPageProps {
  storage: OmniTrackStorage;
  onTrackMedia: (media: MediaItem) => void;
  onUpdateProgress: (mediaId: string, delta: number) => void;
  onTogglePin: (mediaId: string) => void;
}

const COUNTRIES = [
  { code: 'global', name: 'Worldwide / Global', flag: '🌐' },
  { code: 'jp', name: 'Japan', flag: '🇯🇵' },
  { code: 'kr', name: 'South Korea', flag: '🇰🇷' },
  { code: 'us', name: 'United States', flag: '🇺🇸' },
  { code: 'gb', name: 'United Kingdom', flag: '🇬🇧' },
  { code: 'fr', name: 'France', flag: '🇫🇷' },
  { code: 'de', name: 'Germany', flag: '🇩🇪' },
];

const CATEGORIES = [
  { key: 'all', label: 'All Categories' },
  { key: 'anime', label: 'Anime' },
  { key: 'manhwa', label: 'Manhwa' },
  { key: 'manga', label: 'Manga' },
  { key: 'tv', label: 'TV Shows' },
  { key: 'movie', label: 'Movies' },
  { key: 'game', label: 'Games' },
  { key: 'song', label: 'Music & Songs' },
];

export function RankingsPage({
  storage,
  onTrackMedia,
  onUpdateProgress,
  onTogglePin,
}: RankingsPageProps) {
  const [mode, setMode] = useState<'trending' | 'top_rated'>('trending');
  const [country, setCountry] = useState<string>('global');
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [data, setData] = useState<RankingsData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let isMounted = true;
    async function loadData() {
      setLoading(true);
      const res = await getRankings(mode, country);
      if (isMounted) {
        setData(res);
        setLoading(false);
      }
    }
    loadData();
    return () => {
      isMounted = false;
    };
  }, [mode, country]);

  // Combine items according to selected category
  const getDisplayItems = (): MediaItem[] => {
    if (!data) return [];
    if (selectedCategory === 'anime') return data.anime;
    if (selectedCategory === 'tv') return data.tv;
    if (selectedCategory === 'movie') return data.movie;
    if (selectedCategory === 'manga') return data.manga;
    if (selectedCategory === 'manhwa') return data.manhwa;
    if (selectedCategory === 'game') return data.game;
    if (selectedCategory === 'song') return data.song;

    // 'all': Interleave top items from each category
    const maxItems = Math.max(
      data.anime.length,
      data.tv.length,
      data.movie.length,
      data.manga.length,
      data.manhwa.length,
      data.game.length,
      data.song.length
    );
    const combined: MediaItem[] = [];
    for (let i = 0; i < maxItems; i++) {
      if (data.anime[i]) combined.push(data.anime[i]);
      if (data.tv[i]) combined.push(data.tv[i]);
      if (data.movie[i]) combined.push(data.movie[i]);
      if (data.manhwa[i]) combined.push(data.manhwa[i]);
      if (data.game[i]) combined.push(data.game[i]);
      if (data.song[i]) combined.push(data.song[i]);
      if (data.manga[i]) combined.push(data.manga[i]);
    }
    return combined;
  };

  const displayItems = getDisplayItems();

  return (
    <div>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1.5rem', flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <h1 style={{ fontSize: '1.75rem', fontWeight: 800, display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
            <Trophy size={26} color="#f59e0b" />
            <span>Global Media Rankings</span>
          </h1>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', marginTop: '0.25rem' }}>
            Live aggregated leaderboards across legal streaming, broadcast, and gaming platforms.
          </p>
        </div>

        {/* Controls: Mode & Country */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', flexWrap: 'wrap' }}>
          {/* Mode toggle */}
          <div style={{ display: 'flex', background: 'var(--bg-card)', padding: '0.25rem', borderRadius: 'var(--radius-md)', border: '1px solid var(--border-subtle)' }}>
            <button
              type="button"
              className={`chip ${mode === 'trending' ? 'active' : ''}`}
              style={{ padding: '0.35rem 0.75rem', fontSize: '0.8rem', display: 'flex', alignItems: 'center', gap: '0.3rem', border: 'none' }}
              onClick={() => setMode('trending')}
            >
              <Flame size={14} />
              <span>Trending</span>
            </button>
            <button
              type="button"
              className={`chip ${mode === 'top_rated' ? 'active' : ''}`}
              style={{ padding: '0.35rem 0.75rem', fontSize: '0.8rem', display: 'flex', alignItems: 'center', gap: '0.3rem', border: 'none' }}
              onClick={() => setMode('top_rated')}
            >
              <Star size={14} />
              <span>Top Rated</span>
            </button>
          </div>

          {/* Country selector */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
            <Globe size={16} color="var(--text-muted)" />
            <select
              id="rankings-country-select"
              className="form-select"
              value={country}
              onChange={(e) => setCountry(e.target.value)}
              style={{ fontWeight: 600, minWidth: '150px' }}
            >
              {COUNTRIES.map((c) => (
                <option key={c.code} value={c.code}>
                  {c.flag} {c.name}
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* Category Filter Chips */}
      <div className="filter-chips" style={{ marginBottom: '1.75rem', justifyContent: 'flex-start' }}>
        {CATEGORIES.map((cat) => (
          <button
            key={cat.key}
            type="button"
            className={`chip ${selectedCategory === cat.key ? 'active' : ''}`}
            onClick={() => setSelectedCategory(cat.key)}
          >
            {cat.label}
          </button>
        ))}
      </div>

      {loading ? (
        <div style={{ display: 'flex', justifyContent: 'center', padding: '4rem' }}>
          <Loader2 size={36} className="spin" color="var(--accent-primary)" />
        </div>
      ) : displayItems.length === 0 ? (
        <div className="empty-state">
          <Trophy size={40} />
          <div className="empty-title">No ranking items available</div>
          <div className="empty-desc">Check your connection or try another country / category filter.</div>
        </div>
      ) : (
        <div className="media-grid">
          {displayItems.map((item) => (
            <MediaCard
              key={`${item.mediaType}_${item.id}`}
              media={item}
              tracked={storage.trackedItems[item.id]}
              onTrack={onTrackMedia}
              onUpdateProgress={onUpdateProgress}
              onTogglePin={onTogglePin}
            />
          ))}
        </div>
      )}
    </div>
  );
}
