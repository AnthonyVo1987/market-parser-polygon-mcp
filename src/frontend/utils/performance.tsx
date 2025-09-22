// Phase 4: Performance Monitoring Utilities
// Real-time performance tracking and optimization tools

import React, { Suspense, lazy, memo, useEffect, useMemo, useState } from 'react';

export interface PerformanceMetrics {
    fcp: number; // First Contentful Paint
    lcp: number; // Largest Contentful Paint
    cls: number; // Cumulative Layout Shift
    tti: number; // Time to Interactive
    fid: number; // First Input Delay
    ttfb: number; // Time to First Byte
    // Optimization-specific metrics
    backdropFilterCount: number; // Number of backdrop-filter instances
    boxShadowCount: number; // Number of complex box-shadow instances
    gradientCount: number; // Number of gradient backgrounds
    transformCount: number; // Number of transform animations
    willChangeCount: number; // Number of will-change properties
    cssVariableCount: number; // Number of CSS variables
    containerQueryCount: number; // Number of container queries
}

export interface PerformanceBudget {
    fcp: number; // < 1.5s
    lcp: number; // < 2.5s
    cls: number; // < 0.1
    tti: number; // < 3.5s
    fid: number; // < 100ms
    ttfb: number; // < 600ms
    // Optimization-specific budgets
    backdropFilterCount: number; // < 0 (target: remove all)
    boxShadowCount: number; // < 10 (target: simplify)
    gradientCount: number; // < 5 (target: remove most)
    transformCount: number; // < 5 (target: remove most)
    willChangeCount: number; // < 3 (target: dynamic only)
    cssVariableCount: number; // < 25 (target: consolidate)
    containerQueryCount: number; // < 2 (target: replace with media queries)
}

export interface BundleSizeBudget {
    js: number; // < 250KB
    css: number; // < 50KB
    total: number; // < 300KB
}

// Phase 4: Performance Budgets
export const PERFORMANCE_BUDGET: PerformanceBudget = {
    fcp: 1500, // 1.5s
    lcp: 2500, // 2.5s
    cls: 0.1,  // 0.1
    tti: 3500, // 3.5s
    fid: 100,  // 100ms
    ttfb: 600, // 600ms
    // Optimization-specific budgets
    backdropFilterCount: 0, // Target: remove all
    boxShadowCount: 10, // Target: simplify to < 10
    gradientCount: 5, // Target: remove most, keep < 5
    transformCount: 5, // Target: remove most, keep < 5
    willChangeCount: 3, // Target: dynamic only, < 3
    cssVariableCount: 25, // Target: consolidate to < 25
    containerQueryCount: 2, // Target: replace with media queries, < 2
};

export const BUNDLE_SIZE_BUDGET: BundleSizeBudget = {
    js: 250 * 1024,   // 250KB
    css: 50 * 1024,   // 50KB
    total: 300 * 1024, // 300KB
};

