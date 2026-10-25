// ==============================================================================
// SIH26035: Mobile Service Worker (Offline Cache-First Strategy)
// Enables complete zero-network offline field verification for Legal Metrology
// ==============================================================================

const CACHE_NAME = "sih26035-metrology-v2.1";
const PRECACHE_ASSETS = [
  "/",
  "/api/session",
  "/scanner",
  "/mobile/index.html",
  "/mobile/scanner.html",
  "/mobile/manifest.json",
  "/manifest.json",
  "/mobile/vendor/tailwind.min.js",
  "/mobile/vendor/jsQR.min.js"
];

// Install Event: Precache offline core shell
self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log("[ServiceWorker] Precaching app shell for offline use");
      return cache.addAll(PRECACHE_ASSETS).catch((err) => {
        console.warn("[ServiceWorker] Precache soft-failure:", err);
      });
    })
  );
  self.skipWaiting();
});

// Activate Event: Clean up old version caches
self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.map((key) => {
          if (key !== CACHE_NAME) {
            console.log("[ServiceWorker] Removing legacy cache:", key);
            return caches.delete(key);
          }
        })
      );
    })
  );
  self.clients.claim();
});

// Fetch Event: Cache-First for static assets, Network-First with Cache fallback for API
self.addEventListener("fetch", (event) => {
  const url = new URL(event.request.url);

  // For write actions (POST/PUT/DELETE), bypass cache or queue
  if (event.request.method !== "GET") {
    return;
  }

  // Handle static assets & documents
  event.respondWith(
    caches.match(event.request).then((cachedResponse) => {
      if (cachedResponse) {
        // Return cached and refresh in background
        fetch(event.request)
          .then((networkResponse) => {
            if (networkResponse && networkResponse.status === 200) {
              caches.open(CACHE_NAME).then((cache) => cache.put(event.request, networkResponse));
            }
          })
          .catch(() => {});
        return cachedResponse;
      }

      return fetch(event.request)
        .then((networkResponse) => {
          if (!networkResponse || networkResponse.status !== 200 || networkResponse.type !== "basic") {
            return networkResponse;
          }
          const responseToCache = networkResponse.clone();
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(event.request, responseToCache);
          });
          return networkResponse;
        })
        .catch(() => {
          // Offline fallback
          if (event.request.headers.get("accept").includes("text/html")) {
            return caches.match("/");
          }
        });
    })
  );
});
