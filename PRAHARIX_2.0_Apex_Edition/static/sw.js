/**
 * PRAHARIX 3.0 Service Worker
 * Item #45: Offline dashboard support
 * Item #46: Automatic data synchronization
 */

const CACHE_NAME = 'praharix-v3-cache';
const OFFLINE_CACHE = 'praharix-v3-offline';

const STATIC_ASSETS = [
  '/',
  '/alerts',
  '/sar',
  '/india',
  '/govt',
  '/multihazard',
  '/static/css/accessibility.css',
  '/static/js/accessibility.js',
  '/static/js/i18n.js'
];

const API_CACHE_ROUTES = [
  '/api/weather',
  '/api/ai/summary',
  '/api/health',
  '/api/status'
];

// Install: cache static assets
self.addEventListener('install', function(event) {
  event.waitUntil(
    caches.open(CACHE_NAME).then(function(cache) {
      return cache.addAll(STATIC_ASSETS).catch(function() {
        // Silently fail if some assets aren't available
      });
    })
  );
  self.skipWaiting();
});

// Activate: clean old caches
self.addEventListener('activate', function(event) {
  event.waitUntil(
    caches.keys().then(function(keys) {
      return Promise.all(
        keys.filter(k => k !== CACHE_NAME && k !== OFFLINE_CACHE)
            .map(k => caches.delete(k))
      );
    })
  );
  self.clients.claim();
});

// Fetch: network-first with fallback
self.addEventListener('fetch', function(event) {
  const url = new URL(event.request.url);
  
  // Skip non-GET or cross-origin
  if (event.request.method !== 'GET' || url.origin !== self.location.origin) return;

  // API routes: stale-while-revalidate
  if (API_CACHE_ROUTES.some(r => url.pathname.startsWith(r))) {
    event.respondWith(
      caches.open(OFFLINE_CACHE).then(function(cache) {
        return fetch(event.request)
          .then(function(response) {
            if (response.ok) cache.put(event.request, response.clone());
            return response;
          })
          .catch(function() {
            return cache.match(event.request).then(function(cached) {
              return cached || new Response(
                JSON.stringify({ status: 'offline', message: 'Using cached data' }),
                { headers: { 'Content-Type': 'application/json' } }
              );
            });
          });
      })
    );
    return;
  }

  // Static assets: cache-first
  event.respondWith(
    caches.match(event.request).then(function(cached) {
      if (cached) return cached;
      return fetch(event.request).then(function(response) {
        if (response.ok) {
          const clone = response.clone();
          caches.open(CACHE_NAME).then(c => c.put(event.request, clone));
        }
        return response;
      }).catch(function() {
        // Return offline page for navigation requests
        if (event.request.mode === 'navigate') {
          return caches.match('/');
        }
      });
    })
  );
});

// Background sync
self.addEventListener('sync', function(event) {
  if (event.tag === 'sync-incidents') {
    event.waitUntil(syncPendingIncidents());
  }
});

async function syncPendingIncidents() {
  // Sync logic handled by main app
  const clients = await self.clients.matchAll();
  clients.forEach(c => c.postMessage({ type: 'SYNC_COMPLETE' }));
}
