# Phase 3: PWA Features Implementation Plan

**Status**: Ready for Implementation
**Estimated Time**: 8-16 hours (8-13 hours required, +2-3 hours optional)
**Expected Impact**: Instant UI loading, offline functionality, 50-90% faster perceived performance
**Risk Level**: MEDIUM (service worker misconfiguration can break app)
**Prerequisites**: Phase 1 and Phase 2 completed (recommended but not required)

---

## Overview

### Objectives

Transform the Market Parser Gradio PWA into a fully optimized Progressive Web App with:

1. **Service Worker Implementation**: Enable advanced caching and offline capabilities
2. **Workbox Integration**: Google-maintained caching strategies and best practices
3. **Offline Fallback**: Graceful degradation when network is unavailable
4. **Background Sync** (Optional): Queue queries while offline, sync when online
5. **Performance Validation**: Lighthouse PWA score 90+

### Scope

**In Scope:**
- Service worker creation and registration
- Workbox CDN integration
- Three caching strategies (Cache-First, Network-First, Stale-While-Revalidate)
- Offline fallback page
- Browser-based testing (Chrome, Firefox, Edge)
- Lighthouse PWA audit

**Out of Scope:**
- Native mobile app development
- Push notifications (future enhancement)
- Advanced service worker features (pre-caching, runtime caching variants)
- Safari-specific optimizations (limited service worker support)

### Expected Impact

**Performance:**
- **Instant UI loading**: Static assets cached (0ms vs 100-500ms)
- **50-90% faster**: Perceived performance with stale-while-revalidate
- **Offline functionality**: App loads and shows cached data when offline
- **30-50% reduction**: Bandwidth usage (cached responses)

**User Experience:**
- **No loading screens**: For repeat visits (cached assets)
- **Works offline**: View cached market data, offline fallback page
- **Installable**: Users can install PWA from browser
- **Professional feel**: App-like experience on mobile/desktop

**Technical:**
- **Lighthouse PWA score**: 90+ (from ~50-60 baseline)
- **Cache hit rate**: 60-80% for repeat visits
- **First Contentful Paint**: < 1.5s
- **Time to Interactive**: < 3s

---

## Prerequisites

### Required Knowledge

- Basic understanding of Service Workers and PWAs
- JavaScript event-driven programming
- Browser DevTools (Application tab, Network tab)
- HTTP caching concepts (Cache-Control, ETags)

### Required Tools

- Chrome/Edge browser (DevTools with Service Worker debugging)
- Node.js and npm (for Lighthouse CLI)
- Access to HF Spaces deployment (for testing deployed version)

### Verification Commands

```bash
# Install Lighthouse
npm install -g lighthouse

# Verify Lighthouse installation
lighthouse --version

# Check current PWA score (baseline)
lighthouse http://127.0.0.1:7860 --view --preset=desktop
```

---

## Task Breakdown

### Task 1: Create Service Worker Foundation (2-3 hours)

#### Overview

Create the core service worker file with install, activate, and fetch event handlers. This establishes the foundation for all PWA caching functionality.

#### Step-by-Step Implementation

**Step 1.1: Create service-worker.js** (30 minutes)

Create a new file `service-worker.js` in the project root (same level as `app.py`).

```javascript
// service-worker.js
const CACHE_VERSION = 'v1';
const CACHE_NAME = `market-parser-${CACHE_VERSION}`;
const OFFLINE_PAGE = '/offline.html';

// Assets to cache during install
const PRECACHE_ASSETS = [
  OFFLINE_PAGE,
  // Add core assets here (optional, will be cached dynamically)
];

// Install event: Cache precache assets
self.addEventListener('install', (event) => {
  console.log('[Service Worker] Install event');

  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log('[Service Worker] Precaching assets');
        return cache.addAll(PRECACHE_ASSETS);
      })
      .then(() => {
        // Activate immediately (don't wait for page reload)
        return self.skipWaiting();
      })
  );
});

// Activate event: Clean up old caches
self.addEventListener('activate', (event) => {
  console.log('[Service Worker] Activate event');

  event.waitUntil(
    caches.keys()
      .then((cacheNames) => {
        return Promise.all(
          cacheNames
            .filter((cacheName) => {
              // Delete old cache versions
              return cacheName.startsWith('market-parser-') && cacheName !== CACHE_NAME;
            })
            .map((cacheName) => {
              console.log('[Service Worker] Deleting old cache:', cacheName);
              return caches.delete(cacheName);
            })
        );
      })
      .then(() => {
        // Take control of all pages immediately
        return self.clients.claim();
      })
  );
});

// Fetch event: Basic network-first strategy (will be enhanced with Workbox)
self.addEventListener('fetch', (event) => {
  // For now, just pass through to network
  // Will be replaced with Workbox strategies in Task 2
  event.respondWith(
    fetch(event.request)
      .catch(() => {
        // If fetch fails and it's a navigation request, show offline page
        if (event.request.mode === 'navigate') {
          return caches.match(OFFLINE_PAGE);
        }
        // For other requests, try to return from cache
        return caches.match(event.request);
      })
  );
});

console.log('[Service Worker] Loaded');
```

**What this does:**
- **Install event**: Caches the offline page when service worker is first installed
- **Activate event**: Cleans up old cache versions when new service worker activates
- **Fetch event**: Basic fallback to offline page if network fails (will be enhanced in Task 2)

**Step 1.2: Register Service Worker in Gradio** (60 minutes)

Gradio apps require custom JavaScript injection. We'll use Gradio's `js` parameter or create a custom HTML head.

**Option A: Using Gradio's `js` parameter (Recommended)**

Modify `app.py`:

```python
# app.py
from src.backend.gradio_app import demo

# Service worker registration script
service_worker_js = """
function() {
    console.log('Market Parser PWA initializing...');

    // Register service worker
    if ('serviceWorker' in navigator) {
        window.addEventListener('load', () => {
            navigator.serviceWorker.register('/service-worker.js')
                .then((registration) => {
                    console.log('Service Worker registered:', registration.scope);

                    // Listen for updates
                    registration.addEventListener('updatefound', () => {
                        const newWorker = registration.installing;
                        console.log('New Service Worker found, installing...');

                        newWorker.addEventListener('statechange', () => {
                            if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
                                console.log('New Service Worker installed, refresh to activate');
                                // Optional: Show notification to user to refresh
                            }
                        });
                    });
                })
                .catch((error) => {
                    console.error('Service Worker registration failed:', error);
                });
        });
    } else {
        console.warn('Service Workers not supported in this browser');
    }
}
"""

if __name__ == "__main__":
    demo.queue(
        default_concurrency_limit=10,
        max_size=100,
    ).launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True,
        # Inject service worker registration
        js=service_worker_js,
    )
```

