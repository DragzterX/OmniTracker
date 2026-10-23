# OmniTracker — Comprehensive Project Reference & File Guide

## 1. Project Summaries

### What It's About (4 lines max)
OmniTracker is a local-first, zero-database entertainment tracker that consolidates release schedules, watch progress, and rankings across TV Shows, Anime, Movies, Manga, Manhwa, Games, and Music. It is built with zero user tracking and eliminates centralized databases. All user watchlists, progress counters, and custom RSS feeds are stored exclusively on the user's local disk in a clean `omnitrack_data.json` file.

### What Is Done Here (4 lines max)
A complete, functioning full-stack application is implemented with a Python FastAPI asynchronous backend gateway and a React 19 + TypeScript frontend. The backend integrates legal media APIs (AniList, MangaDex, TMDB, RAWG/Steam, iTunes) and a custom RSS/Atom feed parser with in-memory TTL caching. The frontend implements browser File System Access API syncing, zero-server local recommendation scoring, and a modern dark-mode glassmorphic UI.

### What Can a User Do With This Website?
- **Unified Omni-Search**: Concurrently search across 7 media categories (Anime, Manga, Manhwa, TV Shows, Movies, Video Games, Music/Songs) with category chip filters.
- **Track Watch & Read Progress**: Add any media to a personal profile, update completed episodes/chapters using instant `+1` / `-1` steppers, and see unread release badges when new content is out.
- **View Upcoming Airing & Chapter Schedules**: Open a built-in calendar schedule showing countdowns and dates for upcoming releases of all currently bookmarked titles.
- **Explore Live Leaderboards & Regional Rankings**: Browse Top 10 charts toggled between "Trending" and "Top Rated", filterable by global market or specific countries (Japan, South Korea, United States, United Kingdom, France, Germany).
- **Direct Legal Provider Routing**: Access 5 to 10 verified legal streaming, reading, gaming, and listening links for every title (Crunchyroll, Netflix, MangaDex, MangaPlus, Steam, Spotify, Apple Music, etc.).
- **Add Custom Website Feeds**: Ingest any arbitrary website RSS or Atom feed URL to track custom webcomics, scanlation sites, or blog announcements alongside official releases.
- **Privacy-Preserving Personalized Recommendations**: Receive tailored suggestions calculated 100% locally in the browser by analyzing personal genre frequency and media affinities without sending data to any external server.
- **Flexible Local Storage Control**: Save directly to disk via the native browser File System Access API (`omnitrack_data.json`), fallback to LocalStorage, enter temporary Guest Mode, or export/import JSON backups anytime.

---

## 2. Languages & Technologies Used

- **Python (v3.12+)**: Backend API service, async HTTP fetching, RSS parsing, data normalization, and Pydantic models.
- **TypeScript**: Frontend application logic, strict type contracts matching backend models, and client-side scoring algorithms.
- **JavaScript**: Build system tooling (Vite configuration) and production browser runtime bundles.
- **HTML5**: Web application entry point (`index.html`), structural markup, metadata, and SVG vector elements.
- **CSS3 / Vanilla CSS**: Custom properties (CSS variables), responsive layouts, CSS Grid/Flexbox, and glassmorphism styling.
- **Windows Batch Script (`.bat`)**: Dev environment automation script (`scripts/start_dev.bat`) for one-click launching.
- **JSON / JSONC**: Project configuration (`package.json`, `tsconfig.json`, `.oxlintrc.json`) and portable user data schema (`omnitrack_data.json`).
- **Markdown (`.md`)**: Project documentation, architectural plans, and guides.
- **SVG (Scalable Vector Graphics)**: App icons, favicons, and graphic sprites.

---

## 3. Complete File & Folder Structure Guide

Every single directory and file in the project is cataloged below with a concise summary of its purpose.

