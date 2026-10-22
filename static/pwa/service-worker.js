const CACHE_NAME = "quicknest-v3";

const urlsToCache = [
    "/",
];

self.addEventListener("install", (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => cache.addAll(urlsToCache))
    );
    self.skipWaiting();
});

self.addEventListener("activate", (event) => {
    event.waitUntil(
        caches.keys().then((keys) => {
            return Promise.all(
                keys.filter((key) => key !== CACHE_NAME).map((key) => caches.delete(key))
            );
        }).then(() => self.clients.claim())
    );
});

self.addEventListener("fetch", (event) => {
    // CRITICAL: NEVER intercept non-GET requests (POST, PUT, DELETE, etc.).
    // Safari on iOS drops multipart/form-data bodies when intercepted by a Service Worker!
    if (event.request.method !== "GET") {
        return;
    }

    // For navigation (HTML pages), always fetch fresh from network to guarantee active CSRF tokens
    if (event.request.mode === "navigate") {
        event.respondWith(
            fetch(event.request)
                .catch(() => caches.match(event.request).then((res) => res || caches.match("/")))
        );
        return;
    }

    event.respondWith(
        caches.match(event.request).then((response) => {
            return response || fetch(event.request);
        })
    );
});