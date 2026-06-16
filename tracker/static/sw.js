const CACHE_NAME = 'budzet-v1';
const urlsToCache = [
    '/',
    '/wydatki/',
    '/przychody/',
    '/statystyki/',
];

self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => cache.addAll(urlsToCache))
    );
});

self.addEventListener('fetch', event => {
    event.respondWith(
        caches.match(event.request)
            .then(response => response || fetch(event.request))
    );
});