// Phase 4: CSS Analysis Functions
export function analyzeCSSPerformance(): Partial<PerformanceMetrics> {
    const metrics: Partial<PerformanceMetrics> = {
        backdropFilterCount: 0,
        boxShadowCount: 0,
        gradientCount: 0,
        transformCount: 0,
        willChangeCount: 0,
        cssVariableCount: 0,
        containerQueryCount: 0,
    };

    if (typeof window === 'undefined') {
        return metrics;
    }

    // Count backdrop-filter instances
    const backdropFilterElements = document.querySelectorAll('*');
    backdropFilterElements.forEach(element => {
        const computedStyle = window.getComputedStyle(element);
        if (computedStyle.backdropFilter !== 'none' || computedStyle.webkitBackdropFilter !== 'none') {
            metrics.backdropFilterCount!++;
        }
    });

    // Count complex box-shadow instances
    const boxShadowElements = document.querySelectorAll('*');
    boxShadowElements.forEach(element => {
        const computedStyle = window.getComputedStyle(element);
        if (computedStyle.boxShadow !== 'none') {
            // Count multiple shadows (comma-separated)
            const shadowCount = (computedStyle.boxShadow.match(/,/g) || []).length + 1;
            if (shadowCount > 1) {
                metrics.boxShadowCount! += shadowCount;
            }
        }
    });

    // Count gradient backgrounds
    const gradientElements = document.querySelectorAll('*');
    gradientElements.forEach(element => {
        const computedStyle = window.getComputedStyle(element);
        if (computedStyle.backgroundImage.includes('gradient')) {
            metrics.gradientCount!++;
        }
    });

    // Count transform animations
    const transformElements = document.querySelectorAll('*');
    transformElements.forEach(element => {
        const computedStyle = window.getComputedStyle(element);
        if (computedStyle.transform !== 'none') {
            metrics.transformCount!++;
        }
    });

    // Count will-change properties
    const willChangeElements = document.querySelectorAll('*');
    willChangeElements.forEach(element => {
        const computedStyle = window.getComputedStyle(element);
        if (computedStyle.willChange !== 'auto') {
            metrics.willChangeCount!++;
        }
    });

    // Count CSS variables (approximate)
    const rootStyles = getComputedStyle(document.documentElement);
    const cssText = rootStyles.cssText;
    const variableMatches = cssText.match(/--[a-zA-Z-]+/g);
    metrics.cssVariableCount = variableMatches ? variableMatches.length : 0;

    // Count container queries (approximate - would need to parse CSS)
    // This is a simplified count based on common patterns
    const containerQueryElements = document.querySelectorAll('[style*="container-type"]');
    metrics.containerQueryCount = containerQueryElements.length;

    return metrics;
}

// Phase 4: Performance Monitoring Class
export class PerformanceMonitor {
    private metrics: Partial<PerformanceMetrics> = {};
    private observers: PerformanceObserver[] = [];
    private cssMetrics: Partial<PerformanceMetrics> = {};
    // private isMonitoring = false;

    constructor() {
        this.initializeObservers();
        this.analyzeCSSPerformance();
    }

    private analyzeCSSPerformance(): void {
        this.cssMetrics = analyzeCSSPerformance();
        this.metrics = { ...this.metrics, ...this.cssMetrics };
    }

    private initializeObservers(): void {
        if (typeof window === 'undefined' || !('PerformanceObserver' in window)) {
            return;
        }

        // FCP Observer
        try {
            const fcpObserver = new PerformanceObserver((list) => {
                const entries = list.getEntries();
                const fcpEntry = entries.find(entry => entry.name === 'first-contentful-paint');
                if (fcpEntry) {
                    this.metrics.fcp = fcpEntry.startTime;
                    this.checkBudget('fcp', fcpEntry.startTime);
                }
            });
            fcpObserver.observe({ entryTypes: ['paint'] });
            this.observers.push(fcpObserver);
        } catch (error) {
            // FCP observer not supported - silently continue
        }

        // LCP Observer
        try {
            const lcpObserver = new PerformanceObserver((list) => {
                const entries = list.getEntries();
                const lastEntry = entries[entries.length - 1];
                if (lastEntry) {
                    this.metrics.lcp = lastEntry.startTime;
                    this.checkBudget('lcp', lastEntry.startTime);
                }
            });
            lcpObserver.observe({ entryTypes: ['largest-contentful-paint'] });
            this.observers.push(lcpObserver);
        } catch (error) {
            // LCP observer not supported - silently continue
        }

        // CLS Observer
        try {
            let clsValue = 0;
            const clsObserver = new PerformanceObserver((list) => {
                for (const entry of list.getEntries()) {
                    if (!(entry as any).hadRecentInput) {
                        clsValue += (entry as any).value;
                        this.metrics.cls = clsValue;
                        this.checkBudget('cls', clsValue);
                    }
                }
            });
            clsObserver.observe({ entryTypes: ['layout-shift'] });
            this.observers.push(clsObserver);
        } catch (error) {
            // CLS observer not supported - silently continue
        }

        // FID Observer
        try {
            const fidObserver = new PerformanceObserver((list) => {
                const entries = list.getEntries();
                for (const entry of entries) {
                    const fid = (entry as any).processingStart - entry.startTime;
                    this.metrics.fid = fid;
                    this.checkBudget('fid', fid);
                }
            });
            fidObserver.observe({ entryTypes: ['first-input'] });
            this.observers.push(fidObserver);
        } catch (error) {
            // FID observer not supported - silently continue
        }
    }

