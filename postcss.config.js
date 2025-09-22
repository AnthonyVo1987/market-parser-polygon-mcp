// PostCSS Configuration for CSS Optimization
// Integrates cssnano for automated CSS minification and optimization

module.exports = {
    plugins: [
        require('cssnano')({
            preset: ['default', {
                // Optimize for performance
                discardComments: {
                    removeAll: true,
                },
                // Minify selectors
                minifySelectors: true,
                // Reduce transforms
                reduceTransforms: true,
                // Normalize URLs
                normalizeUrl: true,
                // Minify font values
                minifyFontValues: true,
                // Convert values
                convertValues: {
                    length: true,
                    angle: true,
                    time: true,
                },
                // Minify params
                minifyParams: true,
                // Normalize charset
                normalizeCharset: {
                    add: false,
                },
                // Minify gradients
                minifyGradients: true,
                // Minify colors
                minifyColors: true,
                // Merge longhand
                mergeLonghand: true,
                // Merge rules
                mergeRules: true,
                // Normalize display values
                normalizeDisplayValues: true,
                // Normalize positions
                normalizePositions: true,
                // Normalize repeat styles
                normalizeRepeatStyle: true,
                // Normalize string
                normalizeString: true,
                // Normalize timing functions
                normalizeTimingFunctions: true,
                // Normalize unicode
                normalizeUnicode: true,
                // Normalize whitespace
                normalizeWhitespace: true,
                // Ordered values
                orderedValues: true,
                // Reduce idents
                reduceIdents: true,
                // Reduce initial
                reduceInitial: true,
                // Reduce calc
                reduceCalc: true,
                // Reduce declarations
                reduceDeclares: true,
                // Reduce transforms
                reduceTransforms: true,
                // Reduce values
                reduceValues: true,
                // Remove duplicates
                removeDuplicates: true,
                // Remove empty
                removeEmpty: true,
                // Remove unused
                removeUnused: true,
                // Replace
                replace: true,
                // Safe parser
                safe: true,
                // Z-index
                zindex: true,
            }],
        }),
    ],
};
