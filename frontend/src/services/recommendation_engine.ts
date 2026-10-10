import type { MediaItem } from '../types/media';
import type { UserTrackedItem } from '../types/storage';

export interface ScoredMediaItem extends MediaItem {
  matchScore: number;
  matchReasons: string[];
  isAlreadyTracked: boolean;
}

export function generateLocalRecommendations(
  candidates: MediaItem[],
  trackedItems: Record<string, UserTrackedItem>
): ScoredMediaItem[] {
  const trackedList = Object.values(trackedItems);
  
  // 1. Build user genre frequency profile
  const genreFrequency: Record<string, number> = {};
  const mediaTypeFrequency: Record<string, number> = {};
  const trackedIds = new Set(Object.keys(trackedItems));

  for (const item of trackedList) {
    const m = item.mediaItem;
    mediaTypeFrequency[m.mediaType] = (mediaTypeFrequency[m.mediaType] || 0) + 1;
    
    for (const g of m.genres || []) {
      const normalizedGenre = g.trim().toLowerCase();
      genreFrequency[normalizedGenre] = (genreFrequency[normalizedGenre] || 0) + 1;
    }
  }

  const totalTracked = trackedList.length;

  return candidates.map((candidate) => {
    let score = 50; // Base score for trending items
    const matchReasons: string[] = [];
    const isAlreadyTracked = trackedIds.has(candidate.id);

    if (totalTracked > 0) {
      // MediaType affinity
      const typeCount = mediaTypeFrequency[candidate.mediaType] || 0;
      if (typeCount > 0) {
        const typeBonus = Math.min(20, Math.round((typeCount / totalTracked) * 20));
        score += typeBonus;
        matchReasons.push(`Matches your interest in ${candidate.mediaType.toUpperCase()}`);
      }

      // Genre affinities
      const matchedGenres: string[] = [];
      for (const g of candidate.genres || []) {
        const normalized = g.trim().toLowerCase();
        if (genreFrequency[normalized]) {
          matchedGenres.push(g);
          score += 10;
        }
      }

      if (matchedGenres.length > 0) {
        matchReasons.push(`Shares genres: ${matchedGenres.slice(0, 3).join(', ')}`);
      }
    } else {
      matchReasons.push('Trending globally');
    }

    // High rating bonus
    if (candidate.score && candidate.score >= 8.0) {
      score += 10;
      matchReasons.push(`Top rated (${candidate.score.toFixed(1)}/10)`);
    }

    // Clamp score between 0 and 99
    score = Math.min(99, Math.max(10, score));

    return {
      ...candidate,
      matchScore: score,
      matchReasons,
      isAlreadyTracked,
    };
  }).sort((a, b) => {
    // Show untracked items first, ordered by matchScore
    if (a.isAlreadyTracked !== b.isAlreadyTracked) {
      return a.isAlreadyTracked ? 1 : -1;
    }
    return b.matchScore - a.matchScore;
  });
}
