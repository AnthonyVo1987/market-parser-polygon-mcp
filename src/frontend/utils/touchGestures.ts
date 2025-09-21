// Phase 4: Touch Gesture Utilities
// Mobile-specific touch interactions and gesture support

import { useState, useCallback, useEffect } from 'react';

export interface TouchPoint {
    x: number;
    y: number;
    id: number;
    timestamp: number;
}

export interface TouchGesture {
    type: 'swipe' | 'pinch' | 'tap' | 'longpress' | 'doubletap';
    direction?: 'left' | 'right' | 'up' | 'down';
    distance?: number;
    velocity?: number;
    scale?: number;
    duration?: number;
    center?: { x: number; y: number };
}

export interface TouchGestureConfig {
    swipeThreshold: number;
    swipeVelocityThreshold: number;
    pinchThreshold: number;
    tapThreshold: number;
    longPressThreshold: number;
    doubleTapThreshold: number;
}

// Phase 4: Default Touch Gesture Configuration
export const TOUCH_GESTURE_CONFIG: TouchGestureConfig = {
    swipeThreshold: 50, // Minimum distance for swipe
    swipeVelocityThreshold: 0.3, // Minimum velocity for swipe
    pinchThreshold: 0.1, // Minimum scale change for pinch
    tapThreshold: 300, // Maximum duration for tap
    longPressThreshold: 500, // Minimum duration for long press
    doubleTapThreshold: 300, // Maximum time between taps for double tap
};

// Phase 4: Touch Gesture Detector Class
export class TouchGestureDetector {
    private config: TouchGestureConfig;
    private touchPoints: Map<number, TouchPoint> = new Map();
    private lastTapTime: number = 0;
    private lastTapPosition: { x: number; y: number } | null = null;
    private longPressTimer: NodeJS.Timeout | null = null;
    private onGesture: (gesture: TouchGesture) => void;

    constructor(
        onGesture: (gesture: TouchGesture) => void,
        config: TouchGestureConfig = TOUCH_GESTURE_CONFIG
    ) {
        this.config = config;
        this.onGesture = onGesture;
    }

    public handleTouchStart(event: TouchEvent): void {
        const touches = Array.from(event.touches);

        touches.forEach(touch => {
            const touchPoint: TouchPoint = {
                x: touch.clientX,
                y: touch.clientY,
                id: touch.identifier,
                timestamp: Date.now(),
            };

            this.touchPoints.set(touch.identifier, touchPoint);
        });

        // Handle single touch gestures
        if (touches.length === 1) {
            this.handleSingleTouchStart(touches[0]);
        }

        // Handle multi-touch gestures
        if (touches.length === 2) {
            this.handlePinchStart(touches);
        }
    }

    public handleTouchMove(event: TouchEvent): void {
        const touches = Array.from(event.touches);

        touches.forEach(touch => {
            const existingPoint = this.touchPoints.get(touch.identifier);
            if (existingPoint) {
                existingPoint.x = touch.clientX;
                existingPoint.y = touch.clientY;
                existingPoint.timestamp = Date.now();
            }
        });

        // Handle single touch gestures
        if (touches.length === 1) {
            this.handleSingleTouchMove(touches[0]);
        }

        // Handle multi-touch gestures
        if (touches.length === 2) {
            this.handlePinchMove(touches);
        }
    }

    public handleTouchEnd(event: TouchEvent): void {
        const touches = Array.from(event.touches);
        const changedTouches = Array.from(event.changedTouches);

        // Remove ended touches
        changedTouches.forEach(touch => {
            this.touchPoints.delete(touch.identifier);
        });

        // Handle single touch gestures
        if (touches.length === 0 && changedTouches.length === 1) {
            this.handleSingleTouchEnd(changedTouches[0]);
        }

        // Handle multi-touch gestures
        if (touches.length === 1 && changedTouches.length === 1) {
            this.handlePinchEnd();
        }
    }

