// Message formatting utilities for enhanced display

export type MessageType = 'user' | 'ai' | 'system' | 'error' | 'warning' | 'info';

export interface MessageFormattingOptions {
    type: MessageType;
    content: string;
    timestamp: Date;
    metadata?: {
        processingTime?: number;
        isError?: boolean;
        errorType?: string;
    };
}

export interface FormattedMessage {
    type: MessageType;
    content: string;
    formattedContent: string;
    timestamp: Date;
    relativeTime: string;
    absoluteTime: string;
    processingTime?: string;
    isError: boolean;
    errorType?: string;
    cssClass: string;
    ariaLabel: string;
}

// Relative time formatting
export function formatRelativeTime(date: Date): string {
    const now = new Date();
    const diffInSeconds = Math.floor((now.getTime() - date.getTime()) / 1000);

    if (diffInSeconds < 60) {
        return 'Just now';
    }

    const diffInMinutes = Math.floor(diffInSeconds / 60);
    if (diffInMinutes < 60) {
        return `${diffInMinutes} minute${diffInMinutes === 1 ? '' : 's'} ago`;
    }

    const diffInHours = Math.floor(diffInMinutes / 60);
    if (diffInHours < 24) {
        return `${diffInHours} hour${diffInHours === 1 ? '' : 's'} ago`;
    }

    const diffInDays = Math.floor(diffInHours / 24);
    if (diffInDays < 7) {
        return `${diffInDays} day${diffInDays === 1 ? '' : 's'} ago`;
    }

    const diffInWeeks = Math.floor(diffInDays / 7);
    if (diffInWeeks < 4) {
        return `${diffInWeeks} week${diffInWeeks === 1 ? '' : 's'} ago`;
    }

    const diffInMonths = Math.floor(diffInDays / 30);
    if (diffInMonths < 12) {
        return `${diffInMonths} month${diffInMonths === 1 ? '' : 's'} ago`;
    }

    const diffInYears = Math.floor(diffInDays / 365);
    return `${diffInYears} year${diffInYears === 1 ? '' : 's'} ago`;
}

// Absolute time formatting
export function formatAbsoluteTime(date: Date): string {
    return date.toLocaleString('en-US', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: false
    });
}

// Message type-specific CSS classes
export function getMessageTypeClass(type: MessageType): string {
    const baseClass = 'message';

    switch (type) {
        case 'user':
            return `${baseClass} user-message`;
        case 'ai':
            return `${baseClass} ai-message`;
        case 'system':
            return `${baseClass} system-message`;
        case 'error':
            return `${baseClass} error-message`;
        case 'warning':
            return `${baseClass} warning-message`;
        case 'info':
            return `${baseClass} info-message`;
        default:
            return baseClass;
    }
}

// Message type-specific ARIA labels
export function getMessageAriaLabel(type: MessageType, timestamp: Date, isError: boolean): string {
    const timeStr = formatRelativeTime(timestamp);

    switch (type) {
        case 'user':
            return `Your message sent ${timeStr}`;
        case 'ai':
            return `AI response received ${timeStr}`;
        case 'system':
            return `System notification ${timeStr}`;
        case 'error':
            return `Error message ${timeStr}`;
        case 'warning':
            return `Warning message ${timeStr}`;
        case 'info':
            return `Information message ${timeStr}`;
        default:
            return `Message ${timeStr}`;
    }
}

// Content formatting based on message type
export function formatMessageContent(content: string, type: MessageType): string {
    switch (type) {
        case 'error':
            return `❌ ${content}`;
        case 'warning':
            return `⚠️ ${content}`;
        case 'info':
            return `ℹ️ ${content}`;
        case 'system':
            return `🔧 ${content}`;
        default:
            return content;
    }
}

// Main message formatting function
export function formatMessage(options: MessageFormattingOptions): FormattedMessage {
    const {
        type,
        content,
        timestamp,
        metadata = {}
    } = options;

    const isError = metadata.isError || type === 'error';
    const processingTime = metadata.processingTime
        ? `${metadata.processingTime.toFixed(1)}s`
        : undefined;

    return {
        type,
        content,
        formattedContent: formatMessageContent(content, type),
        timestamp,
        relativeTime: formatRelativeTime(timestamp),
        absoluteTime: formatAbsoluteTime(timestamp),
        processingTime,
        isError,
        errorType: metadata.errorType,
        cssClass: getMessageTypeClass(type),
        ariaLabel: getMessageAriaLabel(type, timestamp, isError)
    };
}

// Error message type detection
export function detectErrorType(content: string): string {
    const lowerContent = content.toLowerCase();

    if (lowerContent.includes('network') || lowerContent.includes('connection')) {
        return 'network';
    }
    if (lowerContent.includes('validation') || lowerContent.includes('invalid')) {
        return 'validation';
    }
    if (lowerContent.includes('timeout') || lowerContent.includes('expired')) {
        return 'timeout';
    }
    if (lowerContent.includes('permission') || lowerContent.includes('unauthorized')) {
        return 'permission';
    }
    if (lowerContent.includes('server') || lowerContent.includes('internal')) {
        return 'server';
    }

    return 'general';
}

// Message content validation
export function validateMessageContent(content: string): {
    isValid: boolean;
    issues: string[];
} {
    const issues: string[] = [];

    if (!content || content.trim().length === 0) {
        issues.push('Message content cannot be empty');
    }

    if (content.length > 10000) {
        issues.push('Message content is too long (max 10,000 characters)');
    }

    // Check for potentially harmful content
    const suspiciousPatterns = [
        /<script/i,
        /javascript:/i,
        /on\w+\s*=/i
    ];

    for (const pattern of suspiciousPatterns) {
        if (pattern.test(content)) {
            issues.push('Message contains potentially harmful content');
            break;
        }
    }

    return {
        isValid: issues.length === 0,
        issues
    };
}
