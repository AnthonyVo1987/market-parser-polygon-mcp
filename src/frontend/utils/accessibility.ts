// Phase 4: Accessibility Utilities
// WCAG 2.1 AA compliance and accessibility enhancement tools

import { useCallback, useState } from 'react';

export interface AccessibilityConfig {
    colorContrast: {
        normal: number; // 4.5:1 for normal text
        large: number;  // 3:1 for large text
    };
    focusIndicators: {
        outlineWidth: string;
        outlineOffset: string;
        outlineColor: string;
    };
    keyboardNavigation: {
        tabOrder: string[];
        skipLinks: string[];
    };
    screenReader: {
        announcements: boolean;
        liveRegions: boolean;
    };
}

// Phase 4: WCAG 2.1 AA Compliance Configuration
export const ACCESSIBILITY_CONFIG: AccessibilityConfig = {
    colorContrast: {
        normal: 4.5, // WCAG AA requirement
        large: 3.0,  // WCAG AA requirement for large text
    },
    focusIndicators: {
        outlineWidth: '2px',
        outlineOffset: '2px',
        outlineColor: '#0066cc',
    },
    keyboardNavigation: {
        tabOrder: [
            'skip-link',
            'main-input',
            'ticker-input',
            'analysis-buttons',
            'export-buttons',
            'mobile-sidebar-toggle',
        ],
        skipLinks: [
            'Skip to main content',
            'Skip to navigation',
            'Skip to message input',
        ],
    },
    screenReader: {
        announcements: true,
        liveRegions: true,
    },
};

// Phase 4: Color Contrast Utilities
export function calculateContrastRatio(color1: string, color2: string): number {
    const getLuminance = (color: string): number => {
        const rgb = hexToRgb(color);
        if (!rgb) return 0;

        const { r, g, b } = rgb;
        const [rs, gs, bs] = [r, g, b].map(c => {
            c = c / 255;
            return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
        });

        return 0.2126 * rs + 0.7152 * gs + 0.0722 * bs;
    };

    const luminance1 = getLuminance(color1);
    const luminance2 = getLuminance(color2);

    const lighter = Math.max(luminance1, luminance2);
    const darker = Math.min(luminance1, luminance2);

    return (lighter + 0.05) / (darker + 0.05);
}

export function hexToRgb(hex: string): { r: number; g: number; b: number } | null {
    const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result ? {
        r: parseInt(result[1], 16),
        g: parseInt(result[2], 16),
        b: parseInt(result[3], 16)
    } : null;
}

export function validateColorContrast(
    foreground: string,
    background: string,
    size: 'normal' | 'large' = 'normal'
): {
    isValid: boolean;
    ratio: number;
    required: number;
    level: 'AA' | 'AAA' | 'FAIL';
} {
    const ratio = calculateContrastRatio(foreground, background);
    const required = size === 'large' ? 3.0 : 4.5;
    const isValid = ratio >= required;

    let level: 'AA' | 'AAA' | 'FAIL';
    if (ratio >= 7.0) level = 'AAA';
    else if (ratio >= required) level = 'AA';
    else level = 'FAIL';

    return {
        isValid,
        ratio,
        required,
        level,
    };
}

// Phase 4: Focus Management Utilities
export function createFocusTrap(container: HTMLElement): {
    activate: () => void;
    deactivate: () => void;
} {
    let firstFocusable: HTMLElement | null = null;
    let lastFocusable: HTMLElement | null = null;

    const getFocusableElements = (): HTMLElement[] => {
        const focusableSelectors = [
            'button:not([disabled])',
            'input:not([disabled])',
            'select:not([disabled])',
            'textarea:not([disabled])',
            'a[href]',
            '[tabindex]:not([tabindex="-1"])',
        ];

        return Array.from(container.querySelectorAll(focusableSelectors.join(', ')));
    };

    const handleKeyDown = (e: KeyboardEvent): void => {
        if (e.key !== 'Tab') return;

        if (e.shiftKey) {
            if (document.activeElement === firstFocusable) {
                lastFocusable?.focus();
                e.preventDefault();
            }
        } else {
            if (document.activeElement === lastFocusable) {
                firstFocusable?.focus();
                e.preventDefault();
            }
        }
    };

    const activate = (): void => {
        const focusableElements = getFocusableElements();
        if (focusableElements.length === 0) return;

        firstFocusable = focusableElements[0];
        lastFocusable = focusableElements[focusableElements.length - 1];

        container.addEventListener('keydown', handleKeyDown);
        firstFocusable.focus();
    };

    const deactivate = (): void => {
        container.removeEventListener('keydown', handleKeyDown);
    };

    return { activate, deactivate };
}