```
OmniTracker/
│
├── OmniTracker.exe                              # Standalone Windows native desktop executable; double-click to launch the app window.
├── desktop_app.py                               # Desktop app controller; launches FastAPI in background thread and runs Edge WebView2 window.
├── launcher.cs                                  # C# source code for compiling the zero-console Windows native launcher OmniTracker.exe.
├── icon.ico                                     # Application multi-resolution icon embedded into OmniTracker.exe and window title bar.
├── README.md                                    # Main documentation covering architecture, features, quick start, and setup.
│
├── docs/                                        # Design specifications and project notes.
│   ├── PROJECT_DETAILS.md                       # Comprehensive file-by-file reference guide and project blueprint (this file).
│   ├── Project_idea.txt                         # Original project requirements, initial vision, and roadmap brainstorm.
│   └── project_plan_antigrav                    # Detailed architectural engineering plan and technical evaluation.
│
├── scripts/                                     # Automation and environment scripts.
│   └── start_dev.bat                            # Windows batch script for development mode (Vite HMR + browser).
│
├── backend/                                     # Python FastAPI service & external API gateway.
│   ├── .env                                     # Environment variables file for local secrets (e.g. TMDB_API_KEY, ports).
│   ├── .env.example                             # Template environment file showing available configuration keys.
│   ├── requirements.txt                         # Python package dependencies (FastAPI, Uvicorn, HTTPX, Pydantic, Feedparser).
│   │
│   ├── .venv/                                   # Python virtual environment containing runtime and dependencies.
│   │   ├── pyvenv.cfg                           # Virtual environment configuration file detailing Python version and base path.
│   │   ├── Include/                             # Directory for C/C++ header files for compiled Python packages (empty).
│   │   ├── Lib/                                 # Python library directory.
│   │   │   └── site-packages/                   # [External packages directory - file contents omitted per instruction].
│   │   └── Scripts/                             # Virtual environment executables and CLI tools:
│   │       ├── activate                         # Unix/bash activation script for virtual environment.
│   │       ├── activate.bat                     # Windows CMD script to activate virtual environment.
│   │       ├── Activate.ps1                     # PowerShell script to activate virtual environment.
│   │       ├── deactivate.bat                   # Windows CMD script to deactivate virtual environment.
│   │       ├── dotenv.exe                       # CLI tool for reading and manipulating .env files.
│   │       ├── fastapi.exe                      # Command-line utility for FastAPI project management.
│   │       ├── httpx.exe                        # Command-line async HTTP client tool.
│   │       ├── idna.exe                         # Internationalized Domain Names utility executable.
│   │       ├── pip.exe                          # Python package installer executable.
│   │       ├── pip3.exe                         # Python 3 package installer alias.
│   │       ├── pip3.12.exe                      # Python 3.12 specific package installer executable.
│   │       ├── python.exe                       # Python runtime interpreter executable for this virtual environment.
│   │       ├── pythonw.exe                      # Windowless Python interpreter for running background scripts.
│   │       ├── uvicorn.exe                      # Lightning-fast ASGI web server executable running the FastAPI app.
│   │       ├── watchfiles.exe                   # File change watcher CLI used for automatic reload on code edits.
│   │       └── websockets.exe                   # Command-line utility for WebSocket testing.
│   │
│   └── app/                                     # Core backend application package.
│       ├── __init__.py                          # Package initializer marking backend/app as a Python package.
│       ├── main.py                              # FastAPI application root; registers routers, CORS middleware, and health route.
│       │
│       ├── core/                                # Application configuration and core settings.
│       │   ├── __init__.py                      # Package initializer for core settings module.
│       │   └── config.py                        # Pydantic Settings class loading environment variables and API URLs.
│       │
│       ├── models/                              # Data models and Pydantic validation schemas.
│       │   ├── __init__.py                      # Package initializer exposing data models.
│       │   ├── media.py                         # Unified schemas: MediaItem, MediaType, ProviderLink, and SearchResponse.
│       │   └── user_data.py                     # Storage schemas: UserTrackedItem, CustomFeedRecord, and OmniTrackStorage.
│       │
│       ├── services/                            # Connectors to third-party APIs and ingestion engines.
│       │   ├── __init__.py                      # Package initializer exposing service functions.
│       │   ├── anilist_service.py               # AniList GraphQL client for anime search, trending lists, and airing dates.
│       │   ├── mangadex_service.py              # MangaDex REST client for manga/manhwa search, chapter counts, and cover art.
│       │   ├── tmdb_service.py                  # The Movie Database (TMDB) client for TV shows/movies with fallback mock data.
│       │   ├── games_service.py                 # RAWG / Steam game search and leaderboard aggregator with fallback items.
│       │   ├── music_service.py                 # iTunes / Apple Music search service for songs, albums, and rankings.
│       │   ├── feed_service.py                  # RSS / Atom feed scraper and parser using feedparser and httpx.
│       │   ├── providers.py                     # Generator of 5-10 verified legal streaming and reading links for media items.
│       │   └── cache.py                         # In-memory TTL cache to prevent exceeding third-party API rate limits.
│       │
│       ├── api/                                 # REST API route controllers.
│       │   ├── __init__.py                      # Package initializer exposing API router controllers.
│       │   ├── search.py                        # Universal search endpoint querying all media services concurrently.
│       │   ├── recommendations.py               # Endpoints for global/regional rankings and trending recommendations.
│       │   ├── releases.py                      # Server time and release schedule synchronization endpoint.
│       │   └── feeds.py                         # Custom RSS/Atom feed parsing and testing endpoint.
│       │
│       └── __pycache__/                         # Compiled Python bytecode cache files (auto-generated by runtime).
│           ├── core/__pycache__/                # Bytecode for configuration modules.
│           ├── models/__pycache__/              # Bytecode for schema validation models.
│           ├── services/__pycache__/            # Bytecode for external service connectors.
│           └── api/__pycache__/                 # Bytecode for API routers.
│
└── frontend/                                    # Vite + React 19 + TypeScript web application.
    ├── .gitignore                               # Specifies untracked frontend files (node_modules, dist, .env).
    ├── .oxlintrc.json                           # Configuration file for Oxlint high-performance JS/TS linter.
    ├── index.html                               # Main HTML entry point configuring viewport, Google Fonts, and root container.
    ├── package.json                             # NPM package manifest with dependencies (React, Lucide icons) and scripts.
    ├── package-lock.json                        # Exact dependency lockfile ensuring reproducible npm installations.
    ├── README.md                                # Frontend-specific development documentation.
    ├── tsconfig.json                            # Root TypeScript configuration referencing app and node configs.
    ├── tsconfig.app.json                        # TypeScript compiler options for React UI source code under src/.
    ├── tsconfig.node.json                       # TypeScript compiler options for Vite config and build scripts.
    ├── vite.config.ts                           # Vite configuration file setting up React plugin and /api proxy to FastAPI.
    │
    ├── node_modules/                            # Installed NPM dependencies directory (managed by npm install).
    │
    ├── public/                                  # Static assets served as-is at web root:
    │   ├── favicon.svg                          # Modern glowing radar icon used as browser tab favicon.
    │   └── icons.svg                            # SVG sprite definitions for logos and symbols.
    │
    ├── dist/                                    # Production build output generated by 'npm run build':
    │   ├── index.html                           # Minified production HTML entry point.
    │   ├── favicon.svg                          # Bundled favicon asset.
    │   ├── icons.svg                            # Bundled vector sprite asset.
    │   └── assets/                              # Compiled and optimized production bundles:
    │       ├── index-C4i_ULnW.css               # Minified and prefixed global production CSS stylesheet.
    │       └── index-Cui2S4-K.js                # Minified and bundled production JavaScript application code.
    │
    └── src/                                     # Frontend React application source code:
        ├── App.css                              # Minimal styling for main application wrapper.
        ├── App.tsx                              # Main React component managing active tab, storage state, and tracker events.
        ├── index.css                            # CSS base styles and font defaults.
        ├── main.tsx                             # Application bootstrapping file rendering App into document DOM.
        │
        ├── assets/                              # Graphical assets:
        │   ├── hero.png                         # OmniTracker banner / hero illustration.
        │   ├── react.svg                        # React official logo SVG asset.
        │   └── vite.svg                         # Vite official logo SVG asset.
        │
        ├── styles/                              # Design system stylesheets:
        │   ├── variables.css                    # Design tokens: CSS variables for colors, dark mode, radii, and glassmorphism.
        │   └── global.css                       # Comprehensive UI stylesheet (buttons, cards, grids, modals, scrollbars).
        │
        ├── types/                               # TypeScript interface contracts:
        │   ├── media.ts                         # Type definitions for MediaItem, MediaType, ProviderLink, and SearchResponse.
        │   └── storage.ts                       # Type definitions for OmniTrackStorage, UserTrackedItem, and CustomFeedRecord.
        │
        ├── services/                            # Client-side business logic and data providers:
        │   ├── api.ts                           # HTTP client communicating with backend FastAPI endpoints.
        │   ├── storage.ts                       # File System Access API handler, LocalStorage fallback, and JSON export/import.
        │   └── recommendation_engine.ts         # Zero-server local recommendation algorithm matching personal user taste.
        │
        ├── components/                          # Reusable UI component library:
        │   ├── layout/                          # Layout and navigation components:
        │   │   └── Navbar.tsx                   # Top header navbar with navigation tabs and storage status button.
        │   ├── media/                           # Media presentation components:
        │   │   └── MediaCard.tsx                # Card displaying poster, progress stepper, unread badge, and provider links.
        │   └── storage/                         # Storage management components:
        │       └── StorageModal.tsx             # Modal for linking local file, switching to Guest Mode, or importing JSON.
        │
        └── pages/                               # Primary view pages (tabs):
            ├── HomePage.tsx                     # Centered Google-style search dashboard with quick category filter chips.
            ├── ProfileTrackerPage.tsx           # Watchlist tracker with progress steppers, unread badges, and schedule calendar.
            ├── RankingsPage.tsx                 # Global and country-level Top 10 leaderboards across all media categories.
            ├── RecommendationsPage.tsx          # Local taste-based recommendation discovery page.
            └── AddFeedsPage.tsx                 # Custom RSS/Atom feed manager for adding and testing external websites.
```

