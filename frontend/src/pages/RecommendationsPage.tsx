import { useState, useEffect } from 'react';
import { Compass, Filter, Loader2 } from 'lucide-react';
import type { OmniTrackStorage } from '../types/storage';
import type { MediaItem } from '../types/media';
import { getRecommendations } from '../services/api';
import { generateLocalRecommendations, type ScoredMediaItem } from '../services/recommendation_engine';
import { MediaCard } from '../components/media/MediaCard';

interface RecommendationsPageProps {
  storage: OmniTrackStorage;
  onTrackMedia: (media: MediaItem) => void;
  onUpdateProgress: (mediaId: string, delta: number) => void;
  onTogglePin: (mediaId: string) => void;
}

export function RecommendationsPage({
  storage,
  onTrackMedia,
  onUpdateProgress,
  onTogglePin,
}: RecommendationsPageProps) {
  const [selectedMediaType, setSelectedMediaType] = useState<string>('all');
  const [loading, setLoading] = useState(false);
  const [recommendations, setRecommendations] = useState<ScoredMediaItem[]>([]);

  useEffect(() => {
    let isMounted = true;
    async function fetchAndScore() {
      setLoading(true);
      try {
        const rawItems = await getRecommendations(selectedMediaType);
        if (isMounted) {
          // Zero-Server Local Recommendation Logic
          const scored = generateLocalRecommendations(rawItems, storage.trackedItems);
          setRecommendations(scored);
        }
      } catch (err) {
        console.error('Failed to generate recommendations:', err);
      } finally {
        if (isMounted) setLoading(false);
      }
    }

    fetchAndScore();
    return () => {
      isMounted = false;
    };
  }, [selectedMediaType, storage.trackedItems]);

  const trackedCount = Object.keys(storage.trackedItems).length;

  return (
    <div>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1.5rem', flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <h1 style={{ fontSize: '1.75rem', fontWeight: 800, display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <span>Personalized Recommendations</span>
          </h1>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', marginTop: '0.25rem' }}>
            {trackedCount > 0
              ? `Calculated on-device matching your ${trackedCount} bookmarked titles and genre preferences.`
              : 'Add items in your Profile to get personalized genre affinity matches.'}
          </p>
        </div>

        {/* Dropdown Menu to choose media to see */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <Filter size={16} color="var(--text-muted)" />
          <select
            id="recommendation-media-filter"
            className="form-select"
            value={selectedMediaType}
            onChange={(e) => setSelectedMediaType(e.target.value)}
            style={{ fontWeight: 600, minWidth: '160px' }}
          >
            <option value="all">All Media</option>
            <option value="anime">Anime Only</option>
            <option value="manhwa">Manga & Manhwa</option>
            <option value="tv">TV Shows</option>
            <option value="movie">Movies</option>
            <option value="game">Games</option>
            <option value="song">Music & Songs</option>
          </select>
        </div>
      </div>

      {loading ? (
        <div style={{ display: 'flex', justifyContent: 'center', padding: '4rem' }}>
          <Loader2 size={36} className="spin" color="var(--accent-primary)" />
        </div>
      ) : recommendations.length === 0 ? (
        <div className="empty-state">
          <Compass size={40} />
          <div className="empty-title">No recommendations available right now</div>
          <div className="empty-desc">Ensure the backend API proxy is active to pull trending catalog updates.</div>
        </div>
      ) : (
        <div className="media-grid">
          {recommendations.map((item) => (
            <MediaCard
              key={item.id}
              media={item}
              tracked={storage.trackedItems[item.id]}
              matchScore={item.matchScore}
              matchReasons={item.matchReasons}
              onTrack={onTrackMedia}
              onUpdateProgress={onUpdateProgress}
              onTogglePin={onTogglePin}
            />
          ))}
        </div>
      )}
    </div>
  );
};
