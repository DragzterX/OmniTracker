import { useState, type FormEvent } from 'react';
import { Rss, Plus, AlertCircle, Trash2, ExternalLink, Loader2 } from 'lucide-react';
import type { OmniTrackStorage, CustomFeedRecord } from '../types/storage';
import type { MediaItem } from '../types/media';
import { parseFeed } from '../services/api';
import { MediaCard } from '../components/media/MediaCard';

interface AddFeedsPageProps {
  storage: OmniTrackStorage;
  onAddFeed: (feed: CustomFeedRecord) => void;
  onRemoveFeed: (feedId: string) => void;
  onTrackMedia: (media: MediaItem) => void;
  onUpdateProgress: (mediaId: string, delta: number) => void;
}

export function AddFeedsPage({
  storage,
  onAddFeed,
  onRemoveFeed,
  onTrackMedia,
  onUpdateProgress,
}: AddFeedsPageProps) {
  const [feedUrl, setFeedUrl] = useState('');
  const [feedName, setFeedName] = useState('');
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [previewItems, setPreviewItems] = useState<MediaItem[]>([]);

  const handleTestAndAddFeed = async (e: FormEvent) => {
    e.preventDefault();
    if (!feedUrl.trim()) return;

    setLoading(true);
    setErrorMsg(null);
    setPreviewItems([]);

    try {
      const parsed = await parseFeed(feedUrl);
      const name = feedName.trim() || parsed.feedTitle || 'Custom Web Feed';

      const newRecord: CustomFeedRecord = {
        id: `feed_${Date.now()}`,
        name,
        url: feedUrl.trim(),
        mediaType: 'custom_feed',
        lastFetched: new Date().toISOString(),
      };

      onAddFeed(newRecord);
      setPreviewItems(parsed.items);
      setFeedUrl('');
      setFeedName('');
    } catch (err: any) {
      setErrorMsg(err.message || 'Failed to parse RSS/Atom feed. Please check the URL.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <div style={{ marginBottom: '2rem' }}>
        <h1 style={{ fontSize: '1.75rem', fontWeight: 800 }}>Add Search Websites & Custom Feeds</h1>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', marginTop: '0.25rem' }}>
          Connect RSS, Atom, or release blog endpoints from any entertainment website you wish to monitor.
        </p>
      </div>

      <div
        style={{
          background: 'var(--bg-card)',
          border: '1px solid var(--border-subtle)',
          borderRadius: 'var(--radius-lg)',
          padding: '1.5rem',
          maxWidth: '680px',
          marginBottom: '2.5rem',
        }}
      >
        <h2 style={{ fontSize: '1.1rem', fontWeight: 700, marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <Rss size={18} color="var(--accent-primary)" />
          Add New Web Feed Source
        </h2>

        <form onSubmit={handleTestAndAddFeed} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          <div className="form-group">
            <label className="form-label">Feed or Website RSS / Atom URL</label>
            <input
              type="url"
              className="form-input"
              placeholder="https://example.com/feed.xml or https://mywebsite.org/rss"
              value={feedUrl}
              onChange={(e) => setFeedUrl(e.target.value)}
              required
            />
          </div>

          <div className="form-group">
            <label className="form-label">Custom Display Name (Optional)</label>
            <input
              type="text"
              className="form-input"
              placeholder="e.g. Manga Release Updates"
              value={feedName}
              onChange={(e) => setFeedName(e.target.value)}
            />
          </div>

          {errorMsg && (
            <div
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '0.5rem',
                color: 'var(--accent-danger)',
                fontSize: '0.85rem',
                background: 'rgba(239, 68, 68, 0.1)',
                padding: '0.65rem 0.85rem',
                borderRadius: 'var(--radius-sm)',
              }}
            >
              <AlertCircle size={16} />
              <span>{errorMsg}</span>
            </div>
          )}

          <button
            type="submit"
            className="btn-primary"
            disabled={loading}
            style={{ padding: '0.75rem', alignSelf: 'flex-start' }}
          >
            {loading ? (
              <>
                <Loader2 size={16} className="spin" />
                <span>Testing and Fetching Feed...</span>
              </>
            ) : (
              <>
                <Plus size={16} />
                <span>Add & Validate Website</span>
              </>
            )}
          </button>
        </form>
      </div>

      {/* Active Feeds List */}
      <div style={{ marginBottom: '2.5rem' }}>
        <h2 style={{ fontSize: '1.25rem', fontWeight: 700, marginBottom: '1rem' }}>
          Active Custom Websites ({storage.customFeeds.length})
        </h2>

        {storage.customFeeds.length === 0 ? (
          <div style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>
            No custom websites added yet. Add an RSS URL above to automatically track releases from your favorite sites.
          </div>
        ) : (
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: '1rem' }}>
            {storage.customFeeds.map((feed) => (
              <div
                key={feed.id}
                style={{
                  background: 'var(--bg-card)',
                  border: '1px solid var(--border-subtle)',
                  borderRadius: 'var(--radius-md)',
                  padding: '1rem',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                }}
              >
                <div>
                  <div style={{ fontWeight: 600, fontSize: '0.95rem' }}>{feed.name}</div>
                  <div
                    style={{
                      fontSize: '0.75rem',
                      color: 'var(--text-muted)',
                      maxWidth: '220px',
                      overflow: 'hidden',
                      textOverflow: 'ellipsis',
                      whiteSpace: 'nowrap',
                    }}
                  >
                    {feed.url}
                  </div>
                </div>

                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <a
                    href={feed.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="btn-secondary"
                    style={{ padding: '0.4rem' }}
                  >
                    <ExternalLink size={14} />
                  </a>
                  <button
                    className="btn-secondary"
                    onClick={() => onRemoveFeed(feed.id)}
                    style={{ padding: '0.4rem', color: 'var(--accent-danger)' }}
                    title="Remove feed"
                  >
                    <Trash2 size={14} />
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Live Preview of Ingested Feed Items */}
      {previewItems.length > 0 && (
        <div>
          <h2 style={{ fontSize: '1.25rem', fontWeight: 700, marginBottom: '1rem' }}>
            Latest Items from Added Feed ({previewItems.length})
          </h2>
          <div className="media-grid">
            {previewItems.map((item) => (
              <MediaCard
                key={item.id}
                media={item}
                tracked={storage.trackedItems[item.id]}
                onTrack={onTrackMedia}
                onUpdateProgress={onUpdateProgress}
              />
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
