module.exports = {
  ci: {
    collect: {
      // Use the Vite build output directory
      staticDistDir: './dist',
      
      // Number of runs for consistent results
      numberOfRuns: 1,
      
      // Lighthouse settings optimized for chat application
      settings: {
        // Disable storage reset to maintain realistic user experience
        disableStorageReset: true,
        
        // Increase timeout for interactive chat features
        maxWaitForLoad: 60000,
        
        // Use simulated throttling for consistent results
        throttlingMethod: 'simulate',
        
        // Skip audits that are less relevant for chat applications
        skipAudits: [
          'redirects-http', // Not applicable for SPA
          'canonical', // Not needed for chat interface
        ],
        
        // Chrome flags for CI environment
        chromeFlags: '--no-sandbox --disable-setuid-sandbox --disable-dev-shm-usage',
      },
    },
    
    assert: {
      // Use lighthouse recommended preset as baseline
      preset: 'lighthouse:recommended',
      
      // Custom assertions for chat application performance
      assertions: {
        // Performance - realistic for interactive chat app
        'categories:performance': ['warn', { minScore: 0.85 }],
        
        // PWA - strict since Phase 2 implemented PWA features
        'categories:pwa': ['error', { minScore: 0.90 }],
        
        // Accessibility - high standards for inclusive design
        'categories:accessibility': ['error', { minScore: 0.95 }],
        
        // Best Practices - good code quality standards
        'categories:best-practices': ['warn', { minScore: 0.90 }],
        
        // SEO - relaxed for chat interface
        'categories:seo': ['warn', { minScore: 0.80 }],
        
        // Core Web Vitals - optimized for chat UX
        'first-contentful-paint': ['warn', { maxNumericValue: 2500 }],
        'largest-contentful-paint': ['warn', { maxNumericValue: 4000 }],
        'cumulative-layout-shift': ['warn', { maxNumericValue: 0.1 }],
        
        // Interactive metrics important for chat
        'interactive': ['warn', { maxNumericValue: 5000 }],
        'speed-index': ['warn', { maxNumericValue: 4000 }],
        
        // Resource efficiency for real-time features
        'total-blocking-time': ['warn', { maxNumericValue: 300 }],
        
        // Disable some audits less relevant for chat apps
        'offscreen-images': 'off', // Chat typically loads images on demand
        'uses-webp-images': 'off', // Flexible image format policy
        'render-blocking-resources': 'off', // Some blocking resources acceptable for chat UI
        'unused-css-rules': 'off', // Component-based CSS may appear unused
        
        // PWA specific assertions
        'installable-manifest': ['error'],
        'apple-touch-icon': ['warn'],
        'service-worker': ['error'],
        'works-offline': ['warn'], // Important for chat continuity
        
        // Security and best practices
        'is-on-https': ['error'],
        'uses-https': ['error'],
        'no-vulnerable-libraries': ['error'],
        
        // User experience for chat interface
        'tap-targets': ['warn'], // Important for mobile chat
        'color-contrast': ['warn'], // Accessibility in chat UI
        'meta-viewport': ['error'], // Critical for responsive chat
      },
    },
    
    upload: {
      // Use temporary public storage for prototype simplicity
      target: 'temporary-public-storage',
      
      // Upload URL mapping for historical comparison
      uploadUrlMap: true,
      
      // URL patterns for consistent reporting
      urlReplacementPatterns: [
        's#:[0-9]{3,5}/#:PORT/#',
        's/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}/UUID/ig',
      ],
    },
  },
};