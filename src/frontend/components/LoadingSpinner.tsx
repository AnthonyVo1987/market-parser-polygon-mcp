import { FC } from 'react';

interface LoadingSpinnerProps {
    size?: 'sm' | 'md' | 'lg';
    color?: string;
    className?: string;
    'data-testid'?: string;
}

const LoadingSpinner: FC<LoadingSpinnerProps> = ({
    size = 'md',
    color = 'currentColor',
    className = '',
    'data-testid': dataTestId = 'loading-spinner'
}) => {
    const sizeClasses = {
        sm: 'w-4 h-4',
        md: 'w-6 h-6',
        lg: 'w-8 h-8'
    };

    return (
        <div
            className={`inline-block animate-spin ${sizeClasses[size]} ${className}`}
            data-testid={dataTestId}
            role="status"
            aria-label="Loading"
        >
            <svg
                className="w-full h-full"
                viewBox="0 0 24 24"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
            >
                <circle
                    cx="12"
                    cy="12"
                    r="10"
                    stroke={color}
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeDasharray="60 20"
                    opacity="0.3"
                />
                <circle
                    cx="12"
                    cy="12"
                    r="10"
                    stroke={color}
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeDasharray="15 65"
                    strokeDashoffset="15"
                    opacity="1"
                />
            </svg>
        </div>
    );
};

export default LoadingSpinner;
