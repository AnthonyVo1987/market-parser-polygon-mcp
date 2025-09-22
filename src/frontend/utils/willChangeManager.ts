/**
 * Will-change Management Utility
 * 
 * This utility provides dynamic will-change property management
 * to optimize performance by applying will-change only when needed
 * and removing it after animations complete.
 */

export class WillChangeManager {
    private static instance: WillChangeManager;
    private activeElements: Map<HTMLElement, string[]> = new Map();

    static getInstance(): WillChangeManager {
        if (!WillChangeManager.instance) {
            WillChangeManager.instance = new WillChangeManager();
        }
        return WillChangeManager.instance;
    }

    /**
     * Apply will-change properties to an element
     * @param element - The HTML element to apply will-change to
     * @param properties - Array of CSS properties to optimize
     */
    apply(element: HTMLElement, properties: string[]): void {
        if (!element) return;

        const currentProperties = this.activeElements.get(element) || [];
        const newProperties = [...new Set([...currentProperties, ...properties])];

        element.style.willChange = newProperties.join(', ');
        this.activeElements.set(element, newProperties);
    }

    /**
     * Remove will-change properties from an element
     * @param element - The HTML element to remove will-change from
     * @param properties - Optional array of specific properties to remove
     */
    remove(element: HTMLElement, properties?: string[]): void {
        if (!element) return;

        if (!properties) {
            // Remove all will-change properties
            element.style.willChange = 'auto';
            this.activeElements.delete(element);
            return;
        }

        const currentProperties = this.activeElements.get(element) || [];
        const remainingProperties = currentProperties.filter(prop => !properties.includes(prop));

        if (remainingProperties.length === 0) {
            element.style.willChange = 'auto';
            this.activeElements.delete(element);
        } else {
            element.style.willChange = remainingProperties.join(', ');
            this.activeElements.set(element, remainingProperties);
        }
    }

    /**
     * Remove will-change after a specified delay
     * @param element - The HTML element
     * @param delay - Delay in milliseconds
     * @param properties - Optional array of specific properties to remove
     */
    removeAfterDelay(element: HTMLElement, delay: number, properties?: string[]): void {
        setTimeout(() => {
            this.remove(element, properties);
        }, delay);
    }

    /**
     * Clean up all will-change properties
     */
    cleanup(): void {
        this.activeElements.forEach((_, element) => {
            element.style.willChange = 'auto';
        });
        this.activeElements.clear();
    }

    /**
     * Get current will-change properties for an element
     * @param element - The HTML element
     * @returns Array of current will-change properties
     */
    getCurrentProperties(element: HTMLElement): string[] {
        return this.activeElements.get(element) || [];
    }
}

// Export singleton instance
export const willChangeManager = WillChangeManager.getInstance();

// Utility functions for common use cases
export const applyWillChange = (element: HTMLElement, properties: string[]) => {
    willChangeManager.apply(element, properties);
};

export const removeWillChange = (element: HTMLElement, properties?: string[]) => {
    willChangeManager.remove(element, properties);
};

export const removeWillChangeAfterDelay = (element: HTMLElement, delay: number, properties?: string[]) => {
    willChangeManager.removeAfterDelay(element, delay, properties);
};
