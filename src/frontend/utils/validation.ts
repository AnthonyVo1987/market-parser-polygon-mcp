// Validation utility functions for input fields
export interface ValidationResult {
    isValid: boolean;
    errorCode?: string;
    errorMessage?: string;
}

export interface ValidationRule {
    required?: boolean;
    minLength?: number;
    maxLength?: number;
    pattern?: RegExp;
    custom?: (value: string) => ValidationResult;
}

export const VALIDATION_ERROR_CODES = {
    REQUIRED: 'REQUIRED',
    MIN_LENGTH: 'MIN_LENGTH',
    MAX_LENGTH: 'MAX_LENGTH',
    INVALID_FORMAT: 'INVALID_FORMAT',
    INVALID_EMAIL: 'INVALID_EMAIL',
    INVALID_URL: 'INVALID_URL',
    INVALID_TICKER: 'INVALID_TICKER',
    CUSTOM_ERROR: 'CUSTOM_ERROR'
} as const;

export const VALIDATION_ERROR_MESSAGES = {
    [VALIDATION_ERROR_CODES.REQUIRED]: 'This field is required',
    [VALIDATION_ERROR_CODES.MIN_LENGTH]: 'Minimum length not met',
    [VALIDATION_ERROR_CODES.MAX_LENGTH]: 'Maximum length exceeded',
    [VALIDATION_ERROR_CODES.INVALID_FORMAT]: 'Invalid format',
    [VALIDATION_ERROR_CODES.INVALID_EMAIL]: 'Please enter a valid email address',
    [VALIDATION_ERROR_CODES.INVALID_URL]: 'Please enter a valid URL',
    [VALIDATION_ERROR_CODES.INVALID_TICKER]: 'Please enter a valid stock ticker (1-5 letters)',
    [VALIDATION_ERROR_CODES.CUSTOM_ERROR]: 'Validation error'
} as const;

// Email validation pattern
const EMAIL_PATTERN = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

// URL validation pattern
const URL_PATTERN = /^https?:\/\/(www\.)?[-a-zA-Z0-9@:%._+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_+.~#?&//=]*)$/;

// Stock ticker validation pattern
const TICKER_PATTERN = /^[A-Z]{1,5}$/;

export function validateField(value: string, rules: ValidationRule): ValidationResult {
    // Check if field is empty
    if (!value.trim()) {
        if (rules.required) {
            return {
                isValid: false,
                errorCode: VALIDATION_ERROR_CODES.REQUIRED,
                errorMessage: VALIDATION_ERROR_MESSAGES[VALIDATION_ERROR_CODES.REQUIRED]
            };
        }
        return { isValid: true };
    }

    // Check minimum length
    if (rules.minLength && value.length < rules.minLength) {
        return {
            isValid: false,
            errorCode: VALIDATION_ERROR_CODES.MIN_LENGTH,
            errorMessage: `${VALIDATION_ERROR_MESSAGES[VALIDATION_ERROR_CODES.MIN_LENGTH]} (minimum ${rules.minLength} characters)`
        };
    }

    // Check maximum length
    if (rules.maxLength && value.length > rules.maxLength) {
        return {
            isValid: false,
            errorCode: VALIDATION_ERROR_CODES.MAX_LENGTH,
            errorMessage: `${VALIDATION_ERROR_MESSAGES[VALIDATION_ERROR_CODES.MAX_LENGTH]} (maximum ${rules.maxLength} characters)`
        };
    }

    // Check pattern validation
    if (rules.pattern && !rules.pattern.test(value)) {
        return {
            isValid: false,
            errorCode: VALIDATION_ERROR_CODES.INVALID_FORMAT,
            errorMessage: VALIDATION_ERROR_MESSAGES[VALIDATION_ERROR_CODES.INVALID_FORMAT]
        };
    }

    // Check custom validation
    if (rules.custom) {
        const customResult = rules.custom(value);
        if (!customResult.isValid) {
            return customResult;
        }
    }

    return { isValid: true };
}

// Specific validation functions
export function validateEmail(value: string): ValidationResult {
    if (!value.trim()) {
        return { isValid: true }; // Empty is valid if not required
    }

    if (!EMAIL_PATTERN.test(value)) {
        return {
            isValid: false,
            errorCode: VALIDATION_ERROR_CODES.INVALID_EMAIL,
            errorMessage: VALIDATION_ERROR_MESSAGES[VALIDATION_ERROR_CODES.INVALID_EMAIL]
        };
    }

    return { isValid: true };
}

export function validateUrl(value: string): ValidationResult {
    if (!value.trim()) {
        return { isValid: true }; // Empty is valid if not required
    }

    if (!URL_PATTERN.test(value)) {
        return {
            isValid: false,
            errorCode: VALIDATION_ERROR_CODES.INVALID_URL,
            errorMessage: VALIDATION_ERROR_MESSAGES[VALIDATION_ERROR_CODES.INVALID_URL]
        };
    }

    return { isValid: true };
}

export function validateTicker(value: string): ValidationResult {
    if (!value.trim()) {
        return { isValid: true }; // Empty is valid if not required
    }

    if (!TICKER_PATTERN.test(value)) {
        return {
            isValid: false,
            errorCode: VALIDATION_ERROR_CODES.INVALID_TICKER,
            errorMessage: VALIDATION_ERROR_MESSAGES[VALIDATION_ERROR_CODES.INVALID_TICKER]
        };
    }

    return { isValid: true };
}

// Validation state management
export type ValidationState = 'valid' | 'invalid' | 'pending' | 'warning';

export interface ValidationStateInfo {
    state: ValidationState;
    errorCode?: string;
    errorMessage?: string;
    isValid: boolean;
}

export function getValidationState(
    value: string,
    rules: ValidationRule,
    isTouched: boolean = false
): ValidationStateInfo {
    if (!isTouched && !value.trim()) {
        return { state: 'valid', isValid: true };
    }

    const result = validateField(value, rules);

    if (result.isValid) {
        return { state: 'valid', isValid: true };
    }

    return {
        state: 'invalid',
        isValid: false,
        errorCode: result.errorCode,
        errorMessage: result.errorMessage
    };
}
