/**
 * PRAHARIX 3.0 - Progressive Web App (PWA) Setup
 * Item #45: Offline dashboard
 * Item #46: Automatic data synchronization
 */

(function() {
  // Register Service Worker
  if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
      navigator.serviceWorker.register('/sw.js', { scope: '/' })
        .then(function(reg) {
          console.log('[PRAHARIX PWA] Service Worker registered. Scope:', reg.scope);
          // Listen for SW messages
          navigator.serviceWorker.addEventListener('message', function(event) {
            if (event.data && event.data.type === 'SYNC_COMPLETE') {
              console.log('[PRAHARIX PWA] Background sync completed');
            }
          });
        })
        .catch(function(err) {
          console.warn('[PRAHARIX PWA] Service Worker registration failed:', err);
        });
    });
  }

  // Online/Offline status indicator
  function updateOnlineStatus() {
    var isOnline = navigator.onLine;
    var indicator = document.getElementById('online-status');
    if (indicator) {
      indicator.textContent = isOnline ? '🟢 LIVE' : '🟡 OFFLINE';
      indicator.className = isOnline ? 'badge bg-success' : 'badge bg-warning';
      indicator.title = isOnline ? 'Connected to live data feeds' : 'Using cached data - will sync when online';
    }
    // Show offline toast
    if (!isOnline) {
      var toast = document.getElementById('offline-toast');
      if (toast && window.bootstrap && window.bootstrap.Toast) {
        new window.bootstrap.Toast(toast).show();
      }
    }
  }

  window.addEventListener('online', function() {
    updateOnlineStatus();
    // Trigger background sync when back online
    if ('serviceWorker' in navigator && 'SyncManager' in window) {
      navigator.serviceWorker.ready.then(function(sw) {
        return sw.sync.register('sync-incidents');
      }).catch(function() {});
    }
  });
  window.addEventListener('offline', updateOnlineStatus);

  document.addEventListener('DOMContentLoaded', updateOnlineStatus);

  // Data freshness tracking (#43)
  window.praharixDataFreshness = {};
  window.updateDataFreshness = function(key, timestamp) {
    window.praharixDataFreshness[key] = timestamp || new Date();
    var el = document.querySelector('[data-freshness="' + key + '"]');
    if (el) {
      var diff = Math.round((new Date() - window.praharixDataFreshness[key]) / 60000);
      el.textContent = diff < 1 ? 'just now' : diff + ' min ago';
    }
  };

})();
