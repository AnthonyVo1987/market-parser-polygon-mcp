// Placeholder text utility system for consistent user experience

export interface PlaceholderTextOptions {
  context?: 'chat' | 'ticker' | 'email' | 'url' | 'general';
  userState?: 'idle' | 'typing' | 'loading' | 'error';
  isRequired?: boolean;
  maxLength?: number;
  examples?: string[];
}

export const PLACEHOLDER_TEXTS = {
  // Chat input placeholders
  CHAT_IDLE: 'Type your financial questions here...',
  CHAT_TYPING: 'Continue typing your question...',
  CHAT_LOADING: 'AI is processing your request...',
  CHAT_ERROR: 'Please try again with a different question...',

  // Ticker input placeholders
  TICKER_IDLE: 'Enter stock ticker (e.g., AAPL, MSFT, GOOGL)',
  TICKER_TYPING: 'Enter 1-5 letters for stock symbol...',
  TICKER_LOADING: 'Searching for stock information...',
  TICKER_ERROR: 'Please enter a valid stock ticker...',

  // Email input placeholders
  EMAIL_IDLE: 'Enter your email address',
  EMAIL_TYPING: 'Enter a valid email address...',
  EMAIL_LOADING: 'Validating email address...',
  EMAIL_ERROR: 'Please enter a valid email address...',

  // URL input placeholders
  URL_IDLE: 'Enter a valid URL (e.g., https://example.com)',
  URL_TYPING: 'Enter a complete URL...',
  URL_LOADING: 'Validating URL...',
  URL_ERROR: 'Please enter a valid URL...',

  // General input placeholders
  GENERAL_IDLE: 'Enter your input here...',
  GENERAL_TYPING: 'Continue typing...',
  GENERAL_LOADING: 'Processing your input...',
  GENERAL_ERROR: 'Please check your input and try again...',
} as const;

export function getPlaceholderText(
  options: PlaceholderTextOptions = {}
): string {
  const {
    context = 'general',
    userState = 'idle',
    isRequired = false,
    maxLength,
    examples = [],
  } = options;

  // Build base placeholder text
  let baseText = '';

  switch (context) {
    case 'chat':
      baseText =
        PLACEHOLDER_TEXTS[
          `CHAT_${userState.toUpperCase()}` as keyof typeof PLACEHOLDER_TEXTS
        ];
      break;
    case 'ticker':
      baseText =
        PLACEHOLDER_TEXTS[
          `TICKER_${userState.toUpperCase()}` as keyof typeof PLACEHOLDER_TEXTS
        ];
      break;
    case 'email':
      baseText =
        PLACEHOLDER_TEXTS[
          `EMAIL_${userState.toUpperCase()}` as keyof typeof PLACEHOLDER_TEXTS
        ];
      break;
    case 'url':
      baseText =
        PLACEHOLDER_TEXTS[
          `URL_${userState.toUpperCase()}` as keyof typeof PLACEHOLDER_TEXTS
        ];
      break;
    default:
      baseText =
        PLACEHOLDER_TEXTS[
          `GENERAL_${userState.toUpperCase()}` as keyof typeof PLACEHOLDER_TEXTS
        ];
  }

  // Add examples if provided
  if (examples.length > 0) {
    const exampleText = examples.join(', ');
    baseText = `${baseText} (e.g., ${exampleText})`;
  }

  // Add length information if maxLength is provided
  if (maxLength) {
    baseText = `${baseText} (max ${maxLength} characters)`;
  }

  // Add required indicator
  if (isRequired) {
    baseText = `${baseText} *`;
  }

  return baseText;
}

// Context-specific placeholder text generators
export function getChatPlaceholder(
  userState: PlaceholderTextOptions['userState'] = 'idle'
): string {
  return getPlaceholderText({ context: 'chat', userState });
}

export function getTickerPlaceholder(
  userState: PlaceholderTextOptions['userState'] = 'idle'
): string {
  return getPlaceholderText({
    context: 'ticker',
    userState,
    examples: ['AAPL', 'MSFT', 'GOOGL', 'TSLA', 'NVDA'],
  });
}

export function getEmailPlaceholder(
  userState: PlaceholderTextOptions['userState'] = 'idle'
): string {
  return getPlaceholderText({ context: 'email', userState });
}

export function getUrlPlaceholder(
  userState: PlaceholderTextOptions['userState'] = 'idle'
): string {
  return getPlaceholderText({
    context: 'url',
    userState,
    examples: ['https://example.com'],
  });
}

// Placeholder text validation
export function validatePlaceholderText(text: string): {
  isValid: boolean;
  issues: string[];
} {
  const issues: string[] = [];

  // Check minimum length
  if (text.length < 10) {
    issues.push('Placeholder text should be at least 10 characters long');
  }

  // Check maximum length
  if (text.length > 100) {
    issues.push('Placeholder text should not exceed 100 characters');
  }

  // Check for helpful tone
  if (
    !text.includes('...') &&
    !text.includes('Enter') &&
    !text.includes('Type')
  ) {
    issues.push('Placeholder text should use helpful action words');
  }

  // Check for examples
  if (!text.includes('e.g.,') && !text.includes('example')) {
    issues.push('Consider adding examples for better user guidance');
  }

  return {
    isValid: issues.length === 0,
    issues,
  };
}

// Accessibility helpers for placeholder text
export function getPlaceholderAriaLabel(
  placeholder: string,
  fieldName: string
): string {
  return `${fieldName} - ${placeholder}`;
}

export function getPlaceholderAriaDescribedBy(fieldId: string): string {
  return `${fieldId}-placeholder-help`;
}
