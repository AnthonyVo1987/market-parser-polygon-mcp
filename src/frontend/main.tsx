import React from 'react';
import ReactDOM from 'react-dom/client';
import './wdyr';

import App from './App.tsx';
import './index.css';
import './pwa-types.d.ts';

// Basic CSS reset and global styles
const globalStyles = `
  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }
  
  body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
      'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
      sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
  }
  
  #root {
    height: 100vh;
    overflow: hidden;
  }
`;

// Inject global styles
const styleElement = document.createElement('style');
styleElement.textContent = globalStyles;
document.head.appendChild(styleElement);

const rootElement = document.getElementById('root');
if (!rootElement) throw new Error('Failed to find the root element');

ReactDOM.createRoot(rootElement).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

// PWA Service Worker Registration
async function registerServiceWorker() {
  if ('serviceWorker' in navigator) {
    try {
      const { registerSW } = await import('virtual:pwa-register');

      const updateSW = registerSW({
        onNeedRefresh() {
          // Auto-update strategy - no user prompt needed
        },
        onOfflineReady() {
        },
        onRegistered(_registration: ServiceWorkerRegistration) {
          // Service worker registered successfully
        },
        onRegisterError(_error: Error) {
          // Service worker registration failed
        },
      });

      // Auto-update every hour
      setInterval(
        () => {
          updateSW(true).catch((_error: Error) => {
            // Auto-update failed, will retry next hour
          });
        },
        60 * 60 * 1000
      );
    } catch (_error) {
      // Service worker registration failed, app will work without PWA features
    }
  }
}

// Register service worker after React app is initialized
registerServiceWorker().catch((_error: Error) => {
  // Service worker registration failed, app will work without PWA features
});
