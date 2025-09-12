module.exports = {
  // Basic formatting options
  semi: true,
  trailingComma: 'es5',
  singleQuote: true,
  printWidth: 80,
  tabWidth: 2,
  useTabs: false,

  // JSX and React specific
  jsxSingleQuote: true,
  bracketSpacing: true,
  bracketSameLine: false,
  arrowParens: 'avoid',

  // Line endings (consistent across platforms)
  endOfLine: 'lf',

  // Override for specific file types
  overrides: [
    {
      files: ['*.json', '*.jsonc'],
      options: {
        printWidth: 120,
        tabWidth: 2,
      },
    },
    {
      files: ['*.md', '*.mdx'],
      options: {
        printWidth: 100,
        proseWrap: 'always',
      },
    },
  ],
};