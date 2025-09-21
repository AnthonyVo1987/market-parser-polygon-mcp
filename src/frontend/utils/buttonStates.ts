// Button state management utility for consistent user experience
import { useEffect, useState } from 'react';

export type ButtonState = 'idle' | 'loading' | 'success' | 'error' | 'disabled';

export interface ButtonStateInfo {
    state: ButtonState;
    isLoading: boolean;
    isDisabled: boolean;
    canInteract: boolean;
    displayText: string;
    ariaLabel: string;
}

export interface ButtonStateOptions {
    initialState?: ButtonState;
    loadingText?: string;
    successText?: string;
    errorText?: string;
    idleText: string;
    disabledText?: string;
    timeoutMs?: number;
    onStateChange?: (newState: ButtonState) => void;
}

export class ButtonStateManager {
    private currentState: ButtonState;
    private options: Required<ButtonStateOptions>;
    private timeoutId: NodeJS.Timeout | null = null;

    constructor(options: ButtonStateOptions) {
        this.currentState = options.initialState || 'idle';
        this.options = {
            initialState: 'idle',
            loadingText: 'Loading...',
            successText: 'Success!',
            errorText: 'Error',
            disabledText: 'Disabled',
            timeoutMs: 3000,
            onStateChange: () => { },
            ...options
        };
    }

    getStateInfo(): ButtonStateInfo {
        const { state } = this;
        const isLoading = state === 'loading';
        const isDisabled = state === 'disabled';
        const canInteract = !isLoading && !isDisabled;

        let displayText: string;
        let ariaLabel: string;

        switch (state) {
            case 'loading':
                displayText = this.options.loadingText;
                ariaLabel = `${this.options.idleText} - ${this.options.loadingText}`;
                break;
            case 'success':
                displayText = this.options.successText;
                ariaLabel = `${this.options.idleText} - ${this.options.successText}`;
                break;
            case 'error':
                displayText = this.options.errorText;
                ariaLabel = `${this.options.idleText} - ${this.options.errorText}`;
                break;
            case 'disabled':
                displayText = this.options.disabledText;
                ariaLabel = `${this.options.idleText} - ${this.options.disabledText}`;
                break;
            default:
                displayText = this.options.idleText;
                ariaLabel = this.options.idleText;
        }

        return {
            state,
            isLoading,
            isDisabled,
            canInteract,
            displayText,
            ariaLabel
        };
    }

    setState(newState: ButtonState): void {
        if (this.currentState === newState) return;

        // Clear existing timeout
        if (this.timeoutId) {
            clearTimeout(this.timeoutId);
            this.timeoutId = null;
        }

        this.currentState = newState;
        this.options.onStateChange(newState);

        // Auto-transition from success/error back to idle
        if (newState === 'success' || newState === 'error') {
            this.timeoutId = setTimeout(() => {
                this.setState('idle');
            }, this.options.timeoutMs);
        }
    }

    startLoading(): void {
        this.setState('loading');
    }

    setSuccess(): void {
        this.setState('success');
    }

    setError(): void {
        this.setState('error');
    }

    setDisabled(disabled: boolean): void {
        this.setState(disabled ? 'disabled' : 'idle');
    }

    reset(): void {
        this.setState('idle');
    }

    get state(): ButtonState {
        return this.currentState;
    }

    destroy(): void {
        if (this.timeoutId) {
            clearTimeout(this.timeoutId);
            this.timeoutId = null;
        }
    }
}

// Hook for using button state management
export function useButtonState(options: ButtonStateOptions) {
    const [stateManager] = useState(() => new ButtonStateManager(options));
    const [stateInfo, setStateInfo] = useState(() => stateManager.getStateInfo());

    useEffect(() => {
        const updateState = () => setStateInfo(stateManager.getStateInfo());

        // Update state when manager state changes
        const interval = setInterval(updateState, 100);

        return () => {
            clearInterval(interval);
            stateManager.destroy();
        };
    }, [stateManager]);

    return {
        ...stateInfo,
        startLoading: () => stateManager.startLoading(),
        setSuccess: () => stateManager.setSuccess(),
        setError: () => stateManager.setError(),
        setDisabled: (disabled: boolean) => stateManager.setDisabled(disabled),
        reset: () => stateManager.reset()
    };
}

// Button state validation
export function validateButtonState(state: ButtonState): {
    isValid: boolean;
    issues: string[];
} {
    const issues: string[] = [];

    if (!['idle', 'loading', 'success', 'error', 'disabled'].includes(state)) {
        issues.push('Invalid button state');
    }

    return {
        isValid: issues.length === 0,
        issues
    };
}

// Button state consistency checker
export function checkButtonStateConsistency(buttons: ButtonState[]): {
    isConsistent: boolean;
    issues: string[];
} {
    const issues: string[] = [];
    const stateCounts = buttons.reduce((acc, state) => {
        acc[state] = (acc[state] || 0) + 1;
        return acc;
    }, {} as Record<ButtonState, number>);

    // Check for too many loading states
    if (stateCounts.loading > 1) {
        issues.push('Multiple buttons in loading state');
    }

    // Check for mixed success/error states
    if (stateCounts.success > 0 && stateCounts.error > 0) {
        issues.push('Mixed success and error states detected');
    }

    return {
        isConsistent: issues.length === 0,
        issues
    };
}
