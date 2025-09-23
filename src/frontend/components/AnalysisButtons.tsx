/**
 * AnalysisButtons Component
 * 
 * Provides direct analysis buttons for SNAPSHOT, SUPPORT/RESISTANCE, and TECHNICAL analysis.
 * Features:
 * - One-click analysis with automatic ticker detection
 * - Real-time button states (loading, success, error)
 * - Direct message sending without intermediate steps
 * - Accessibility support with proper ARIA labels
 * - Mobile-responsive design
 */
import React, { useCallback, useState } from 'react';
import { AnalysisButtonProps, AnalysisButtonType, ButtonState } from '../types/chat_OpenAI';

type AnalysisButtonsState = {
    [key in AnalysisButtonType]: ButtonState;
}

const AnalysisButtons: React.FC<AnalysisButtonProps> = ({
    onButtonClick,
    isLoading,
    currentTicker,
    disabled = false
}) => {
    const [buttonStates, setButtonStates] = useState<AnalysisButtonsState>({
        SNAPSHOT: { loading: false, success: false, error: null },
        SUPPORT_RESISTANCE: { loading: false, success: false, error: null },
        TECHNICAL: { loading: false, success: false, error: null }
    });

    const handleButtonClick = useCallback((buttonType: AnalysisButtonType) => {
        // Set loading state
        setButtonStates(prev => ({
            ...prev,
            [buttonType]: { loading: true, success: false, error: null }
        }));

        try {
            // Call the parent handler
            onButtonClick(buttonType, currentTicker);

            // Set success state
            setButtonStates(prev => ({
                ...prev,
                [buttonType]: { loading: false, success: true, error: null }
            }));

            // Reset success state after 2 seconds
            setTimeout(() => {
                setButtonStates(prev => ({
                    ...prev,
                    [buttonType]: { loading: false, success: false, error: null }
                }));
            }, 2000);

        } catch (error) {
            // Set error state
            setButtonStates(prev => ({
                ...prev,
                [buttonType]: {
                    loading: false,
                    success: false,
                    error: error instanceof Error ? error.message : 'Unknown error'
                }
            }));

            // Reset error state after 3 seconds
            setTimeout(() => {
                setButtonStates(prev => ({
                    ...prev,
                    [buttonType]: { loading: false, success: false, error: null }
                }));
            }, 3000);
        }
    }, [onButtonClick, currentTicker]);

    const getButtonText = (buttonType: AnalysisButtonType): string => {
        const state = buttonStates[buttonType] as ButtonState;
        if (state.loading) return 'Loading...';
        if (state.success) return 'Sent!';
        if (state.error) return 'Error';

        switch (buttonType) {
            case 'SNAPSHOT': return 'Snapshot';
            case 'SUPPORT_RESISTANCE': return 'Support/Resistance';
            case 'TECHNICAL': return 'Technical';
            default: return buttonType;
        }
    };

    const getButtonStyle = (buttonType: AnalysisButtonType): string => {
        const state = buttonStates[buttonType] as ButtonState;
        const baseStyle = "px-4 py-2 rounded-lg font-medium transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed";

        if (state.loading) return `${baseStyle} bg-blue-100 text-blue-700 cursor-wait`;
        if (state.success) return `${baseStyle} bg-green-100 text-green-700`;
        if (state.error) return `${baseStyle} bg-red-100 text-red-700`;

        return `${baseStyle} bg-blue-600 text-white hover:bg-blue-700 active:bg-blue-800`;
    };

    const buttons: { type: AnalysisButtonType; label: string }[] = [
        { type: 'SNAPSHOT', label: 'Snapshot' },
        { type: 'SUPPORT_RESISTANCE', label: 'Support/Resistance' },
        { type: 'TECHNICAL', label: 'Technical' }
    ];

    return (
        <div className="flex flex-wrap gap-2 p-4 bg-gray-50 rounded-lg">
            <div className="w-full mb-2">
                <h3 className="text-sm font-medium text-gray-700 mb-1">Quick Analysis</h3>
                {currentTicker && (
                    <p className="text-xs text-gray-500">Ticker: {currentTicker}</p>
                )}
            </div>

            {buttons.map(({ type, label }) => {
                const state = buttonStates[type] as ButtonState;
                const isDisabled = disabled || isLoading || state.loading;

                return (
                    <button
                        key={type}
                        type="button"
                        onClick={() => handleButtonClick(type)}
                        disabled={isDisabled}
                        className={getButtonStyle(type)}
                        aria-label={`${label} analysis for ${currentTicker || 'current ticker'}`}
                        title={`Send ${label} analysis request${currentTicker ? ` for ${currentTicker}` : ''}`}
                    >
                        {getButtonText(type)}
                    </button>
                );
            })}

            {Object.values(buttonStates).some((state: ButtonState) => state.error) && (
                <div className="w-full mt-2">
                    <p className="text-xs text-red-600">
                        Some requests failed. Please try again.
                    </p>
                </div>
            )}
        </div>
    );
};

export default AnalysisButtons;
