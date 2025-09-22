module.exports = {
    ci: {
        collect: {
            numberOfRuns: 3,
            settings: {
                preset: 'desktop',
                budgetPath: './budgets.json'
            }
        },
        assert: {
            assertions: {
                'first-contentful-paint': ['error', { maxNumericValue: 2000 }],
                'interactive': ['error', { maxNumericValue: 5000 }],
                'speed-index': ['error', { maxNumericValue: 3000 }],
                'total-blocking-time': ['error', { maxNumericValue: 300 }],
                'largest-contentful-paint': ['error', { maxNumericValue: 2500 }],
                'cumulative-layout-shift': ['error', { maxNumericValue: 0.1 }]
            }
        },
        upload: {
            target: 'temporary-public-storage'
        }
    }
};