    private checkBudget(metric: keyof PerformanceBudget, value: number): void {
        const budget = PERFORMANCE_BUDGET[metric];
        if (value > budget) {
            // Performance budget exceeded - could be logged to analytics
        }
    }

    public startMonitoring(): void {
        // this.isMonitoring = true;
        // Performance monitoring started
        this.analyzeCSSPerformance();
    }

    public stopMonitoring(): void {
        // this.isMonitoring = false;
        this.observers.forEach(observer => observer.disconnect());
        this.observers = [];
        // Performance monitoring stopped
    }

    public getMetrics(): Partial<PerformanceMetrics> {
        // Update CSS metrics before returning
        this.analyzeCSSPerformance();
        return { ...this.metrics };
    }

    public getReport(): {
        metrics: Partial<PerformanceMetrics>;
        budgets: PerformanceBudget;
        violations: Array<{ metric: string; value: number; budget: number }>;
        regressionAlerts: Array<{ metric: string; current: number; previous: number; change: number }>;
    } {
        const violations: Array<{ metric: string; value: number; budget: number }> = [];
        const regressionAlerts: Array<{ metric: string; current: number; previous: number; change: number }> = [];

        Object.entries(this.metrics).forEach(([key, value]) => {
            if (value !== undefined) {
                const budget = PERFORMANCE_BUDGET[key as keyof PerformanceBudget];
                if (value > budget) {
                    violations.push({
                        metric: key,
                        value,
                        budget,
                    });
                }

                // Check for performance regression (simplified - would need historical data)
                const previousValue = this.cssMetrics[key as keyof PerformanceMetrics];
                if (previousValue !== undefined && value > previousValue) {
                    regressionAlerts.push({
                        metric: key,
                        current: value,
                        previous: previousValue,
                        change: value - previousValue,
                    });
                }
            }
        });

        return {
            metrics: this.metrics,
            budgets: PERFORMANCE_BUDGET,
            violations,
            regressionAlerts,
        };
    }
}

// Phase 4: Bundle Size Monitoring
export function getBundleSize(): Promise<BundleSizeBudget> {
    return new Promise((resolve) => {
        if (typeof window === 'undefined') {
            resolve({ js: 0, css: 0, total: 0 });
            return;
        }

        const jsSize = Array.from(document.querySelectorAll('script[src]'))
            .reduce((total, script) => {
                const src = (script as HTMLScriptElement).src;
                return total + (src ? new URL(src).pathname.length : 0);
            }, 0);

        const cssSize = Array.from(document.querySelectorAll('link[rel="stylesheet"]'))
            .reduce((total, link) => {
                const href = (link as HTMLLinkElement).href;
                return total + (href ? new URL(href).pathname.length : 0);
            }, 0);

        resolve({
            js: jsSize,
            css: cssSize,
            total: jsSize + cssSize,
        });
    });
}

// Phase 4: Performance Optimization Utilities
export function debounce<T extends (...args: any[]) => any>(
    func: T,
    wait: number
): (...args: Parameters<T>) => void {
    let timeout: ReturnType<typeof setTimeout>;
    return (...args: Parameters<T>) => {
        clearTimeout(timeout);
        timeout = setTimeout(() => func(...args), wait);
    };
}

export function throttle<T extends (...args: any[]) => any>(
    func: T,
    limit: number
): (...args: Parameters<T>) => void {
    let inThrottle: boolean;
    return (...args: Parameters<T>) => {
        if (!inThrottle) {
            func(...args);
            inThrottle = true;
            setTimeout(() => (inThrottle = false), limit);
        }
    };
}