---

## 4. Suggestions for Changes & Future Improvements

Here are key architectural and feature enhancements recommended to elevate OmniTracker into an even more powerful, seamless product:

### 1. In-App TMDB API Key & Settings Configuration UI
- **Current State**: Users must manually edit `backend/.env` to provide a TMDB API key.
- **Improvement**: Add a small "Settings" modal or tab in the frontend where users can paste their TMDB API key (or RAWG key), storing it locally in `omnitrack_data.json` or passing it to the backend via headers. This keeps the app completely zero-config for non-technical users.

### 2. Automated Background Release Polling & Desktop Notifications
- **Current State**: The schedule and release checks occur when the user opens the page or navigates tabs.
- **Improvement**: Implement an optional background polling timer (e.g., every 30 or 60 minutes) that checks for new chapters/episodes of pinned titles and triggers native browser notifications (`Notification.requestPermission()`) when an unread release drops.

### 3. Native Desktop Shell (OmniTracker.exe) [COMPLETED]
- **Implemented**: Built a native Windows desktop executable `OmniTracker.exe` in the root folder using Microsoft Edge WebView2 and a zero-console C# native launcher.
- **Benefits**: Double-clicking `OmniTracker.exe` immediately opens a dedicated desktop app window without opening any black CMD/terminal windows, running the FastAPI backend silently in the background and loading the full React interface directly.

### 4. Import / Export Integrations (AniList, MyAnimeList, Trakt)
- **Current State**: Users currently search and add titles manually.
- **Improvement**: Add a 1-click import feature supporting standard XML or JSON export files from MyAnimeList, AniList, or Trakt.tv. This allows users to migrate existing libraries with hundreds of shows in seconds.

### 5. Offline Progressive Web App (PWA) Caching
- **Current State**: If the backend is closed, searches fail and fallback data is not cached on the frontend.
- **Improvement**: Register a Service Worker in Vite with `vite-plugin-pwa` to cache recent search responses and images locally via IndexedDB. This ensures users can view their profile and read past notes even when completely offline.

### 6. Interactive Toast Notifications & Error Boundaries
- **Current State**: Some network errors log to the browser console or use inline error banners.
- **Improvement**: Add an interactive toast notification system (e.g. lightweight custom toasts) to provide instant visual feedback when items are pinned, progress is saved to disk, or an invalid RSS feed URL is tested.
