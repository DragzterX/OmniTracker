import { useRef } from 'react';
import { X, HardDrive, Download, Upload, Shield } from 'lucide-react';
import type { OmniTrackStorage, StorageStatus } from '../../types/storage';
import {
  linkExistingLocalFile,
  createNewLocalFile,
  exportDataAsJson,
  parseImportedJson,
  isFileSystemApiSupported,
} from '../../services/storage';

interface StorageModalProps {
  isOpen: boolean;
  onClose: () => void;
  storage: OmniTrackStorage;
  storageStatus: StorageStatus;
  onStorageUpdated: (newData: OmniTrackStorage) => void;
  onToggleGuestMode: (guest: boolean) => void;
}

export function StorageModal({
  isOpen,
  onClose,
  storage,
  storageStatus,
  onStorageUpdated,
  onToggleGuestMode,
}: StorageModalProps) {
  const fileInputRef = useRef<HTMLInputElement>(null);

  if (!isOpen) return null;

  const handleLinkFile = async () => {
    try {
      const data = await linkExistingLocalFile();
      if (data) {
        onStorageUpdated(data);
      }
    } catch (err: any) {
      alert(err.message || 'Failed to link local file.');
    }
  };

  const handleCreateFile = async () => {
    try {
      const success = await createNewLocalFile(storage);
      if (success) {
        alert('Successfully linked and saved omnitrack_data.json to your selected folder!');
      }
    } catch (err: any) {
      alert(err.message || 'Failed to create local file.');
    }
  };

  const handleExport = () => {
    exportDataAsJson(storage);
  };

  const handleImportFile = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (event) => {
      try {
        const text = event.target?.result as string;
        const parsed = parseImportedJson(text);
        onStorageUpdated(parsed);
        alert(`Successfully imported ${Object.keys(parsed.trackedItems).length} tracked items!`);
      } catch (err) {
        alert('Invalid JSON file format.');
      }
    };
    reader.readAsText(file);
    e.target.value = '';
  };

  const isFsSupported = isFileSystemApiSupported();

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-card" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <HardDrive size={20} color="var(--accent-primary)" />
            <h2 className="modal-title">Local Storage & File Persistence</h2>
          </div>
          <button className="close-btn" onClick={onClose}>
            <X size={20} />
          </button>
        </div>

        <div style={{ fontSize: '0.875rem', color: 'var(--text-secondary)', lineHeight: 1.6 }}>
          OmniTracker uses a <strong>zero-database architecture</strong>. All your tracked shows, anime, manga, and custom web feeds are saved directly onto your device.
        </div>

        <div
          style={{
            background: 'var(--bg-card)',
            padding: '1rem',
            borderRadius: 'var(--radius-md)',
            border: '1px solid var(--border-subtle)',
            display: 'flex',
            flexDirection: 'column',
            gap: '0.5rem',
            fontSize: '0.85rem',
          }}
        >
          <div style={{ display: 'flex', justifyContent: 'space-between' }}>
            <span style={{ color: 'var(--text-secondary)' }}>Current Mode:</span>
            <strong style={{ color: 'var(--text-primary)' }}>
              {storageStatus.mode === 'local_file'
                ? 'Linked to Local omnitrack_data.json'
                : storageStatus.mode === 'guest'
                ? 'Guest Mode (No Saving)'
                : 'Browser Storage (Local Cache)'}
            </strong>
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between' }}>
            <span style={{ color: 'var(--text-secondary)' }}>Tracked Items:</span>
            <span>{Object.keys(storage.trackedItems).length} items</span>
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between' }}>
            <span style={{ color: 'var(--text-secondary)' }}>Last Saved:</span>
            <span>{new Date(storage.lastModified).toLocaleTimeString()}</span>
          </div>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
          {isFsSupported ? (
            <>
              <button className="btn-primary" onClick={handleLinkFile} style={{ width: '100%', padding: '0.75rem' }}>
                <HardDrive size={16} />
                <span>Choose Existing omnitrack_data.json</span>
              </button>

              <button className="btn-secondary" onClick={handleCreateFile} style={{ width: '100%', padding: '0.75rem' }}>
                <Download size={16} />
                <span>Create New omnitrack_data.json on Disk</span>
              </button>
            </>
          ) : (
            <div style={{ color: 'var(--accent-warning)', fontSize: '0.8rem' }}>
              Direct disk file link requires Chrome, Edge, or Brave. You can use JSON Export / Import below.
            </div>
          )}

          <div style={{ display: 'flex', gap: '0.5rem', marginTop: '0.25rem' }}>
            <button className="btn-secondary" onClick={handleExport} style={{ flex: 1, padding: '0.65rem' }}>
              <Download size={15} />
              <span>Export JSON Backup</span>
            </button>

            <button
              className="btn-secondary"
              onClick={() => fileInputRef.current?.click()}
              style={{ flex: 1, padding: '0.65rem' }}
            >
              <Upload size={15} />
              <span>Import JSON File</span>
            </button>
            <input
              ref={fileInputRef}
              type="file"
              accept=".json"
              style={{ display: 'none' }}
              onChange={handleImportFile}
            />
          </div>

          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              paddingTop: '0.75rem',
              borderTop: '1px solid var(--border-subtle)',
              marginTop: '0.25rem',
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <Shield size={16} color="var(--text-muted)" />
              <span style={{ fontSize: '0.85rem' }}>Guest Mode (temporary session)</span>
            </div>
            <input
              type="checkbox"
              checked={storage.settings.guestMode}
              onChange={(e) => onToggleGuestMode(e.target.checked)}
              style={{ width: '18px', height: '18px', cursor: 'pointer' }}
            />
          </div>
        </div>
      </div>
    </div>
  );
}