    private handleSingleTouchStart(touch: Touch): void {
        const touchPoint = this.touchPoints.get(touch.identifier);
        if (!touchPoint) return;

        // Start long press timer
        this.longPressTimer = setTimeout(() => {
            this.onGesture({
                type: 'longpress',
                center: { x: touchPoint.x, y: touchPoint.y },
                duration: this.config.longPressThreshold,
            });
        }, this.config.longPressThreshold);
    }

    private handleSingleTouchMove(touch: Touch): void {
        const touchPoint = this.touchPoints.get(touch.identifier);
        if (!touchPoint) return;

        // Clear long press timer if moving
        if (this.longPressTimer) {
            clearTimeout(this.longPressTimer);
            this.longPressTimer = null;
        }
    }

    private handleSingleTouchEnd(touch: Touch): void {
        const touchPoint = this.touchPoints.get(touch.identifier);
        if (!touchPoint) return;

        // Clear long press timer
        if (this.longPressTimer) {
            clearTimeout(this.longPressTimer);
            this.longPressTimer = null;
        }

        const duration = Date.now() - touchPoint.timestamp;

        // Handle tap gestures
        if (duration < this.config.tapThreshold) {
            this.handleTap(touchPoint);
        }
    }

    private handleTap(touchPoint: TouchPoint): void {
        const now = Date.now();
        const timeSinceLastTap = now - this.lastTapTime;

        // Check for double tap
        if (this.lastTapPosition &&
            timeSinceLastTap < this.config.doubleTapThreshold &&
            this.getDistance(touchPoint, this.lastTapPosition) < 50) {

            this.onGesture({
                type: 'doubletap',
                center: { x: touchPoint.x, y: touchPoint.y },
                duration: timeSinceLastTap,
            });

            this.lastTapTime = 0;
            this.lastTapPosition = null;
        } else {
            this.onGesture({
                type: 'tap',
                center: { x: touchPoint.x, y: touchPoint.y },
                duration: now - touchPoint.timestamp,
            });

            this.lastTapTime = now;
            this.lastTapPosition = { x: touchPoint.x, y: touchPoint.y };
        }
    }

    private handlePinchStart(touches: Touch[]): void {
        if (touches.length !== 2) return;

        const touch1 = this.touchPoints.get(touches[0].identifier);
        const touch2 = this.touchPoints.get(touches[1].identifier);

        if (!touch1 || !touch2) return;

        const initialDistance = this.getDistance(touch1, touch2);
        const center = this.getCenter(touch1, touch2);

        // Store initial pinch data
        (this as any).initialPinchDistance = initialDistance;
        (this as any).initialPinchCenter = center;
    }

    private handlePinchMove(touches: Touch[]): void {
        if (touches.length !== 2) return;

        const touch1 = this.touchPoints.get(touches[0].identifier);
        const touch2 = this.touchPoints.get(touches[1].identifier);

        if (!touch1 || !touch2) return;

        const currentDistance = this.getDistance(touch1, touch2);
        const initialDistance = (this as any).initialPinchDistance;

        if (initialDistance && currentDistance) {
            const scale = currentDistance / initialDistance;

            if (Math.abs(scale - 1) > this.config.pinchThreshold) {
                this.onGesture({
                    type: 'pinch',
                    scale: scale,
                    center: this.getCenter(touch1, touch2),
                });
            }
        }
    }

    private handlePinchEnd(): void {
        // Clear pinch data
        (this as any).initialPinchDistance = null;
        (this as any).initialPinchCenter = null;
    }

    private getDistance(point1: TouchPoint, point2: TouchPoint): number {
        const dx = point1.x - point2.x;
        const dy = point1.y - point2.y;
        return Math.sqrt(dx * dx + dy * dy);
    }

    private getCenter(point1: TouchPoint, point2: TouchPoint): { x: number; y: number } {
        return {
            x: (point1.x + point2.x) / 2,
            y: (point1.y + point2.y) / 2,
        };
    }

    public destroy(): void {
        if (this.longPressTimer) {
            clearTimeout(this.longPressTimer);
        }
        this.touchPoints.clear();
    }
}

