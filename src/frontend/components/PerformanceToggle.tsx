// Performance Mode Toggle Component
// Allows users to switch between performance-optimized and full-featured modes

import React, { useEffect, useState } from 'react';

interface PerformanceToggleProps {
    onToggle?: (isPerformanceMode: boolean) => void;
    className?: string;
}

export const PerformanceToggle: React.FC<PerformanceToggleProps> = ({
    onToggle,
    className = ''
}) => {
    const [isPerformanceMode, setIsPerformanceMode] = useState<boolean>(() => {
        // Check localStorage for saved preference
        if (typeof window !== 'undefined') {
            const saved = localStorage.getItem('performance-mode');
            return saved === 'true';
        }
        return false;
    });

    useEffect(() => {
        // Apply performance mode class to document body
        if (typeof document !== 'undefined') {
            if (isPerformanceMode) {
                document.body.classList.add('performance-mode');
            } else {
                document.body.classList.remove('performance-mode');
            }
        }

        // Save preference to localStorage
        if (typeof window !== 'undefined') {
            localStorage.setItem('performance-mode', isPerformanceMode.toString());
        }

        // Notify parent component
        onToggle?.(isPerformanceMode);
    }, [isPerformanceMode, onToggle]);

    const handleToggle = () => {
        setIsPerformanceMode(prev => !prev);
    };

    return (
        <div className={`performance-toggle ${className}`}>
            <label className="performance-toggle__label">
                <input
                    type="checkbox"
                    checked={isPerformanceMode}
                    onChange={handleToggle}
                    className="performance-toggle__input"
                    aria-label="Toggle performance mode"
                />
                <span className="performance-toggle__slider">
                    <span className="performance-toggle__text">
                        {isPerformanceMode ? 'Performance Mode' : 'Full Features'}
                    </span>
                </span>
            </label>
        </div>
    );
};

export default PerformanceToggle;