**What this does:**
- Checks if browser supports Service Workers
- Registers `/service-worker.js` when page loads
- Listens for service worker updates (for future deployments)
- Logs all events for debugging

**Option B: Using Gradio's `head` parameter (Alternative)**

If `js` parameter doesn't work, use `head`:

```python
# In gradio_app.py, add to demo.launch():
head_html = """
<script>
    if ('serviceWorker' in navigator) {
        window.addEventListener('load', () => {
            navigator.serviceWorker.register('/service-worker.js')
                .then((registration) => {
                    console.log('Service Worker registered:', registration.scope);
                })
                .catch((error) => {
                    console.error('Service Worker registration failed:', error);
                });
        });
    }
</script>
"""

demo.launch(
    ...
    head=head_html,
)
```

**Step 1.3: Configure HF Spaces to Serve service-worker.js** (30 minutes)

Hugging Face Spaces needs to serve the service worker file at the root URL.

**Option 1: Add static file serving to app.py**

```python
# app.py
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os

# Check if running on HF Spaces
is_hf_spaces = os.getenv("SPACE_ID") is not None

if is_hf_spaces:
    app = FastAPI()

    # Serve service worker at root
    @app.get("/service-worker.js")
    async def serve_service_worker():
        return FileResponse("service-worker.js", media_type="application/javascript")

    # Serve offline page
    @app.get("/offline.html")
    async def serve_offline_page():
        return FileResponse("offline.html", media_type="text/html")

    # Mount Gradio app
    app = gr.mount_gradio_app(app, demo, path="/")
else:
    # Local development
    demo.launch(...)
```

**Option 2: Use Gradio's static file serving (Gradio 5+)**

```python
# app.py
import gradio as gr

demo.launch(
    ...
    # Gradio 5+ can serve static files from project root
    # Ensure service-worker.js is in project root
)
```

**Note**: For HF Spaces, you may need to test both approaches. Gradio 5+ should automatically serve files from the project root.

**Step 1.4: Test Service Worker Registration** (30 minutes)

1. **Start local Gradio server:**

   ```bash
   uv run python app.py
   ```

2. **Open Chrome DevTools** (F12 or Cmd+Option+I)

3. **Navigate to Application tab → Service Workers**

4. **Verify:**
   - Service worker status: "activated and running"
   - Scope: "/" (root scope)
   - Source: "/service-worker.js"

5. **Check Console for logs:**
   ```
   Service Worker registered: http://127.0.0.1:7860/
   [Service Worker] Install event
   [Service Worker] Activate event
   [Service Worker] Loaded
   ```