// Phase 4: Mobile UX Patterns
export interface MobileUXConfig {
    hapticFeedback: boolean;
    visualFeedback: boolean;
    soundFeedback: boolean;
    gestureNavigation: boolean;
    swipeToClose: boolean;
    pullToRefresh: boolean;
}

export const MOBILE_UX_CONFIG: MobileUXConfig = {
    hapticFeedback: true,
    visualFeedback: true,
    soundFeedback: false,
    gestureNavigation: true,
    swipeToClose: true,
    pullToRefresh: true,
};

// Phase 4: Mobile UX Manager
export class MobileUXManager {
    private config: MobileUXConfig;
    private gestureDetector: TouchGestureDetector | null = null;

    constructor(config: MobileUXConfig = MOBILE_UX_CONFIG) {
        this.config = config;
    }

    public initialize(element: HTMLElement): void {
        if (!this.config.gestureNavigation) return;

        this.gestureDetector = new TouchGestureDetector((gesture) => {
            this.handleGesture(gesture);
        });

        element.addEventListener('touchstart', this.gestureDetector.handleTouchStart.bind(this.gestureDetector));
        element.addEventListener('touchmove', this.gestureDetector.handleTouchMove.bind(this.gestureDetector));
        element.addEventListener('touchend', this.gestureDetector.handleTouchEnd.bind(this.gestureDetector));
    }

    private handleGesture(gesture: TouchGesture): void {
        switch (gesture.type) {
            case 'swipe':
                this.handleSwipe(gesture);
                break;
            case 'pinch':
                this.handlePinch(gesture);
                break;
            case 'tap':
                this.handleTap(gesture);
                break;
            case 'longpress':
                this.handleLongPress(gesture);
                break;
            case 'doubletap':
                this.handleDoubleTap(gesture);
                break;
        }
    }

    private handleSwipe(gesture: TouchGesture): void {
        if (!gesture.direction) return;

        // Provide haptic feedback
        if (this.config.hapticFeedback && 'vibrate' in navigator) {
            navigator.vibrate(10);
        }

        // Handle swipe navigation
        if (gesture.direction === 'left' || gesture.direction === 'right') {
            // Swipe to close sidebar
            if (this.config.swipeToClose) {
                this.triggerSwipeToClose(gesture.direction);
            }
        }
    }

    private handlePinch(gesture: TouchGesture): void {
        if (!gesture.scale) return;

        // Provide haptic feedback
        if (this.config.hapticFeedback && 'vibrate' in navigator) {
            navigator.vibrate(5);
        }

        // Handle pinch to zoom
        this.triggerPinchToZoom(gesture.scale);
    }

    private handleTap(gesture: TouchGesture): void {
        // Provide haptic feedback
        if (this.config.hapticFeedback && 'vibrate' in navigator) {
            navigator.vibrate(5);
        }

        // Handle tap interactions
        this.triggerTap(gesture.center);
    }

    private handleLongPress(gesture: TouchGesture): void {
        // Provide haptic feedback
        if (this.config.hapticFeedback && 'vibrate' in navigator) {
            navigator.vibrate(50);
        }

        // Handle long press interactions
        this.triggerLongPress(gesture.center);
    }

    private handleDoubleTap(gesture: TouchGesture): void {
        // Provide haptic feedback
        if (this.config.hapticFeedback && 'vibrate' in navigator) {
            navigator.vibrate(10);
        }

        // Handle double tap interactions
        this.triggerDoubleTap(gesture.center);
    }

    private triggerSwipeToClose(direction: 'left' | 'right'): void {
        // Dispatch custom event for swipe to close
        const event = new CustomEvent('swipeToClose', {
            detail: { direction },
            bubbles: true,
        });
        document.dispatchEvent(event);
    }

    private triggerPinchToZoom(scale: number): void {
        // Dispatch custom event for pinch to zoom
        const event = new CustomEvent('pinchToZoom', {
            detail: { scale },
            bubbles: true,
        });
        document.dispatchEvent(event);
    }