// Phase 4: Memory Usage Monitoring
export function getMemoryUsage(): {
    used: number;
    total: number;
    percentage: number;
} {
    if (typeof window === 'undefined' || !('memory' in performance)) {
        return { used: 0, total: 0, percentage: 0 };
    }

    const memory = (performance as any).memory;
    const used = memory.usedJSHeapSize;
    const total = memory.totalJSHeapSize;
    const percentage = (used / total) * 100;

    return { used, total, percentage };
}

// Phase 4: Performance Monitoring Hook
export function usePerformanceMonitoring() {
    const monitor = useMemo(() => new PerformanceMonitor(), []);
    const [metrics, setMetrics] = useState<Partial<PerformanceMetrics>>({
        fcp: 0,
        lcp: 0,
        cls: 0,
        tti: 0,
        fid: 0,
        ttfb: 0,
        backdropFilterCount: 0,
        boxShadowCount: 0,
        gradientCount: 0,
        transformCount: 0,
        willChangeCount: 0,
        cssVariableCount: 0,
        containerQueryCount: 0
    });

    useEffect(() => {
        monitor.startMonitoring();

        const updateMetrics = () => {
            if (document.visibilityState === 'visible') {
                const currentMetrics = monitor.getMetrics();
                // Only update if we have actual values
                if (Object.keys(currentMetrics).length > 0) {
                    setMetrics(prev => ({ ...prev, ...currentMetrics }));
                }
            }
        };

        const handleIdle = () => {
            if (window.requestIdleCallback) {
                requestIdleCallback(updateMetrics, { timeout: 5000 });
            } else {
                // Fallback for browsers without requestIdleCallback
                setTimeout(updateMetrics, 0);
            }
        };

        // Initial update
        handleIdle();

        const interval = setInterval(handleIdle, 2000);

        return () => {
            clearInterval(interval);
            monitor.stopMonitoring();
        };
    }, [monitor]);

    return {
        metrics,
        getReport: () => monitor.getReport(),
        getBundleSize,
        getMemoryUsage,
    };
}

// Phase 4: Performance Optimization HOC
export function withPerformanceMonitoring<P extends object>(
    Component: React.ComponentType<P>
): React.ComponentType<P> {
    const WrappedComponent = memo((props: P) => {
        const { metrics } = usePerformanceMonitoring();

        useEffect(() => {
            // Component performance metrics could be logged to analytics
        }, [metrics]);

        return <Component {...props} />;
    });

    WrappedComponent.displayName = `withPerformanceMonitoring(${Component.displayName || Component.name || 'Component'})`;

    return WrappedComponent as unknown as React.ComponentType<P>;
}

// Phase 4: Lazy Loading Utilities
export function createLazyComponent<T extends React.ComponentType<any>>(
    importFunc: () => Promise<{ default: T }>,
    fallback?: React.ReactNode
): React.ComponentType<React.ComponentProps<T>> {
    const LazyComponent = lazy(importFunc);

    const LazyWrapper = (props: React.ComponentProps<T>) => (
        <Suspense fallback={fallback || <div>Loading...</div>}>
            <LazyComponent {...props} />
        </Suspense>
    );

    LazyWrapper.displayName = 'LazyWrapper';

    return LazyWrapper;
}

// Phase 4: Performance Budget Validation
export function validatePerformanceBudget(
    metrics: Partial<PerformanceMetrics>
): {
    isValid: boolean;
    violations: Array<{ metric: string; value: number; budget: number }>;
} {
    const violations: Array<{ metric: string; value: number; budget: number }> = [];

    Object.entries(metrics).forEach(([key, value]) => {
        if (value !== undefined) {
            const budget = PERFORMANCE_BUDGET[key as keyof PerformanceBudget];
            if (value > budget) {
                violations.push({
                    metric: key,
                    value,
                    budget,
                });
            }
        }
    });

    return {
        isValid: violations.length === 0,
        violations,
    };
}