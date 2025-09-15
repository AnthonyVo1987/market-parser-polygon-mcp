// Service Worker Cleanup Script for Development
// This script unregisters existing service workers and clears workbox caches
// Only runs in development to prevent workbox console errors

// Check if we're in development (localhost or 127.0.0.1)
const isDevelopment = location.hostname === 'localhost' || location.hostname === '127.0.0.1';

if ('serviceWorker' in navigator && isDevelopment) {
  console.log('🧹 Development SW Cleanup: Starting service worker cleanup...');

  // Unregister all existing service workers
  navigator.serviceWorker.getRegistrations().then(function(registrations) {
    if (registrations.length === 0) {
      console.log('🧹 Development SW Cleanup: No existing service workers found');
      return;
    }

    console.log(`🧹 Development SW Cleanup: Found ${registrations.length} existing service worker(s), unregistering...`);

    for(let registration of registrations) {
      registration.unregister().then(function(boolean) {
        if (boolean) {
          console.log('🧹 Development SW Cleanup: Service worker unregistered successfully');
        } else {
          console.log('🧹 Development SW Cleanup: Service worker unregistration failed');
        }
      });
    }
  }).catch(function(error) {
    console.log('🧹 Development SW Cleanup: Error during service worker cleanup:', error);
  });

  // Clear workbox-related caches
  if ('caches' in window) {
    caches.keys().then(function(cacheNames) {
      const workboxCaches = cacheNames.filter(name =>
        name.includes('workbox') ||
        name.includes('precache') ||
        name.includes('runtime') ||
        name.includes('api-cache') ||
        name.includes('manifest-cache') ||
        name.includes('webmanifest-cache')
      );

      if (workboxCaches.length > 0) {
        console.log(`🧹 Development SW Cleanup: Found ${workboxCaches.length} workbox cache(s), clearing...`);

        return Promise.all(
          workboxCaches.map(cacheName => {
            return caches.delete(cacheName).then(function(deleted) {
              if (deleted) {
                console.log(`🧹 Development SW Cleanup: Cleared cache: ${cacheName}`);
              }
            });
          })
        );
      } else {
        console.log('🧹 Development SW Cleanup: No workbox caches found');
      }
    }).catch(function(error) {
      console.log('🧹 Development SW Cleanup: Error during cache cleanup:', error);
    });
  }

  console.log('🧹 Development SW Cleanup: Cleanup script completed');
}