    private triggerTap(center: { x: number; y: number } | undefined): void {
        // Dispatch custom event for tap
        const event = new CustomEvent('mobileTap', {
            detail: { center },
            bubbles: true,
        });
        document.dispatchEvent(event);
    }

    private triggerLongPress(center: { x: number; y: number } | undefined): void {
        // Dispatch custom event for long press
        const event = new CustomEvent('mobileLongPress', {
            detail: { center },
            bubbles: true,
        });
        document.dispatchEvent(event);
    }

    private triggerDoubleTap(center: { x: number; y: number } | undefined): void {
        // Dispatch custom event for double tap
        const event = new CustomEvent('mobileDoubleTap', {
            detail: { center },
            bubbles: true,
        });
        document.dispatchEvent(event);
    }

    public destroy(): void {
        if (this.gestureDetector) {
            this.gestureDetector.destroy();
        }
    }
}

// Phase 4: Mobile UX Hook
export function useMobileUX(config: MobileUXConfig = MOBILE_UX_CONFIG) {
    const [mobileUXManager] = useState(() => new MobileUXManager(config));
    const [isInitialized, setIsInitialized] = useState(false);

    const initialize = useCallback((element: HTMLElement) => {
        if (isInitialized) return;

        mobileUXManager.initialize(element);
        setIsInitialized(true);
    }, [mobileUXManager, isInitialized]);

    const destroy = useCallback(() => {
        mobileUXManager.destroy();
        setIsInitialized(false);
    }, [mobileUXManager]);

    useEffect(() => {
        return () => {
            destroy();
        };
    }, [destroy]);

    return {
        initialize,
        destroy,
        isInitialized,
    };
}

// Phase 4: Mobile Form Optimization
export function optimizeForMobile(form: HTMLFormElement): void {
    // Set input mode for better mobile keyboards
    const inputs = form.querySelectorAll('input[type="text"], input[type="email"], input[type="tel"], input[type="url"]');
    inputs.forEach(input => {
        const inputElement = input as HTMLInputElement;
        if (inputElement.type === 'email') {
            inputElement.setAttribute('inputmode', 'email');
        } else if (inputElement.type === 'tel') {
            inputElement.setAttribute('inputmode', 'tel');
        } else if (inputElement.type === 'url') {
            inputElement.setAttribute('inputmode', 'url');
        } else {
            inputElement.setAttribute('inputmode', 'text');
        }
    });

    // Set autocomplete attributes
    const emailInputs = form.querySelectorAll('input[type="email"]');
    emailInputs.forEach(input => {
        input.setAttribute('autocomplete', 'email');
    });

    const nameInputs = form.querySelectorAll('input[name*="name"]');
    nameInputs.forEach(input => {
        input.setAttribute('autocomplete', 'name');
    });

    // Set autocapitalize attributes
    const textInputs = form.querySelectorAll('input[type="text"], textarea');
    textInputs.forEach(input => {
        const inputElement = input as HTMLInputElement;
        if (inputElement.name.includes('name') || inputElement.name.includes('title')) {
            inputElement.setAttribute('autocapitalize', 'words');
        } else {
            inputElement.setAttribute('autocapitalize', 'sentences');
        }
    });
}

// Phase 4: Mobile Performance Optimization
export function optimizeForMobilePerformance(): void {
    // Disable hover effects on touch devices
    if ('ontouchstart' in window) {
        document.body.classList.add('touch-device');
    }

    // Optimize scroll performance
    let ticking = false;
    const optimizeScroll = () => {
        if (!ticking) {
            requestAnimationFrame(() => {
                // Scroll optimization logic here
                ticking = false;
            });
            ticking = true;
        }
    };

    window.addEventListener('scroll', optimizeScroll, { passive: true });

    // Optimize resize performance
    let resizeTimeout: NodeJS.Timeout;
    const optimizeResize = () => {
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(() => {
            // Resize optimization logic here
        }, 250);
    };

    window.addEventListener('resize', optimizeResize, { passive: true });
}
