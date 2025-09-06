import React from 'react';
import ReactDOM from 'react-dom/client';

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
          // eslint-disable-next-line no-console
          console.log('PWA: New app version available. Update will be applied automatically.');
          // Auto-update strategy - no user prompt needed
        },
        onOfflineReady() {
          // eslint-disable-next-line no-console
          console.log('PWA: App is ready to work offline.');
        },
        onRegistered(registration: ServiceWorkerRegistration) {
          // eslint-disable-next-line no-console
          console.log('PWA: Service worker registered successfully:', registration);
        },
        onRegisterError(error: Error) {
          // eslint-disable-next-line no-console
          console.error('PWA: Service worker registration failed:', error);
        }
      });
      
      // Auto-update every hour
      setInterval(() => {
        updateSW(true).catch((error: Error) => {
          // eslint-disable-next-line no-console
          console.error('PWA: Auto-update failed:', error);
        });
      }, 60 * 60 * 1000);
      
    } catch (error) {
      // eslint-disable-next-line no-console
      console.error('PWA: Failed to register service worker:', error);
    }
  }
}

// Register service worker after React app is initialized
registerServiceWorker().catch((error: Error) => {
  // eslint-disable-next-line no-console
  console.error('PWA: Service worker registration initialization failed:', error);
});
