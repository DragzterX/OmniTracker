import { Pin, ExternalLink, Plus, Clock } from 'lucide-react';
import type { MediaItem } from '../../types/media';
import type { UserTrackedItem } from '../../types/storage';

interface MediaCardProps {
  media: MediaItem;
  tracked?: UserTrackedItem;
  matchScore?: number;
  matchReasons?: string[];
  onTrack: (media: MediaItem) => void;
  onUntrack?: (mediaId: string) => void;
  onUpdateProgress?: (mediaId: string, delta: number) => void;
  onTogglePin?: (mediaId: string) => void;
}

export function MediaCard({
  media,
  tracked,
  matchScore,
  matchReasons,
  onTrack,
  onUpdateProgress,
  onTogglePin,
}: MediaCardProps) {
  const isTracked = Boolean(tracked);
  const isPinned = tracked?.isPinned ?? false;
  const currentProgress = tracked?.userProgress ?? 0;

  // Check if unread releases exist
  const hasUnread = isTracked && media.latestReleaseNumber > currentProgress;

  const formatCountdown = (isoString?: string) => {
    if (!isoString) return null;
    const diff = new Date(isoString).getTime() - Date.now();
    if (diff <= 0) return 'Available Now';
    const days = Math.floor(diff / (1000 * 60 * 60 * 24));
    const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    if (days > 0) return `In ${days}d ${hours}h`;
    return `In ${hours}h`;
  };

  const nextCountdown = formatCountdown(media.nextReleaseDate);

  return (
    <div className={`media-card ${isPinned ? 'pinned-card' : ''}`}>
      <div className="card-poster-wrapper">
        <img
          src={media.coverImage || 'https://placehold.co/400x600/18181b/ffffff?text=No+Cover'}
          alt={media.title}
          className="card-poster"
          loading="lazy"
          onError={(e) => {
            (e.target as HTMLImageElement).src = 'https://placehold.co/400x600/18181b/ffffff?text=Image+Unavailable';
          }}
        />

        <div className="card-badge">{media.mediaType.toUpperCase()}</div>

        {media.rank && (
          <div
            style={{
              position: 'absolute',
              top: '0.6rem',
              left: '0.6rem',
              background: media.rank <= 3 ? 'linear-gradient(135deg, #f59e0b, #d97706)' : 'rgba(15, 23, 42, 0.85)',
              color: '#fff',
              fontSize: '0.75rem',
              fontWeight: 800,
              padding: '0.2rem 0.5rem',
              borderRadius: 'var(--radius-sm)',
              boxShadow: '0 2px 6px rgba(0,0,0,0.4)',
              border: '1px solid rgba(255,255,255,0.2)'
            }}
          >
            #{media.rank}
          </div>
        )}

        {isTracked && onTogglePin && (
          <button
            className={`pin-btn ${isPinned ? 'pinned' : ''}`}
            onClick={() => onTogglePin(media.id)}
            title={isPinned ? 'Unpin' : 'Pin to top'}
          >
            <Pin size={14} />
          </button>
        )}

        {matchScore !== undefined && (
          <div
            style={{
              position: 'absolute',
              bottom: '0.6rem',
              left: '0.6rem',
              background: 'rgba(10, 13, 20, 0.85)',
              backdropFilter: 'blur(8px)',
              padding: '0.2rem 0.5rem',
              borderRadius: 'var(--radius-sm)',
              fontSize: '0.72rem',
              fontWeight: 700,
              color: 'var(--accent-secondary)',
              border: '1px solid var(--border-subtle)',
            }}
          >
            {matchScore}% Match
          </div>
        )}
      </div>

      <div className="card-body">
        <h3 className="card-title" title={media.title}>
          {media.title}
        </h3>

        <div className="card-genres">
          {(media.genres || []).slice(0, 3).map((genre) => (
            <span key={genre} className="genre-tag">
              {genre}
            </span>
          ))}
        </div>

        {matchReasons && matchReasons.length > 0 && (
          <div style={{ fontSize: '0.75rem', color: 'var(--accent-secondary)', marginBottom: '0.5rem' }}>
            {matchReasons[0]}
          </div>
        )}

        <div className="release-indicator">
          <div>
            <div className="release-label">Latest:</div>
            <div className="release-val">{media.latestRelease || 'Ongoing'}</div>
          </div>

          {nextCountdown && (
            <div style={{ textAlign: 'right' }}>
              <div className="release-label">Next:</div>
              <div style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--accent-secondary)', display: 'flex', alignItems: 'center', gap: '2px' }}>
                <Clock size={11} /> {nextCountdown}
              </div>
            </div>
          )}
        </div>

        <div className="card-actions">
          {isTracked ? (
            <>
              <div className="progress-control">
                <button
                  className="progress-btn"
                  onClick={() => onUpdateProgress && onUpdateProgress(media.id, -1)}
                  disabled={currentProgress <= 0}
                  title="Previous release"
                >
                  -
                </button>
                <span className="progress-display">
                  {currentProgress} {media.totalReleases ? `/ ${media.totalReleases}` : ''}
                </span>
                <button
                  className="progress-btn"
                  onClick={() => onUpdateProgress && onUpdateProgress(media.id, 1)}
                  title="Next release (+1)"
                >
                  +1
                </button>
              </div>

              {hasUnread && (
                <span
                  style={{
                    fontSize: '0.7rem',
                    fontWeight: 700,
                    color: 'var(--accent-warning)',
                    background: 'rgba(245, 158, 11, 0.1)',
                    padding: '0.2rem 0.4rem',
                    borderRadius: 'var(--radius-sm)',
                    border: '1px solid rgba(245, 158, 11, 0.3)',
                  }}
                >
                  New Release!
                </span>
              )}
            </>
          ) : (
            <button className="btn-primary" onClick={() => onTrack(media)}>
              <Plus size={14} />
              <span>Track</span>
            </button>
          )}

          {media.officialProviders && media.officialProviders.length > 0 && (
            <div style={{ display: 'flex', gap: '0.3rem', alignItems: 'center' }}>
              {media.officialProviders.slice(0, 2).map((prov) => (
                <a
                  key={prov.name}
                  href={prov.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="btn-secondary"
                  style={{ padding: '0.35rem 0.5rem', fontSize: '0.75rem', gap: '0.25rem', whiteSpace: 'nowrap' }}
                  title={`Open on ${prov.name}`}
                >
                  <span>{prov.name}</span>
                  <ExternalLink size={11} />
                </a>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