// Phase 4: ARIA Utilities
export function generateAriaLabel(
    element: string,
    context?: string,
    state?: string
): string {
    const labels: Record<string, string> = {
        'button': 'Button',
        'input': 'Input field',
        'textarea': 'Text area',
        'select': 'Select dropdown',
        'link': 'Link',
        'heading': 'Heading',
        'list': 'List',
        'listitem': 'List item',
        'navigation': 'Navigation',
        'main': 'Main content',
        'complementary': 'Complementary content',
        'banner': 'Banner',
        'contentinfo': 'Content information',
        'form': 'Form',
        'search': 'Search',
        'dialog': 'Dialog',
        'alert': 'Alert',
        'status': 'Status',
        'log': 'Log',
        'marquee': 'Marquee',
        'timer': 'Timer',
        'tablist': 'Tab list',
        'tab': 'Tab',
        'tabpanel': 'Tab panel',
        'tree': 'Tree',
        'treeitem': 'Tree item',
        'grid': 'Grid',
        'gridcell': 'Grid cell',
        'row': 'Row',
        'columnheader': 'Column header',
        'rowheader': 'Row header',
        'menubar': 'Menu bar',
        'menu': 'Menu',
        'menuitem': 'Menu item',
        'toolbar': 'Toolbar',
        'tooltip': 'Tooltip',
        'progressbar': 'Progress bar',
        'slider': 'Slider',
        'spinbutton': 'Spin button',
        'switch': 'Switch',
        'checkbox': 'Checkbox',
        'radio': 'Radio button',
        'combobox': 'Combo box',
        'textbox': 'Text box',
    };

    let label = labels[element] || element;

    if (context) {
        label += ` for ${context}`;
    }

    if (state) {
        label += ` (${state})`;
    }

    return label;
}

export function generateAriaDescribedBy(
    element: HTMLElement,
    description: string
): string {
    const id = `aria-describedby-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;

    const descriptionElement = document.createElement('div');
    descriptionElement.id = id;
    descriptionElement.className = 'sr-only';
    descriptionElement.textContent = description;

    element.parentNode?.insertBefore(descriptionElement, element.nextSibling);

    return id;
}

// Phase 4: Screen Reader Utilities
export function announceToScreenReader(message: string, priority: 'polite' | 'assertive' = 'polite'): void {
    const announcement = document.createElement('div');
    announcement.setAttribute('aria-live', priority);
    announcement.setAttribute('aria-atomic', 'true');
    announcement.className = 'sr-only';
    announcement.textContent = message;

    document.body.appendChild(announcement);

    setTimeout(() => {
        document.body.removeChild(announcement);
    }, 1000);
}

export function createLiveRegion(priority: 'polite' | 'assertive' = 'polite'): HTMLElement {
    const liveRegion = document.createElement('div');
    liveRegion.setAttribute('aria-live', priority);
    liveRegion.setAttribute('aria-atomic', 'true');
    liveRegion.className = 'sr-only';
    liveRegion.id = `live-region-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;

    return liveRegion;
}

// Phase 4: Keyboard Navigation Utilities
export function createKeyboardShortcuts(
    shortcuts: Record<string, () => void>
): {
    activate: () => void;
    deactivate: () => void;
} {
    const handleKeyDown = (e: KeyboardEvent): void => {
        const key = e.key.toLowerCase();
        const modifier = e.ctrlKey || e.metaKey;

        const shortcutKey = modifier ? `ctrl+${key}` : key;

        if (shortcuts[shortcutKey]) {
            e.preventDefault();
            shortcuts[shortcutKey]();
        }
    };

    const activate = (): void => {
        document.addEventListener('keydown', handleKeyDown);
    };

    const deactivate = (): void => {
        document.removeEventListener('keydown', handleKeyDown);
    };

    return { activate, deactivate };
}

