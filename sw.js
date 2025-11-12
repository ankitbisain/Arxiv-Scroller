const CACHE_NAME = 'slides-cache-v1';
const urlsToCache = [
  '/', 
  'index.html',
  // Add your icon files here
  'icon-192.png',
  'icon-512.png'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(urlsToCache))
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request).then(response => {
        return response || fetch(event.request);
      })
  );
});