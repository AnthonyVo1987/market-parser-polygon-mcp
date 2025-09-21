// Phase 4: Performance Monitoring Utilities
// Real-time performance tracking and optimization tools

import React, { Suspense, lazy, memo, useEffect, useState } from 'react';

export interface PerformanceMetrics {
    fcp: number; // First Contentful Paint
    lcp: number; // Largest Contentful Paint
    cls: number; // Cumulative Layout Shift
    tti: number; // Time to Interactive
    fid: number; // First Input Delay
    ttfb: number; // Time to First Byte
}

export interface PerformanceBudget {
    fcp: number; // < 1.5s
    lcp: number; // < 2.5s
    cls: number; // < 0.1
    tti: number; // < 3.5s
    fid: number; // < 100ms
    ttfb: number; // < 600ms
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
};

export const BUNDLE_SIZE_BUDGET: BundleSizeBudget = {
    js: 250 * 1024,   // 250KB
    css: 50 * 1024,   // 50KB
    total: 300 * 1024, // 300KB
};

// Phase 4: Performance Monitoring Class
export class PerformanceMonitor {
    private metrics: Partial<PerformanceMetrics> = {};
    private observers: PerformanceObserver[] = [];
    // private isMonitoring = false;

    constructor() {
        this.initializeObservers();
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
            console.warn('FCP observer not supported:', error);
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
            console.warn('LCP observer not supported:', error);
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
            console.warn('CLS observer not supported:', error);
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
            console.warn('FID observer not supported:', error);
        }
    }

    private checkBudget(metric: keyof PerformanceBudget, value: number): void {
        const budget = PERFORMANCE_BUDGET[metric];
        if (value > budget) {
            console.warn(`Performance budget exceeded for ${metric}:`, {
                value: `${value}ms`,
                budget: `${budget}ms`,
                exceeded: value - budget,
            });
        }
    }

    public startMonitoring(): void {
        // this.isMonitoring = true;
        console.log('Performance monitoring started');
    }

    public stopMonitoring(): void {
        // this.isMonitoring = false;
        this.observers.forEach(observer => observer.disconnect());
        this.observers = [];
        console.log('Performance monitoring stopped');
    }

    public getMetrics(): Partial<PerformanceMetrics> {
        return { ...this.metrics };
    }

    public getReport(): {
        metrics: Partial<PerformanceMetrics>;
        budgets: PerformanceBudget;
        violations: Array<{ metric: string; value: number; budget: number }>;
    } {
        const violations: Array<{ metric: string; value: number; budget: number }> = [];

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
            }
        });

        return {
            metrics: this.metrics,
            budgets: PERFORMANCE_BUDGET,
            violations,
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
    const [monitor] = useState(() => new PerformanceMonitor());
    const [metrics, setMetrics] = useState<Partial<PerformanceMetrics>>({});

    useEffect(() => {
        monitor.startMonitoring();

        const interval = setInterval(() => {
            setMetrics(monitor.getMetrics());
        }, 1000);

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
            console.log('Component performance metrics:', metrics);
        }, [metrics]);

        return <Component {...props} />;
    });

    return WrappedComponent as unknown as React.ComponentType<P>;
}

// Phase 4: Lazy Loading Utilities
export function createLazyComponent<T extends React.ComponentType<any>>(
    importFunc: () => Promise<{ default: T }>,
    fallback?: React.ReactNode
): React.ComponentType<React.ComponentProps<T>> {
    const LazyComponent = lazy(importFunc);

    return (props: React.ComponentProps<T>) => (
        <Suspense fallback={fallback || <div>Loading...</div>}>
            <LazyComponent {...props} />
        </Suspense>
    );
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