// Phase 4: Skip Links Utilities
export function createSkipLinks(): HTMLElement {
    const skipLinksContainer = document.createElement('div');
    skipLinksContainer.className = 'skip-links-container';

    ACCESSIBILITY_CONFIG.keyboardNavigation.skipLinks.forEach((text, index) => {
        const skipLink = document.createElement('a');
        skipLink.href = `#${ACCESSIBILITY_CONFIG.keyboardNavigation.tabOrder[index] || 'main'}`;
        skipLink.className = 'skip-link';
        skipLink.textContent = text;
        skipLinksContainer.appendChild(skipLink);
    });

    return skipLinksContainer;
}

// Phase 4: Accessibility Testing Utilities
export function runAccessibilityAudit(): {
    violations: Array<{
        element: string;
        rule: string;
        description: string;
        severity: 'error' | 'warning' | 'info';
    }>;
    summary: {
        total: number;
        errors: number;
        warnings: number;
        info: number;
    };
} {
    const violations: Array<{
        element: string;
        rule: string;
        description: string;
        severity: 'error' | 'warning' | 'info';
    }> = [];

    // Check for missing alt text on images
    const images = document.querySelectorAll('img');
    images.forEach((img, index) => {
        if (!img.alt && !img.getAttribute('aria-label')) {
            violations.push({
                element: `img[${index}]`,
                rule: 'WCAG 2.1 AA - Images must have alt text',
                description: 'Image elements must have alt text or aria-label',
                severity: 'error',
            });
        }
    });

    // Check for missing form labels
    const inputs = document.querySelectorAll('input, textarea, select');
    inputs.forEach((input, index) => {
        const id = input.id;
        const label = document.querySelector(`label[for="${id}"]`);
        const ariaLabel = input.getAttribute('aria-label');
        const ariaLabelledBy = input.getAttribute('aria-labelledby');

        if (!label && !ariaLabel && !ariaLabelledBy) {
            violations.push({
                element: `input[${index}]`,
                rule: 'WCAG 2.1 AA - Form controls must have labels',
                description: 'Form controls must have associated labels',
                severity: 'error',
            });
        }
    });

    // Check for missing heading hierarchy
    const headings = document.querySelectorAll('h1, h2, h3, h4, h5, h6');
    let lastLevel = 0;
    headings.forEach((heading, index) => {
        const level = parseInt(heading.tagName.charAt(1));
        if (level > lastLevel + 1) {
            violations.push({
                element: `heading[${index}]`,
                rule: 'WCAG 2.1 AA - Heading hierarchy must be logical',
                description: `Heading level ${level} follows level ${lastLevel}`,
                severity: 'warning',
            });
        }
        lastLevel = level;
    });

    // Check for color contrast
    const elements = document.querySelectorAll('*');
    elements.forEach((element, index) => {
        const styles = window.getComputedStyle(element);
        const color = styles.color;
        const backgroundColor = styles.backgroundColor;

        if (color && backgroundColor && color !== 'rgba(0, 0, 0, 0)' && backgroundColor !== 'rgba(0, 0, 0, 0)') {
            const contrast = calculateContrastRatio(color, backgroundColor);
            if (contrast < 4.5) {
                violations.push({
                    element: `element[${index}]`,
                    rule: 'WCAG 2.1 AA - Color contrast must be at least 4.5:1',
                    description: `Color contrast ratio is ${contrast.toFixed(2)}:1`,
                    severity: 'error',
                });
            }
        }
    });

    const summary = {
        total: violations.length,
        errors: violations.filter(v => v.severity === 'error').length,
        warnings: violations.filter(v => v.severity === 'warning').length,
        info: violations.filter(v => v.severity === 'info').length,
    };

    return { violations, summary };
}

// Phase 4: Accessibility Hook
export function useAccessibility() {
    const [violations, setViolations] = useState<Array<{
        element: string;
        rule: string;
        description: string;
        severity: 'error' | 'warning' | 'info';
    }>>([]);

    const runAudit = useCallback(() => {
        const audit = runAccessibilityAudit();
        setViolations(audit.violations);
        return audit;
    }, []);

    const announce = useCallback((message: string, priority: 'polite' | 'assertive' = 'polite') => {
        announceToScreenReader(message, priority);
    }, []);

    const validateContrast = useCallback((foreground: string, background: string, size: 'normal' | 'large' = 'normal') => {
        return validateColorContrast(foreground, background, size);
    }, []);

    return {
        violations,
        runAudit,
        announce,
        validateContrast,
    };
}