6. **Test offline fallback:**
   - Go to Network tab → Check "Offline"
   - Refresh page
   - Should see offline.html (we'll create this in Task 3)

#### Success Criteria

- ✅ Service Worker registers successfully (DevTools → Application → Service Workers)
- ✅ Console shows install and activate events
- ✅ Service Worker scope is "/" (root)
- ✅ No registration errors in console
- ✅ Service Worker persists across page reloads

#### Rollback Plan

If service worker breaks the app:

1. **Unregister service worker** (Chrome DevTools):
   - Application → Service Workers → Click "Unregister"

2. **Clear caches** (Chrome DevTools):
   - Application → Cache Storage → Right-click → Delete

3. **Remove service worker registration code** from app.py

4. **Delete service-worker.js** file

5. **Restart Gradio server** and verify app works normally

#### Common Issues

**Issue 1: "Service Worker registration failed: SecurityError"**
- **Cause**: Service Workers require HTTPS (or localhost)
- **Fix**: Test on localhost or deployed HTTPS URL (HF Spaces has HTTPS)

**Issue 2: "Service Worker not found (404)"**
- **Cause**: service-worker.js not accessible at root URL
- **Fix**: Ensure file is in project root, check FastAPI static file serving

**Issue 3: "Service Worker stuck in 'waiting'"**
- **Cause**: Old service worker still active
- **Fix**: Add `self.skipWaiting()` in install event (already in code above)

---

### Task 2: Implement Workbox Caching Strategies (3-4 hours)

#### Overview

Replace the basic fetch handler with Workbox, implementing three caching strategies:
1. **Cache-First**: For static assets (CSS, JS, images)
2. **Network-First**: For API responses (real-time data)
3. **Stale-While-Revalidate**: For historical data (fast + fresh)

#### Step-by-Step Implementation

**Step 2.1: Import Workbox from CDN** (15 minutes)

Replace the content of `service-worker.js`:

```javascript
// service-worker.js
const CACHE_VERSION = 'v1';

// Import Workbox from CDN
importScripts('https://storage.googleapis.com/workbox-cdn/releases/7.0.0/workbox-sw.js');

// Check if Workbox loaded successfully
if (workbox) {
  console.log('[Workbox] Loaded successfully');

  // Configure Workbox
  workbox.setConfig({
    debug: false, // Set to true for development
  });

  // Enable Workbox logging in development
  workbox.core.setLogLevel(workbox.core.LOG_LEVELS.warn);
} else {
  console.error('[Workbox] Failed to load');
}

console.log('[Service Worker] Loaded with Workbox');
```

**What this does:**
- Imports Workbox library from Google's CDN (no npm install needed)
- Configures Workbox with production settings
- Provides fallback if Workbox fails to load

**Step 2.2: Implement Cache-First Strategy (Static Assets)** (45 minutes)

Add after Workbox configuration:

```javascript
// service-worker.js (continued)

// Strategy 1: Cache-First for static assets
// Use Case: CSS, JS, images, fonts (immutable or rarely changing)
workbox.routing.registerRoute(
  // Match CSS, JS, images, fonts
  ({request}) => {
    return (
      request.destination === 'style' ||
      request.destination === 'script' ||
      request.destination === 'image' ||
      request.destination === 'font'
    );
  },
  new workbox.strategies.CacheFirst({
    cacheName: 'static-assets-v1',
    plugins: [
      // Expiration: Limit cache size and age
      new workbox.expiration.ExpirationPlugin({
        maxEntries: 60, // Max 60 cached items
        maxAgeSeconds: 30 * 24 * 60 * 60, // 30 days
        purgeOnQuotaError: true, // Delete old entries if quota exceeded
      }),
      // Cache only successful responses (200)
      new workbox.cacheableResponse.CacheableResponsePlugin({
        statuses: [0, 200],
      }),
    ],
  })
);

console.log('[Workbox] Cache-First strategy registered for static assets');
```

**What this does:**
- **Cache-First**: Checks cache first, only fetches from network if not cached
- **Targets**: CSS, JS, images, fonts (Gradio UI assets)
- **Max 60 items**: Prevents unlimited cache growth
- **30-day TTL**: Assets expire after 30 days
- **Quota handling**: Automatically purges old entries if storage quota exceeded

**Benefits:**
- **Instant loading**: Cached assets load in 0ms (vs 100-500ms)
- **Offline support**: UI loads even when offline
- **Bandwidth savings**: No re-downloading of unchanged assets

**Step 2.3: Implement Network-First Strategy (API Responses)** (45 minutes)

Add after Cache-First strategy:

```javascript
// service-worker.js (continued)

// Strategy 2: Network-First for API responses
// Use Case: Real-time market data (prefer fresh, fallback to cache)
workbox.routing.registerRoute(
  // Match /api/* endpoints
  ({url}) => {
    return url.pathname.startsWith('/api/');
  },
  new workbox.strategies.NetworkFirst({
    cacheName: 'api-cache-v1',
    networkTimeoutSeconds: 10, // Fallback to cache after 10s
    plugins: [
      // Expiration: Short TTL for real-time data
      new workbox.expiration.ExpirationPlugin({
        maxEntries: 100, // Max 100 cached API responses
        maxAgeSeconds: 5 * 60, // 5 minutes TTL
        purgeOnQuotaError: true,
      }),
      // Cache only successful responses
      new workbox.cacheableResponse.CacheableResponsePlugin({
        statuses: [0, 200],
      }),
    ],
  })
);

console.log('[Workbox] Network-First strategy registered for API responses');
```

**What this does:**
- **Network-First**: Tries network first, falls back to cache if network fails
- **10s timeout**: If network takes > 10s, use cached response
- **Targets**: /api/* endpoints (Gradio API calls)
- **5-minute TTL**: Fresh data for 5 minutes, then re-fetch
- **Max 100 entries**: Limits cache size for API responses

**Benefits:**
- **Fresh data**: Always tries to fetch latest data first
- **Offline fallback**: Shows cached data if network unavailable
- **Timeout protection**: Prevents hanging on slow networks

**Step 2.4: Implement Stale-While-Revalidate (Mixed Content)** (45 minutes)

Add after Network-First strategy:

```javascript
// service-worker.js (continued)

// Strategy 3: Stale-While-Revalidate for mixed content
// Use Case: Historical data, company info (instant response + background update)
workbox.routing.registerRoute(
  // Match Gradio static files and historical data endpoints
  ({url}) => {
    return (
      url.pathname.includes('/file=') || // Gradio file serving
      url.pathname.includes('/gradio_api/') || // Gradio API
      url.pathname.includes('/historical/') || // Historical data (if you add this endpoint)
      url.pathname.includes('/company/')      // Company info (if you add this endpoint)
    );
  },
  new workbox.strategies.StaleWhileRevalidate({
    cacheName: 'dynamic-content-v1',
    plugins: [
      // Expiration: Medium TTL for mixed content
      new workbox.expiration.ExpirationPlugin({
        maxEntries: 50, // Max 50 cached items
        maxAgeSeconds: 60 * 60, // 1 hour TTL
        purgeOnQuotaError: true,
      }),
      // Cache successful responses
      new workbox.cacheableResponse.CacheableResponsePlugin({
        statuses: [0, 200],
      }),
    ],
  })
);

console.log('[Workbox] Stale-While-Revalidate strategy registered for mixed content');
```

**What this does:**
- **Stale-While-Revalidate**: Returns cached response immediately, fetches fresh data in background
- **Targets**: Gradio file serving, historical data
- **1-hour TTL**: Cached for 1 hour
- **Max 50 entries**: Moderate cache size

**Benefits:**
- **Instant response**: Cached data returns immediately (0ms)
- **Always fresh**: Background update ensures next visit has fresh data
- **Best of both worlds**: Fast + fresh

**Step 2.5: Add Offline Fallback Handler** (30 minutes)

Add at the end of service-worker.js:

```javascript
// service-worker.js (continued)

// Offline fallback for navigation requests
const OFFLINE_PAGE = '/offline.html';

// Precache offline page
workbox.precaching.precacheAndRoute([
  { url: OFFLINE_PAGE, revision: CACHE_VERSION },
]);

// Set up navigation route with offline fallback
workbox.routing.setDefaultHandler(
  new workbox.strategies.NetworkFirst({
    cacheName: 'default-cache-v1',
  })
);

// Catch navigation failures and show offline page
workbox.routing.setCatchHandler(({event}) => {
  if (event.request.destination === 'document') {
    return caches.match(OFFLINE_PAGE);
  }
  return Response.error();
});

console.log('[Workbox] Offline fallback configured');
```

**What this does:**
- **Precaches offline.html**: Ensures it's always available
- **Default handler**: Network-First for unmatched requests
- **Catch handler**: Shows offline page when navigation fails

**Step 2.6: Test Workbox Caching Strategies** (60 minutes)

1. **Restart Gradio server** (to load new service worker):

   ```bash
   uv run python app.py
   ```

2. **Force service worker update** (Chrome DevTools):
   - Application → Service Workers → Click "Update"
   - Refresh page (Cmd+R or Ctrl+R)

3. **Test Cache-First (Static Assets):**
   - Open Network tab
   - Refresh page
   - Filter by "CSS" and "JS"
   - Second refresh should show "(from ServiceWorker)" or "(disk cache)"

4. **Test Network-First (API Responses):**
   - Submit a query (e.g., "Tesla stock price")
   - Check Network tab for /api/ requests
   - Go offline (Network tab → Offline checkbox)
   - Submit same query again
   - Should return cached response

5. **Test Stale-While-Revalidate:**
   - Load Gradio UI assets
   - Check Network tab → Should see cached response
   - Verify background update (check DevTools console)

6. **Verify cache storage** (Chrome DevTools):
   - Application → Cache Storage
   - Should see 3 caches:
     - static-assets-v1
     - api-cache-v1
     - dynamic-content-v1

#### Success Criteria

- ✅ Workbox loads successfully (console: "Workbox loaded successfully")
- ✅ Three cache strategies registered (console logs)
- ✅ Static assets cached on first load
- ✅ API responses cached and returned when offline
- ✅ Cache Storage shows all three caches
- ✅ No console errors related to caching

#### Rollback Plan

If Workbox breaks caching:

1. **Revert to basic service worker**:
   - Restore service-worker.js from Task 1 (basic version)

2. **Clear all caches** (DevTools):
   - Application → Cache Storage → Delete all

3. **Unregister and re-register service worker**

4. **Test basic functionality** without Workbox

#### Common Issues

**Issue 1: "Workbox is not defined"**
- **Cause**: CDN import failed or blocked
- **Fix**: Check network connectivity, try alternative CDN URL

**Issue 2: "Cache quota exceeded"**
- **Cause**: Too many cached items
- **Fix**: Reduce maxEntries or maxAgeSeconds in expiration plugins

**Issue 3: "Service Worker not updating"**
- **Cause**: Browser caching old service worker
- **Fix**: Application → Service Workers → "Update on reload" checkbox

---

### Task 3: Create Offline Fallback Page (1-2 hours)

#### Overview

Design and implement a user-friendly offline.html page that displays when the network is unavailable. This provides a better user experience than the browser's default "No internet" page.

#### Step-by-Step Implementation

**Step 3.1: Create offline.html** (45 minutes)

Create a new file `offline.html` in the project root:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Offline - Market Parser</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #fff;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 20px;
        }

        .container {
            text-align: center;
            max-width: 600px;
        }

        .icon {
            font-size: 80px;
            margin-bottom: 20px;
            opacity: 0.9;
        }

        h1 {
            font-size: 2.5em;
            margin-bottom: 20px;
            font-weight: 700;
        }

        p {
            font-size: 1.2em;
            line-height: 1.6;
            margin-bottom: 30px;
            opacity: 0.95;
        }

        .status {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            padding: 20px;
            margin-top: 30px;
            backdrop-filter: blur(10px);
        }

        .status h2 {
            font-size: 1.3em;
            margin-bottom: 15px;
        }

        .status-indicator {
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: #ff4444;
            animation: pulse 2s infinite;
            margin-right: 10px;
        }

        @keyframes pulse {
            0%, 100% {
                opacity: 1;
            }
            50% {
                opacity: 0.5;
            }
        }

        .retry-button {
            display: inline-block;
            background: rgba(255, 255, 255, 0.2);
            color: #fff;
            padding: 15px 40px;
            border-radius: 30px;
            text-decoration: none;
            font-weight: 600;
            font-size: 1.1em;
            transition: all 0.3s ease;
            border: 2px solid rgba(255, 255, 255, 0.3);
            cursor: pointer;
            margin-top: 20px;
        }

        .retry-button:hover {
            background: rgba(255, 255, 255, 0.3);
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
        }

        .features {
            margin-top: 40px;
            text-align: left;
        }

        .features h3 {
            font-size: 1.2em;
            margin-bottom: 15px;
            text-align: center;
        }

        .features ul {
            list-style: none;
            padding: 0;
        }

        .features li {
            padding: 10px 0;
            padding-left: 30px;
            position: relative;
            opacity: 0.9;
        }

        .features li:before {
            content: "✓";
            position: absolute;
            left: 0;
            font-weight: bold;
            font-size: 1.3em;
        }

        @media (max-width: 768px) {
            h1 {
                font-size: 2em;
            }

            .icon {
                font-size: 60px;
            }

            p {
                font-size: 1em;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="icon">📡</div>
        <h1>You're Offline</h1>
        <p>
            It looks like you've lost your internet connection. Don't worry - Market Parser works offline too!
        </p>

        <div class="status">
            <h2>
                <span class="status-indicator"></span>
                Connection Status: Offline
            </h2>
            <p style="font-size: 1em; margin: 10px 0 0 0;">
                Please check your network connection and try again.
            </p>
        </div>

        <a href="/" class="retry-button" onclick="location.reload(); return false;">
            Retry Connection
        </a>

        <div class="features">
            <h3>What You Can Do Offline:</h3>
            <ul>
                <li>View cached market data from your recent queries</li>
                <li>Browse historical analysis you've already loaded</li>
                <li>Access the app interface and navigation</li>
            </ul>
        </div>
    </div>

    <script>
        // Auto-retry when connection restored
        window.addEventListener('online', () => {
            console.log('Connection restored, reloading...');
            location.reload();
        });

        // Update status indicator
        function updateConnectionStatus() {
            const indicator = document.querySelector('.status-indicator');
            const statusText = document.querySelector('.status h2');

            if (navigator.onLine) {
                indicator.style.background = '#44ff44';
                statusText.innerHTML = '<span class="status-indicator"></span>Connection Status: Back Online';
                setTimeout(() => location.reload(), 1000);
            } else {
                indicator.style.background = '#ff4444';
                statusText.innerHTML = '<span class="status-indicator"></span>Connection Status: Offline';
            }
        }

        // Check connection status every 5 seconds
        setInterval(updateConnectionStatus, 5000);
        updateConnectionStatus();
    </script>
</body>
</html>
```

**What this does:**
- **Visual design**: Professional gradient background, clear messaging
- **Status indicator**: Pulsing red dot shows offline status
- **Auto-retry**: Automatically reloads when connection restored
- **Feature list**: Tells users what they can still do offline
- **Responsive**: Works on mobile and desktop
- **Inline CSS**: No external dependencies (works 100% offline)

**Step 3.2: Test Offline Page** (30 minutes)

1. **Ensure offline.html is cached** (from Task 1):
   - Check service-worker.js precaches offline.html
   - Verify in DevTools → Application → Cache Storage

2. **Test offline navigation**:
   - Start Gradio server: `uv run python app.py`
   - Load the app in browser
   - Open DevTools → Network tab
   - Check "Offline" checkbox
   - Navigate to a new page or refresh
   - Should see offline.html

3. **Test auto-recovery**:
   - While offline page is showing
   - Uncheck "Offline" in Network tab
   - Should see "Connection Status: Back Online"
   - Page should auto-reload after 1 second

4. **Test on mobile** (optional):
   - Use Chrome Remote Debugging
   - Or test on deployed HF Spaces URL
   - Turn off WiFi on mobile device
   - Should see offline page

#### Success Criteria

- ✅ offline.html loads when network is unavailable
- ✅ Styled page displays (not plain HTML)
- ✅ Status indicator shows "Offline"
- ✅ "Retry Connection" button works
- ✅ Auto-reload when connection restored
- ✅ Responsive design works on mobile

#### Rollback Plan

If offline page breaks:

1. **Simplify offline.html**:
   - Remove JavaScript auto-retry
   - Use basic HTML and CSS only

2. **Verify it's cached**:
   - Check DevTools → Cache Storage
   - Ensure offline.html is in precache

3. **Test with simple content**:
   ```html
   <!DOCTYPE html>
   <html>
   <body>
     <h1>You're Offline</h1>
     <a href="/">Retry</a>
   </body>
   </html>
   ```

#### Common Issues

**Issue 1: "offline.html not found (404)"**
- **Cause**: File not served by Gradio/FastAPI
- **Fix**: Add static file serving in app.py (see Task 1 Step 1.3)

**Issue 2: "Offline page not cached"**
- **Cause**: Service worker didn't precache offline.html
- **Fix**: Check service-worker.js install event includes offline.html

**Issue 3: "Auto-reload not working"**
- **Cause**: 'online' event not firing
- **Fix**: Test manually, remove auto-reload if needed

---

### Task 4: Implement Background Sync (OPTIONAL - 2-3 hours)

#### Overview

**⚠️ OPTIONAL TASK** - Only implement if you want users to submit queries while offline and have them sync when connection is restored.

**Use Case:** User types a query while offline → query is queued → automatically sent when online.

**Complexity:** High (IndexedDB, sync events, error handling)

**Recommendation:** Skip this task unless user explicitly requests offline query submission feature. The offline fallback page from Task 3 is sufficient for most use cases.

#### When to Implement

Only implement Background Sync if:
- Users frequently lose connectivity during use
- Users want to queue multiple queries offline
- You're willing to add IndexedDB complexity
- You have 2-3 hours for implementation and testing

#### Step-by-Step Implementation

**Step 4.1: Create IndexedDB Query Queue** (60 minutes)

Add to service-worker.js:

```javascript
// service-worker.js (at the top, after Workbox import)

// IndexedDB setup for query queue
const DB_NAME = 'market-parser-db';
const DB_VERSION = 1;
const QUEUE_STORE = 'query-queue';

// Open IndexedDB
function openDB() {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open(DB_NAME, DB_VERSION);

    request.onerror = () => reject(request.error);
    request.onsuccess = () => resolve(request.result);

    request.onupgradeneeded = (event) => {
      const db = event.target.result;

      // Create object store for query queue
      if (!db.objectStoreNames.contains(QUEUE_STORE)) {
        const store = db.createObjectStore(QUEUE_STORE, {
          keyPath: 'id',
          autoIncrement: true,
        });
        store.createIndex('timestamp', 'timestamp', { unique: false });
        store.createIndex('status', 'status', { unique: false });
      }
    };
  });
}

// Add query to queue
async function queueQuery(query) {
  const db = await openDB();
  const tx = db.transaction(QUEUE_STORE, 'readwrite');
  const store = tx.objectStore(QUEUE_STORE);

  return store.add({
    query: query,
    timestamp: Date.now(),
    status: 'pending',
  });
}

// Get all pending queries
async function getPendingQueries() {
  const db = await openDB();
  const tx = db.transaction(QUEUE_STORE, 'readonly');
  const store = tx.objectStore(QUEUE_STORE);
  const index = store.index('status');

  return new Promise((resolve, reject) => {
    const request = index.getAll('pending');
    request.onsuccess = () => resolve(request.result);
    request.onerror = () => reject(request.error);
  });
}

// Mark query as synced
async function markQuerySynced(id) {
  const db = await openDB();
  const tx = db.transaction(QUEUE_STORE, 'readwrite');
  const store = tx.objectStore(QUEUE_STORE);

  const query = await store.get(id);
  if (query) {
    query.status = 'synced';
    return store.put(query);
  }
}

console.log('[IndexedDB] Query queue initialized');
```

**What this does:**
- Creates IndexedDB database for storing queries
- Provides functions to add, retrieve, and update queries
- Indexes by status (pending/synced) and timestamp

**Step 4.2: Implement Sync Event Handler** (60 minutes)

Add sync event listener:

```javascript
// service-worker.js (continued)

// Background sync event
self.addEventListener('sync', (event) => {
  console.log('[Background Sync] Sync event:', event.tag);

  if (event.tag === 'sync-queries') {
    event.waitUntil(syncQueuedQueries());
  }
});

// Sync all queued queries
async function syncQueuedQueries() {
  console.log('[Background Sync] Syncing queued queries...');

  try {
    const queries = await getPendingQueries();
    console.log(`[Background Sync] Found ${queries.length} pending queries`);

    for (const queryObj of queries) {
      try {
        // Send query to API
        const response = await fetch('/api/query', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            query: queryObj.query,
            timestamp: queryObj.timestamp,
          }),
        });

        if (response.ok) {
          // Mark as synced
          await markQuerySynced(queryObj.id);
          console.log(`[Background Sync] Synced query ${queryObj.id}`);

          // Notify user (optional)
          self.registration.showNotification('Query Synced', {
            body: `Your query "${queryObj.query}" has been processed`,
            icon: '/favicon.ico',
          });
        } else {
          console.error(`[Background Sync] Failed to sync query ${queryObj.id}:`, response.status);
        }
      } catch (error) {
        console.error(`[Background Sync] Error syncing query ${queryObj.id}:`, error);
        // Query will remain pending and retry on next sync
      }
    }

    console.log('[Background Sync] Sync complete');
  } catch (error) {
    console.error('[Background Sync] Sync failed:', error);
    throw error; // Retry sync
  }
}
```

**What this does:**
- Listens for 'sync-queries' event
- Retrieves all pending queries from IndexedDB
- Sends each query to the API
- Marks successful queries as synced
- Shows notification on successful sync (optional)
- Retries failed queries on next sync event

**Step 4.3: Register Sync from Client** (45 minutes)

Add sync registration to app.py or create a client-side script:

```javascript
// Add to service worker registration in app.py js parameter:

service_worker_js = """
function() {
    // ... existing service worker registration ...

    // Background sync registration helper
    window.registerBackgroundSync = async function(query) {
        if ('serviceWorker' in navigator && 'SyncManager' in window) {
            try {
                const registration = await navigator.serviceWorker.ready;

                // Queue the query (call service worker method)
                // This requires message passing to service worker
                const swController = navigator.serviceWorker.controller;
                if (swController) {
                    swController.postMessage({
                        type: 'QUEUE_QUERY',
                        query: query,
                    });
                }

                // Register sync
                await registration.sync.register('sync-queries');
                console.log('Background sync registered');
                return true;
            } catch (error) {
                console.error('Background sync registration failed:', error);
                return false;
            }
        } else {
            console.warn('Background sync not supported');
            return false;
        }
    };
}
"""
```

**Step 4.4: Handle Messages in Service Worker** (30 minutes)

Add message handler to service-worker.js:

```javascript
// service-worker.js (continued)

// Handle messages from client
self.addEventListener('message', async (event) => {
  console.log('[Service Worker] Message received:', event.data);

  if (event.data.type === 'QUEUE_QUERY') {
    try {
      await queueQuery(event.data.query);
      console.log('[Service Worker] Query queued:', event.data.query);

      // Respond to client
      event.ports[0].postMessage({
        success: true,
        message: 'Query queued successfully',
      });
    } catch (error) {
      console.error('[Service Worker] Failed to queue query:', error);
      event.ports[0].postMessage({
        success: false,
        error: error.message,
      });
    }
  }
});
```

**Step 4.5: Test Background Sync** (60 minutes)

1. **Test query queuing**:
   - Open DevTools → Console
   - Go offline (Network tab → Offline)
   - Submit a query
   - Check IndexedDB: Application → IndexedDB → market-parser-db → query-queue
   - Should see pending query

2. **Test sync execution**:
   - Go back online
   - Service worker should automatically trigger sync
   - Check console for "[Background Sync] Syncing queued queries..."
   - Query status should change to 'synced' in IndexedDB

3. **Test notifications** (if enabled):
   - Grant notification permission
   - Queue and sync a query
   - Should see notification: "Query Synced"

4. **Test failure handling**:
   - Queue a query with invalid data
   - Sync should fail gracefully
   - Query should remain pending for retry

#### Success Criteria (Optional Task)

- ✅ Queries queued in IndexedDB when offline
- ✅ Sync event triggers when connection restored
- ✅ Queued queries sent to API successfully
- ✅ Successful queries marked as synced
- ✅ Failed queries remain pending for retry
- ✅ Notifications shown (if enabled)

#### Rollback Plan

If background sync is too complex:

1. **Remove sync event listener** from service-worker.js
2. **Remove IndexedDB code**
3. **Remove sync registration** from app.py
4. **Rely on offline fallback page** (Task 3) instead
5. **Simpler approach**: Show "Cannot submit queries while offline" message

#### Common Issues

**Issue 1: "SyncManager is not defined"**
- **Cause**: Background sync not supported in all browsers
- **Fix**: Add feature detection, graceful degradation

**Issue 2: "Sync event not firing"**
- **Cause**: Browser throttles sync events
- **Fix**: Wait longer, test with Chrome DevTools sync controls

**Issue 3: "IndexedDB quota exceeded"**
- **Cause**: Too many queued queries
- **Fix**: Add cleanup for old synced queries

#### When to Skip This Task

Skip Background Sync if:
- ✅ You want faster implementation (save 2-3 hours)
- ✅ Users rarely lose connectivity
- ✅ Offline fallback page (Task 3) is sufficient
- ✅ You want to reduce complexity
- ✅ Browser compatibility is a concern (Safari has limited support)

**Recommended:** Skip this task initially, implement later if users request it.

---

### Task 5: Testing & Optimization (2-4 hours)

#### Overview

Comprehensive testing of all PWA features, Lighthouse audit, cross-browser testing, and performance optimization.

#### Step-by-Step Implementation

**Step 5.1: Run Lighthouse PWA Audit** (30 minutes)

1. **Deploy to HF Spaces** (if not already deployed):

   ```bash
   # Ensure all files are committed
   git add service-worker.js offline.html app.py
   git commit -m "[PWA] Add service worker and offline support"
   git push
   ```

2. **Run Lighthouse audit**:

   ```bash
   # For deployed HF Spaces URL
   lighthouse https://your-username-market-parser.hf.space --view --preset=desktop

   # For local testing
   lighthouse http://127.0.0.1:7860 --view --preset=desktop
   ```

3. **Review PWA checklist**:
   - ✅ Installable (manifest.json, service worker)
   - ✅ PWA optimized (offline support, fast load)
   - ✅ Accessible (ARIA labels, semantic HTML)
   - ✅ Best practices (HTTPS, no console errors)

4. **Target scores**:
   - **PWA**: 90+ (must pass)
   - **Performance**: 90+
   - **Accessibility**: 95+
   - **Best Practices**: 95+
   - **SEO**: 90+

**Step 5.2: Test Caching Strategies** (60 minutes)

1. **Test Cache-First (Static Assets)**:

   ```bash
   # Open Chrome DevTools → Network tab
   # Filter by CSS/JS
   # Load page twice
   # Second load should show "(from ServiceWorker)" or "(disk cache)"
   ```

   **Expected:**
   - First load: Network fetch (200-500ms)
   - Second load: Cache hit (0-10ms)

2. **Test Network-First (API Responses)**:

   ```bash
   # Submit query: "Tesla stock price"
   # Check Network tab → /api/ requests
   # Submit same query again
   # Should fetch from network (fresh data)

   # Go offline
   # Submit same query
   # Should return from cache
   ```

   **Expected:**
   - Online: Always fresh from network
   - Offline: Fallback to cached response

3. **Test Stale-While-Revalidate**:

   ```bash
   # Load Gradio UI assets
   # Network tab should show:
   #   1. Cached response returned immediately
   #   2. Background network request
   #   3. Cache updated
   ```

   **Expected:**
   - Instant cached response
   - Background update visible in Network tab

**Step 5.3: Calculate Cache Hit Rate** (30 minutes)

Add cache monitoring to service-worker.js:

```javascript
// service-worker.js (add at top)

let cacheHits = 0;
let cacheMisses = 0;

// Modify existing fetch handler or add new one
self.addEventListener('fetch', (event) => {
  const originalFetch = event.respondWith;

  event.respondWith(
    caches.match(event.request).then((cachedResponse) => {
      if (cachedResponse) {
        cacheHits++;
        console.log(`Cache hit rate: ${(cacheHits / (cacheHits + cacheMisses) * 100).toFixed(2)}%`);
        return cachedResponse;
      } else {
        cacheMisses++;
        return fetch(event.request);
      }
    })
  );
});
```

**Monitor cache hit rate:**
- Open DevTools → Console
- Use app normally for 5-10 minutes
- Check console for cache hit rate logs
- **Target**: 60-80% cache hit rate for repeat visits

**Step 5.4: Test Across Browsers** (60 minutes)

1. **Chrome** (full support):
   - Service worker: ✅
   - Cache API: ✅
   - Background sync: ✅
   - Install prompt: ✅

2. **Firefox** (full support):
   - Service worker: ✅
   - Cache API: ✅
   - Background sync: ✅ (desktop only)
   - Install prompt: ✅

3. **Edge** (Chromium-based, full support):
   - Service worker: ✅
   - Cache API: ✅
   - Background sync: ✅
   - Install prompt: ✅

4. **Safari** (partial support):
   - Service worker: ✅ (iOS 11.3+, macOS 11.1+)
   - Cache API: ✅
   - Background sync: ❌ (not supported)
   - Install prompt: Limited

**Testing checklist per browser:**
- [ ] Service worker registers successfully
- [ ] Static assets cached
- [ ] API responses cached
- [ ] Offline fallback works
- [ ] Cache hit rate > 60%
- [ ] No console errors

**Step 5.5: Monitor Cache Storage Size** (30 minutes)

Check cache storage quotas:

```javascript
// Add to service-worker.js or run in DevTools console
navigator.storage.estimate().then((estimate) => {
  const percentUsed = (estimate.usage / estimate.quota * 100).toFixed(2);
  console.log(`Storage used: ${estimate.usage} bytes`);
  console.log(`Storage quota: ${estimate.quota} bytes`);
  console.log(`Percent used: ${percentUsed}%`);
});
```

**Monitor in DevTools:**
- Application → Storage → Usage
- Should show cache size breakdown
- **Warning**: If usage > 80%, implement cache pruning

**Step 5.6: Optimize Cache Pruning** (60 minutes)

If cache grows too large, implement aggressive pruning:

```javascript
// service-worker.js (modify Workbox expiration plugins)

// Reduce maxEntries for each cache
new workbox.expiration.ExpirationPlugin({
  maxEntries: 30, // Was 60, now 30
  maxAgeSeconds: 7 * 24 * 60 * 60, // 7 days (was 30)
  purgeOnQuotaError: true,
})
```

**Add manual cache cleanup**:

```javascript
// service-worker.js (add helper function)

async function pruneOldCaches() {
  const cacheNames = await caches.keys();
  const now = Date.now();
  const maxAge = 7 * 24 * 60 * 60 * 1000; // 7 days

  for (const cacheName of cacheNames) {
    const cache = await caches.open(cacheName);
    const requests = await cache.keys();

    for (const request of requests) {
      const response = await cache.match(request);
      const dateHeader = response.headers.get('date');

      if (dateHeader) {
        const age = now - new Date(dateHeader).getTime();
        if (age > maxAge) {
          await cache.delete(request);
          console.log('[Cache Pruning] Deleted old entry:', request.url);
        }
      }
    }
  }
}

// Run pruning daily
setInterval(pruneOldCaches, 24 * 60 * 60 * 1000);
```

**Step 5.7: Test Install Prompt (PWA Installability)** (30 minutes)

1. **Test on Chrome desktop**:
   - Load app
   - Look for install icon in address bar (⊕)
   - Click icon → "Install Market Parser"
   - App should install as standalone app

2. **Test on Chrome mobile**:
   - Load app on mobile browser
   - Should see "Add to Home Screen" prompt
   - Add to home screen
   - Open from home screen → Should open as standalone app

3. **Verify manifest.json** (if not already present):

   ```json
   {
     "name": "Market Parser",
     "short_name": "MarketParser",
     "description": "Natural language financial queries",
     "start_url": "/",
     "display": "standalone",
     "background_color": "#ffffff",
     "theme_color": "#667eea",
     "icons": [
       {
         "src": "/icon-192.png",
         "sizes": "192x192",
         "type": "image/png"
       },
       {
         "src": "/icon-512.png",
         "sizes": "512x512",
         "type": "image/png"
       }
     ]
   }
   ```

   **Note**: Gradio may auto-generate manifest.json. Check if already exists.

**Step 5.8: Final Performance Validation** (30 minutes)

Run comprehensive performance test:

```bash
# Lighthouse audit (deployed URL)
lighthouse https://your-username-market-parser.hf.space \
  --view \
  --preset=desktop \
  --output=html \
  --output-path=./lighthouse-report.html
```

**Review performance metrics:**

| Metric | Target | Actual |
|--------|--------|--------|
| First Contentful Paint | < 1.5s | ___ |
| Time to Interactive | < 3s | ___ |
| Speed Index | < 3s | ___ |
| Total Blocking Time | < 200ms | ___ |
| Cumulative Layout Shift | < 0.1 | ___ |
| PWA Score | 90+ | ___ |

**If metrics don't meet targets:**
- Review Lighthouse suggestions
- Optimize cache strategies
- Reduce bundle size (if possible)
- Check HF Spaces resource limits

#### Success Criteria

- ✅ Lighthouse PWA score: 90+
- ✅ Lighthouse Performance score: 90+
- ✅ Cache hit rate: 60-80%
- ✅ All browsers tested (Chrome, Firefox, Edge)
- ✅ Offline functionality verified
- ✅ Install prompt working
- ✅ No console errors
- ✅ Cache storage < 80% quota

#### Rollback Plan

If testing reveals critical issues:

1. **Disable service worker**:
   - Remove service worker registration from app.py
   - Clear caches in DevTools

2. **Revert to working version**:
   - Git revert to commit before PWA changes

3. **Deploy without PWA features**:
   - Keep manifest.json (low risk)
   - Remove service-worker.js
   - Deploy basic version

4. **Fix issues incrementally**:
   - Fix one strategy at a time
   - Test thoroughly before proceeding

#### Common Issues

**Issue 1: "Lighthouse PWA score < 90"**
- **Causes**: Missing manifest.json, HTTPS required, offline not working
- **Fix**: Check Lighthouse report for specific failures, address each

**Issue 2: "Cache hit rate < 60%"**
- **Causes**: Incorrect caching strategies, cache not persisting
- **Fix**: Review Workbox configuration, check cache expiration settings

**Issue 3: "Safari service worker not working"**
- **Causes**: Safari has limited service worker support
- **Fix**: Test on Safari 11.3+, accept graceful degradation on older versions

---

## Final Testing and Validation

### Pre-Deployment Checklist

Before deploying to production:

- [ ] All 5 tasks completed (or Task 4 skipped if optional)
- [ ] Service worker registers successfully (DevTools verification)
- [ ] Three caching strategies working (Cache-First, Network-First, SWR)
- [ ] Offline fallback page loads correctly
- [ ] Lighthouse PWA score 90+
- [ ] Lighthouse Performance score 90+
- [ ] Cache hit rate 60-80%
- [ ] Tested on Chrome, Firefox, Edge (Safari optional)
- [ ] Install prompt working
- [ ] No console errors
- [ ] Cache storage within quota (< 80%)
- [ ] Background sync working (if implemented)

### Deployment Steps

1. **Commit all changes**:

   ```bash
   git add service-worker.js offline.html app.py
   git commit -m "[PWA] Phase 3 complete: Service worker, offline support, Workbox caching"
   git push
   ```

2. **Monitor HF Spaces build**:
   - Check build logs for errors
   - Verify service-worker.js deployed

3. **Test deployed version**:
   - Run Lighthouse on deployed URL
   - Test offline functionality
   - Verify install prompt

4. **Monitor for 24 hours**:
   - Check for console errors in production
   - Monitor cache hit rates
   - Collect user feedback

### Post-Deployment Validation

1. **Run Lighthouse audit** (deployed URL):

   ```bash
   lighthouse https://your-username-market-parser.hf.space --view
   ```

2. **Test on real devices**:
   - Mobile Chrome (Android)
   - Mobile Safari (iOS)
   - Desktop browsers

3. **Monitor metrics**:
   - Cache hit rate
   - Storage usage
   - Error rates
   - User feedback

---

## Success Metrics

### Quantitative Metrics

**Performance:**
- [ ] First Contentful Paint: < 1.5s (target: ~1s)
- [ ] Time to Interactive: < 3s (target: ~2s)
- [ ] Cache hit rate: > 60% (target: 70-80%)
- [ ] Lighthouse PWA score: 90+ (target: 95+)
- [ ] Lighthouse Performance: 90+ (target: 95+)

**Caching:**
- [ ] Static assets cached: 100% (after first visit)
- [ ] API responses cached: 60-80% (depends on usage)
- [ ] Cache storage: < 50 MB (target: ~20-30 MB)

**Offline:**
- [ ] Offline page loads: 100% success rate
- [ ] Cached content accessible offline: Yes
- [ ] Service worker active: > 99% uptime

**User Experience:**
- [ ] Install prompt shown: Yes
- [ ] PWA installed: Track installation rate
- [ ] Offline usage: Track offline access attempts

### Qualitative Metrics

**Developer Experience:**
- [ ] Code is maintainable and documented
- [ ] Service worker is debuggable (DevTools)
- [ ] Caching strategies are configurable
- [ ] Error handling is robust

**User Feedback:**
- [ ] Faster perceived performance (user reports)
- [ ] App works offline (user reports)
- [ ] Install experience is smooth (user feedback)
- [ ] No broken functionality (bug reports)

---

## Troubleshooting

### Service Worker Issues

**Problem: Service worker not registering**

```bash
# Check console for errors
# Common causes:
# 1. HTTPS required (except localhost)
# 2. service-worker.js not found (404)
# 3. Syntax errors in service-worker.js
```

**Solution:**
- Ensure HTTPS or localhost
- Verify service-worker.js in project root
- Check console for syntax errors
- Test with basic service worker first

**Problem: Service worker stuck in "waiting"**

```bash
# Cause: Old service worker still active
# Fix: Force update
```

**Solution:**
- DevTools → Application → Service Workers → "Update"
- Check "Update on reload" checkbox
- Add `self.skipWaiting()` in install event (already in code)

**Problem: Service worker not updating**

```bash
# Cause: Browser caching old service worker
```

**Solution:**
- Change CACHE_VERSION (e.g., 'v1' → 'v2')
- Hard refresh (Cmd+Shift+R or Ctrl+Shift+R)
- DevTools → "Bypass for network" checkbox

### Caching Issues

**Problem: Assets not caching**

```bash
# Check DevTools → Application → Cache Storage
# If empty, caching is not working
```

**Solution:**
- Verify Workbox loaded (console: "Workbox loaded successfully")
- Check route patterns match URLs
- Verify cache names in DevTools match service-worker.js

**Problem: Cache quota exceeded**

```bash
# Cause: Too many cached items
```

**Solution:**
- Reduce maxEntries in expiration plugins
- Reduce maxAgeSeconds (shorter TTL)
- Implement cache pruning (see Task 5.6)

**Problem: Stale data being served**

```bash
# Cause: Cache-First strategy for dynamic data
```

**Solution:**
- Use Network-First for API responses (already in code)
- Reduce maxAgeSeconds for API cache (currently 5 minutes)
- Force cache refresh: Change CACHE_VERSION

### Offline Issues

**Problem: Offline page not showing**

```bash
# Cause: offline.html not cached or not served
```

**Solution:**
- Verify offline.html in project root
- Check service-worker.js precaches offline.html
- Add static file serving in app.py (see Task 1.3)

**Problem: App not working offline**

```bash
# Cause: Service worker not catching fetch events
```

**Solution:**
- Check fetch event handler in service-worker.js
- Verify Workbox strategies registered
- Test with Network tab → Offline mode

### Lighthouse Issues

**Problem: Lighthouse PWA score < 90**

```bash
# Check specific failures in Lighthouse report
```

**Common failures:**
- "Does not register a service worker" → Fix service worker registration
- "Does not respond with 200 when offline" → Fix offline fallback
- "Does not provide a valid manifest.json" → Add/fix manifest
- "Is not configured for a custom splash screen" → Add icons to manifest

**Solution:**
- Address each failure individually
- Re-run Lighthouse after each fix

**Problem: Lighthouse Performance score < 90**

```bash
# Common causes:
# 1. Unoptimized images
# 2. Large bundle size
# 3. Slow server response time
```

**Solution:**
- Enable caching (should help significantly)
- Optimize HF Spaces resource allocation
- Review Lighthouse performance suggestions

---

## References

### Official Documentation

- **Workbox**: https://developer.chrome.com/docs/workbox/
- **Service Workers (MDN)**: https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API
- **PWA Caching Strategies**: https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Guides/Caching
- **Lighthouse**: https://developer.chrome.com/docs/lighthouse/
- **Background Sync**: https://developer.chrome.com/docs/workbox/modules/workbox-background-sync/

### Gradio-Specific

- **Gradio PWA**: https://www.gradio.app/guides/progressive-web-apps
- **Gradio Static Files**: https://www.gradio.app/guides/working-with-files

### Testing Tools

- **Lighthouse CLI**: https://github.com/GoogleChrome/lighthouse#using-the-node-cli
- **Chrome DevTools**: https://developer.chrome.com/docs/devtools/

---

## Notes

### Architecture Decisions

**Why Workbox?**
- Google-maintained, production-ready
- Simplified strategy implementation
- Built-in best practices (expiration, quota management)
- Active development and community support

**Why Three Caching Strategies?**
- **Cache-First**: Optimal for immutable static assets (instant loading)
- **Network-First**: Ensures fresh data for APIs (critical for financial data)
- **Stale-While-Revalidate**: Best of both worlds (fast + fresh)

**Why Optional Background Sync?**
- High complexity (IndexedDB, sync events)
- Limited browser support (Safari)
- Most users don't need offline query submission
- Offline fallback page is sufficient for most use cases

### Future Enhancements

Potential Phase 4 improvements:

1. **Advanced Caching**:
   - Predictive pre-caching (popular stocks)
   - Smart cache invalidation (market hours)

2. **Push Notifications**:
   - Price alerts
   - Market open/close notifications

3. **Advanced Service Worker Features**:
   - Runtime caching strategies
   - Network resilience patterns

4. **Performance Monitoring**:
   - Cache analytics dashboard
   - Real user monitoring (RUM)

---

## Conclusion

Phase 3 transforms Market Parser into a fully optimized Progressive Web App with:

- ✅ **Service Worker**: Advanced caching and offline capabilities
- ✅ **Workbox**: Production-ready caching strategies
- ✅ **Offline Support**: Graceful degradation with offline fallback page
- ✅ **Installability**: Users can install PWA from browser
- ✅ **Performance**: 50-90% faster perceived performance
- ✅ **Lighthouse**: 90+ PWA score

**Estimated Impact:**
- **Instant UI loading**: 0ms (vs 100-500ms)
- **Offline functionality**: Works without internet
- **Bandwidth reduction**: 30-50% less data usage
- **Professional UX**: App-like experience

**Next Steps:**
- Implement Phase 3 tasks sequentially
- Test thoroughly after each task
- Run Lighthouse audit
- Deploy to HF Spaces
- Monitor metrics and user feedback

---

**Phase 3 Plan Created**: 2025-10-19
**Status**: Ready for implementation
**Prerequisites**: Phase 1 and Phase 2 recommended (not required)
**Risk Level**: MEDIUM (test thoroughly, have rollback plan)
**Support**: Reference this document during implementation
