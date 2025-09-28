import { FC, ReactNode, useState } from 'react';

interface CollapsiblePanelProps {
    title: string;
    children: ReactNode;
    defaultExpanded?: boolean;
    className?: string;
    'data-testid'?: string;
}

const CollapsiblePanel: FC<CollapsiblePanelProps> = ({
    title,
    children,
    defaultExpanded = true,
    className = '',
    'data-testid': dataTestId,
}) => {
    const [isExpanded, setIsExpanded] = useState(defaultExpanded);

    const toggleExpanded = () => {
        setIsExpanded(!isExpanded);
    };

    return (
        <section
            className={`collapsible-panel ${className} ${isExpanded ? 'expanded' : 'collapsed'}`}
            data-testid={dataTestId}
        >
            <div className="collapsible-panel-header" onClick={toggleExpanded}>
                <h4 className="collapsible-panel-title">{title}</h4>
                <button
                    className="collapsible-panel-toggle"
                    aria-label={isExpanded ? 'Collapse panel' : 'Expand panel'}
                    aria-expanded={isExpanded}
                >
                    <svg
                        className={`collapsible-panel-icon ${isExpanded ? 'expanded' : 'collapsed'}`}
                        viewBox="0 0 24 24"
                        fill="none"
                        xmlns="http://www.w3.org/2000/svg"
                    >
                        <path
                            d="M6 9l6 6 6-6"
                            stroke="currentColor"
                            strokeWidth="2"
                            strokeLinecap="round"
                            strokeLinejoin="round"
                        />
                    </svg>
                </button>
            </div>
            {isExpanded && (
                <div className="collapsible-panel-content">
                    {children}
                </div>
            )}
        </section>
    );
};

export default CollapsiblePanel;
