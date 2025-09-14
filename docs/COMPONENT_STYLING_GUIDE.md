# Component Styling Guide

## Overview

Comprehensive styling documentation for all 11 enhanced React components in the fintech glassmorphic design system. This guide provides implementation patterns, usage examples, responsive design strategies, and optimization techniques for each component.

## Table of Contents

1. [ChatInterface_OpenAI](#chatinterface_openai) - Main 7-section layout container
2. [ChatMessage_OpenAI](#chatmessage_openai) - Message bubble components
3. [ChatInput_OpenAI](#chatinput_openai) - Multi-line input component
4. [AnalysisButton](#analysisbutton) - Advanced state management buttons
5. [AnalysisButtons](#analysisbuttons) - Button group container
6. [SharedTickerInput](#sharedtickerinput) - Professional validation input
7. [ExportButtons](#exportbuttons) - Export functionality buttons
8. [RecentMessageButtons](#recentmessagebuttons) - Recent messages management
9. [MessageCopyButton](#messagecopybutton) - Copy functionality component
10. [DebugPanel](#debugpanel) - Developer information panel
11. [App](#app) - Root application container

---

## ChatInterface_OpenAI

### Component Overview

The main container component featuring a sophisticated 7-section glassmorphic layout with professional fintech styling and cross-platform responsive design.

### Architecture

**7-Section Layout Structure:**
```
┌─────────────────────────────────┐
│ 1. Header Section               │
├─────────────────────────────────┤
│ 2. Messages Container (Scroll)  │
├─────────────────────────────────┤
│ 3. Chat Input Section          │
├─────────────────────────────────┤
│ 4. Ticker Input Section        │
├─────────────────────────────────┤
│ 5. Analysis Buttons Section    │
├─────────────────────────────────┤
│ 6. Export/Recent Section       │
├─────────────────────────────────┤
│ 7. Debug Panel Section         │
└─────────────────────────────────┘
```

### Key Styling Features

**Glassmorphic Container:**
```css
.chat-interface-container {
  /* Uses 100dvh/100svh for mobile compatibility */
  height: 100dvh;
  height: 100svh;
  
  /* Glassmorphic background */
  background: var(--glass-surface-2);
  backdrop-filter: var(--glass-blur-md);
  border: 1px solid var(--glass-border-1);
  
  /* CSS Grid 7-section layout */
  display: grid;
  grid-template-rows: auto 1fr auto auto auto auto auto;
  gap: var(--spacing-4);
  padding: var(--spacing-4);
}
```

### Responsive Design Patterns

**Mobile (≤767px):**
```css
@media (max-width: 767px) {
  .chat-interface-container {
    padding: var(--spacing-2);
    gap: var(--spacing-2);
    
    /* iOS safe area handling */
    padding-bottom: env(safe-area-inset-bottom);
  }
  
  /* Compact section spacing */
  .section {
    padding: var(--spacing-2);
  }
}
```

**Desktop (≥768px):**
```css
@media (min-width: 768px) {
  .chat-interface-container {
    padding: var(--spacing-6);
    gap: var(--spacing-4);
    border-radius: var(--radius-2xl);
    
    /* Enhanced shadows for desktop */
    box-shadow: var(--shadow-2xl);
  }
}
```

### Performance Optimizations

**Lazy Loading Implementation:**
```tsx
// Lazy load secondary components for better performance
const ExportButtons = lazy(() =>
  import('./ExportButtons').then(module => ({ default: module.default }))
);
const RecentMessageButtons = lazy(() =>
  import('./RecentMessageButtons').then(module => ({ default: module.default }))
);
```

**GPU Acceleration:**
```css
.chat-interface-container {
  transform: var(--gpu-acceleration);
  will-change: var(--will-change-auto);
}
```

### Usage Example

```tsx
<div className="chat-interface-container">
  {/* Section 1: Header */}
  <header className="interface-header">
    <h1 className="h1 text-trust">Market Analysis Chat</h1>
  </header>
  
  {/* Section 2: Messages (Scrollable) */}
  <div className="messages-container smooth-scroll">
    {messages.map(message => (
      <ChatMessage_OpenAI key={message.id} {...message} />
    ))}
    <div ref={messagesEndRef} />
  </div>
  
  {/* Section 3: Chat Input */}
  <div className="input-section">
    <ChatInput_OpenAI
      ref={chatInputRef}
      onSendMessage={handleSendMessage}
      value={inputValue}
      onChange={setInputValue}
    />
  </div>
  
  {/* Section 4: Ticker Input */}
  <div className="ticker-section">
    <SharedTickerInput
      ref={tickerInputRef}
      value={sharedTicker}
      onChange={setSharedTicker}
    />
  </div>
  
  {/* Section 5: Analysis Buttons */}
  <div className="buttons-section">
    <Suspense fallback={<div className="loading-shimmer">Loading...</div>}>
      <AnalysisButtons
        ticker={sharedTicker}
        onPromptGenerated={handlePromptGenerated}
        isLoading={isLoading}
      />
    </Suspense>
  </div>
  
  {/* Section 6: Export/Recent */}
  <div className="utilities-section">
    <div className="utilities-grid">
      <Suspense fallback={null}>
        <ExportButtons messages={messages} />
        <RecentMessageButtons onPromptGenerated={handlePromptGenerated} />
      </Suspense>
    </div>
  </div>
  
  {/* Section 7: Debug Panel */}
  <div className="debug-section">
    <DebugPanel latestResponseTime={latestResponseTime} />
  </div>
</div>
```

---

## ChatMessage_OpenAI

### Component Overview

Professional message bubble component with glassmorphic design, responsive sizing, and enhanced typography for financial data display.

### Styling Architecture

**Message Bubble Structure:**
```css
.message-bubble {
  /* Glassmorphic styling */
  background: var(--glass-surface-3);
  backdrop-filter: var(--glass-blur-sm);
  border: 1px solid var(--glass-border-2);
  border-radius: var(--radius-xl);
  
  /* Responsive sizing */
  max-width: 85%; /* Mobile */
  padding: var(--spacing-4);
  margin-bottom: var(--spacing-3);
  
  /* Performance optimizations */
  transform: var(--gpu-acceleration);
  transition: all var(--timing-base) var(--ease-out);
}

@media (min-width: 768px) {
  .message-bubble {
    max-width: 70%; /* Desktop */
    padding: var(--spacing-5);
  }
}
```

### User vs AI Message Differentiation

**User Messages (Right-aligned):**
```css
.message-bubble.user {
  margin-left: auto;
  background: var(--gradient-trust-subtle);
  border-color: var(--accent-trust);
  animation: slideInRight var(--timing-base) var(--ease-out) forwards;
}

.message-bubble.user .message-content {
  font-weight: var(--font-weight-medium);
  color: var(--text-primary);
}
```

**AI Messages (Left-aligned):**
```css
.message-bubble.ai {
  margin-right: auto;
  background: var(--glass-surface-4);
  border-color: var(--glass-border-3);
  animation: slideInLeft var(--timing-base) var(--ease-out) forwards;
}

.message-bubble.ai .message-content {
  font-weight: var(--font-weight-normal);
  color: var(--text-secondary);
  line-height: var(--line-height-relaxed);
}
```

### Enhanced Scrollbars

**Cross-Platform Scrollbar Styling:**
```css
.message-content {
  overflow-x: auto;
  
  /* Desktop: Thin scrollbars */
  scrollbar-width: thin;
  scrollbar-color: var(--border-color) transparent;
}

.message-content::-webkit-scrollbar {
  height: 6px;
}

.message-content::-webkit-scrollbar-thumb {
  background: var(--border-color);
  border-radius: 3px;
}

/* Touch devices: Larger scrollbars */
@media (hover: none) and (pointer: coarse) {
  .message-content::-webkit-scrollbar {
    height: 10px;
  }
}
```

### Hover Interactions

**Professional Micro-Interactions:**
```css
.message-bubble:hover {
  transform: translateY(-2px) var(--gpu-acceleration);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  border-color: var(--accent-trust);
}

.message-bubble.user:hover {
  background: var(--gradient-trust);
  box-shadow: var(--shadow-glow-trust);
}

.message-bubble.ai:hover {
  background: var(--glass-surface-5);
  box-shadow: var(--shadow-lg);
}
```

### Typography Integration

**Financial Data Typography:**
```tsx
<div className="message-bubble ai">
  <div className="message-content">
    <h6 className="chat-section-header">🎯 Key Takeaways</h6>
    
    <p className="text-body">
      <span className="ticker">NVIDIA</span> is trading at{' '}
      <span className="price-medium">$124.36</span> with{' '}
      <span className="percentage percentage-negative">-3.59%</span> change.
    </p>
    
    <div className="financial-metrics">
      <div className="metric-item">
        <span className="text-small text-secondary">Market Cap:</span>
        <span className="currency font-mono">$3.05T</span>
      </div>
      <div className="metric-item">
        <span className="text-small text-secondary">Volume:</span>
        <span className="font-mono volume-high">224.1M</span>
      </div>
    </div>
  </div>
  
  <div className="message-footer">
    <span className="chat-timestamp">2:34 PM</span>
    <MessageCopyButton content={content} />
  </div>
</div>
```

---

## ChatInput_OpenAI

### Component Overview

Advanced multi-line input component with auto-resizing, keyboard shortcuts, and professional fintech styling.

### Core Styling Features

**Auto-Resizing Textarea:**
```css
.chat-input-container {
  position: relative;
  background: var(--glass-surface-3);
  backdrop-filter: var(--glass-blur-sm);
  border: 1px solid var(--glass-border-2);
  border-radius: var(--radius-xl);
  transition: all var(--timing-base) var(--ease-out);
}

.chat-input-textarea {
  width: 100%;
  min-height: 64px;  /* 4 lines default */
  max-height: 200px; /* 12.5 lines max */
  resize: none;
  
  /* Typography */
  font-family: var(--font-body);
  font-size: var(--font-size-body);
  line-height: var(--line-height-normal);
  
  /* Styling */
  background: transparent;
  border: none;
  padding: var(--spacing-4);
  color: var(--text-primary);
  
  /* Auto-resize behavior */
  overflow-y: auto;
  field-sizing: content; /* Native auto-resize */
}
```

### Focus States

**Enhanced Focus Indicators:**
```css
.chat-input-container:focus-within {
  border-color: var(--accent-trust);
  box-shadow: var(--shadow-focus);
  background: var(--glass-surface-4);
  transform: translateY(-1px) var(--gpu-acceleration);
}

.chat-input-textarea:focus {
  outline: none; /* Custom focus handled by container */
}
```

### Responsive Design

**Mobile Optimizations:**
```css
@media (max-width: 767px) {
  .chat-input-textarea {
    font-size: 16px; /* Prevent zoom on iOS */
    min-height: 48px; /* Compact on mobile */
    padding: var(--spacing-3);
  }
  
  /* iOS safe area */
  .chat-input-container {
    margin-bottom: env(safe-area-inset-bottom);
  }
}

/* Android keyboard handling */
@media screen and (-webkit-min-device-pixel-ratio: 0) and (min-resolution: 0.001dpcm) {
  .chat-input-container {
    position: relative;
    bottom: env(keyboard-inset-height, 0px);
  }
}
```

### Send Button Integration

**Floating Send Button:**
```css
.send-button {
  position: absolute;
  bottom: var(--spacing-2);
  right: var(--spacing-2);
  
  /* Button styling */
  background: var(--accent-trust);
  color: var(--text-primary);
  border: none;
  border-radius: var(--radius-full);
  width: 40px;
  height: 40px;
  
  /* Interactions */
  transition: all var(--timing-fast) var(--ease-out);
  cursor: pointer;
}

.send-button:hover:not(:disabled) {
  background: var(--accent-trust-hover);
  transform: scale(1.05) var(--gpu-acceleration);
}

.send-button:disabled {
  background: var(--accent-trust-disabled);
  cursor: not-allowed;
}
```

### Usage Example

```tsx
<div className="chat-input-container">
  <textarea
    ref={textareaRef}
    className="chat-input-textarea"
    value={inputValue}
    onChange={handleInputChange}
    onKeyDown={handleKeyDown}
    placeholder="Ask about stocks, markets, or financial analysis..."
    disabled={isLoading}
    aria-label="Enter your financial question"
  />
  
  <button
    className="send-button"
    onClick={handleSendMessage}
    disabled={isLoading || !inputValue.trim()}
    aria-label="Send message"
  >
    {isLoading ? (
      <div className="animate-spin">⟳</div>
    ) : (
      <span>→</span>
    )}
  </button>
</div>
```

---

## AnalysisButton

### Component Overview

Advanced button component with sophisticated state management, loading indicators, and financial-specific styling patterns.

### Multi-State Design Architecture

**Button State System:**
```css
.analysis-button {
  /* Base styling */
  background: var(--glass-surface-3);
  backdrop-filter: var(--glass-blur-sm);
  border: 1px solid var(--glass-border-2);
  border-radius: var(--radius-lg);
  padding: var(--spacing-3) var(--spacing-4);
  
  /* Typography */
  font-family: var(--font-body);
  font-size: var(--font-size-body);
  font-weight: var(--font-weight-medium);
  color: var(--text-primary);
  
  /* Performance */
  transition: all var(--timing-base) var(--ease-out);
  cursor: pointer;
  position: relative;
  overflow: hidden;
}
```

### Interactive State Variations

**Default State:**
```css
.analysis-button {
  background: var(--glass-surface-3);
  border-color: var(--glass-border-2);
}
```

**Hover State:**
```css
.analysis-button:hover:not(:disabled) {
  background: var(--glass-surface-4);
  border-color: var(--accent-trust);
  transform: translateY(-2px) var(--gpu-acceleration);
  box-shadow: var(--shadow-glow-trust);
}
```

**Loading State:**
```css
.analysis-button.loading {
  background: var(--gradient-trust-subtle);
  border-color: var(--accent-trust);
  cursor: wait;
  
  /* Shimmer effect */
  background-image: linear-gradient(
    90deg,
    transparent,
    rgba(99, 102, 241, 0.2),
    transparent
  );
  background-size: 200% 100%;
  animation: shimmer 2s linear infinite;
}
```

**Success State:**
```css
.analysis-button.success {
  background: var(--gradient-success-subtle);
  border-color: var(--accent-success);
  animation: priceFlash var(--timing-medium) var(--ease-bullish);
}
```

**Error State:**
```css
.analysis-button.error {
  background: var(--gradient-error-subtle);
  border-color: var(--accent-error);
  animation: shake var(--timing-medium) var(--ease-in-out);
}
```

**Disabled State:**
```css
.analysis-button:disabled {
  background: var(--glass-surface-1);
  border-color: var(--glass-border-1);
  color: var(--neutral-color);
  cursor: not-allowed;
  opacity: 0.6;
  transform: none;
}
```

### Template-Specific Styling

**Snapshot Analysis Button:**
```css
.analysis-button.snapshot {
  background: var(--gradient-trust-subtle);
  border-left: 4px solid var(--accent-trust);
}

.analysis-button.snapshot::before {
  content: '📊';
  margin-right: var(--spacing-2);
}
```

**Technical Analysis Button:**
```css
.analysis-button.technical {
  background: var(--gradient-info-subtle);
  border-left: 4px solid var(--accent-info);
}

.analysis-button.technical::before {
  content: '📈';
  margin-right: var(--spacing-2);
}
```

**Support & Resistance Button:**
```css
.analysis-button.support-resistance {
  background: var(--gradient-warning-subtle);
  border-left: 4px solid var(--accent-warning);
}

.analysis-button.support-resistance::before {
  content: '🎯';
  margin-right: var(--spacing-2);
}
```

### Loading Indicator Integration

**Spinner Implementation:**
```tsx
{isLoading && (
  <div className="loading-indicator">
    <div className="spinner animate-spin" />
    <span className="loading-text">Generating...</span>
  </div>
)}
```

**Spinner Styling:**
```css
.spinner {
  width: 16px;
  height: 16px;
  border: 2px solid var(--glass-border-2);
  border-top: 2px solid var(--accent-trust);
  border-radius: var(--radius-full);
  margin-right: var(--spacing-2);
}

.loading-text {
  font-size: var(--font-size-small);
  color: var(--text-secondary);
  font-style: italic;
}
```

### Usage Example

```tsx
<button
  className={`analysis-button ${template.type} ${getButtonState()}`}
  onClick={handleButtonClick}
  disabled={isButtonDisabled}
  data-testid={getTestId(template.type)}
  aria-label={`Generate ${template.title} analysis`}
  onMouseEnter={() => setIsHovered(true)}
  onMouseLeave={() => setIsHovered(false)}
>
  <div className="button-content">
    <span className="button-title">{template.title}</span>
    {template.requiresTicker && (
      <span className="button-ticker">({ticker || 'AAPL'})</span>
    )}
  </div>
  
  {isLoading && (
    <div className="loading-overlay">
      <div className="spinner animate-spin" />
    </div>
  )}
  
  {showSuccess && (
    <div className="success-indicator animate-fade-in">✓</div>
  )}
  
  {hasError && (
    <div className="error-indicator animate-shake">⚠</div>
  )}
</button>
```

---

## SharedTickerInput

### Component Overview

Professional stock ticker input with real-time validation, accessibility features, and enhanced financial-specific styling.

### Core Input Styling

**Input Container:**
```css
.ticker-input-container {
  position: relative;
  background: var(--glass-surface-3);
  backdrop-filter: var(--glass-blur-sm);
  border: 1px solid var(--glass-border-2);
  border-radius: var(--radius-lg);
  transition: all var(--timing-base) var(--ease-out);
}

.ticker-input {
  width: 100%;
  background: transparent;
  border: none;
  padding: var(--spacing-3) var(--spacing-4);
  
  /* Typography optimized for stock symbols */
  font-family: var(--font-mono);
  font-size: var(--font-size-ticker);
  font-weight: var(--font-weight-semibold);
  letter-spacing: var(--letter-spacing-wider);
  text-transform: uppercase;
  color: var(--text-primary);
}
```

### Validation States

**Valid State:**
```css
.ticker-input-container.valid {
  border-color: var(--accent-success);
  background: var(--gradient-success-subtle);
}

.ticker-input-container.valid::after {
  content: '✓';
  position: absolute;
  right: var(--spacing-3);
  top: 50%;
  transform: translateY(-50%);
  color: var(--accent-success);
  font-weight: var(--font-weight-bold);
}
```

**Invalid State:**
```css
.ticker-input-container.invalid {
  border-color: var(--accent-error);
  background: var(--gradient-error-subtle);
  animation: shake var(--timing-medium) var(--ease-in-out);
}

.ticker-input-container.invalid::after {
  content: '⚠';
  position: absolute;
  right: var(--spacing-3);
  top: 50%;
  transform: translateY(-50%);
  color: var(--accent-error);
}
```

**Focus State:**
```css
.ticker-input-container:focus-within {
  border-color: var(--accent-trust);
  background: var(--glass-surface-4);
  box-shadow: var(--shadow-focus);
  transform: translateY(-1px) var(--gpu-acceleration);
}
```

### Label and Error Display

**Floating Label Pattern:**
```css
.ticker-input-label {
  position: absolute;
  left: var(--spacing-4);
  top: 50%;
  transform: translateY(-50%);
  
  /* Typography */
  font-size: var(--font-size-small);
  font-weight: var(--font-weight-medium);
  color: var(--text-secondary);
  
  /* Animation */
  transition: all var(--timing-base) var(--ease-out);
  pointer-events: none;
}

.ticker-input:focus ~ .ticker-input-label,
.ticker-input:not(:placeholder-shown) ~ .ticker-input-label {
  top: -8px;
  font-size: var(--font-size-micro);
  color: var(--accent-trust);
  background: var(--background-primary);
  padding: 0 var(--spacing-1);
}
```

**Error Message Display:**
```css
.ticker-input-error {
  margin-top: var(--spacing-2);
  padding: var(--spacing-2) var(--spacing-3);
  background: var(--gradient-error-subtle);
  border-radius: var(--radius-md);
  
  font-size: var(--font-size-small);
  color: var(--accent-error);
  
  animation: fadeInUp var(--timing-base) var(--ease-out);
}
```

### Auto-Completion Styling

**Dropdown Suggestions:**
```css
.ticker-suggestions {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  z-index: 10;
  
  background: var(--glass-surface-4);
  backdrop-filter: var(--glass-blur-lg);
  border: 1px solid var(--glass-border-3);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-lg);
  
  max-height: 200px;
  overflow-y: auto;
  margin-top: var(--spacing-1);
}

.ticker-suggestion-item {
  padding: var(--spacing-3) var(--spacing-4);
  cursor: pointer;
  transition: all var(--timing-fast) var(--ease-out);
  
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.ticker-suggestion-item:hover {
  background: var(--glass-surface-5);
  color: var(--accent-trust);
}

.ticker-suggestion-symbol {
  font-family: var(--font-mono);
  font-weight: var(--font-weight-bold);
  color: var(--text-primary);
}

.ticker-suggestion-name {
  font-size: var(--font-size-small);
  color: var(--text-secondary);
}
```

### Usage Example

```tsx
<div className="ticker-input-wrapper">
  <div className={`ticker-input-container ${getValidationState()}`}>
    <input
      ref={inputRef}
      type="text"
      className="ticker-input"
      value={currentValue}
      onChange={handleInputChange}
      onBlur={handleBlur}
      onFocus={handleFocus}
      onKeyDown={handleKeyDown}
      placeholder=""
      aria-describedby={error ? `${id}-error` : undefined}
      aria-invalid={hasValidationError}
      maxLength={10}
    />
    <label className="ticker-input-label">{label}</label>
  </div>
  
  {error && (
    <div id={`${id}-error`} className="ticker-input-error" role="alert">
      {error}
    </div>
  )}
  
  {showSuggestions && suggestions.length > 0 && (
    <div className="ticker-suggestions">
      {suggestions.map((suggestion, index) => (
        <div
          key={suggestion.symbol}
          className={`ticker-suggestion-item ${focusedSuggestion === index ? 'focused' : ''}`}
          onClick={() => handleSuggestionClick(suggestion)}
        >
          <span className="ticker-suggestion-symbol">{suggestion.symbol}</span>
          <span className="ticker-suggestion-name">{suggestion.name}</span>
        </div>
      ))}
    </div>
  )}
</div>
```

---

## ExportButtons

### Component Overview

Professional export functionality buttons with glassmorphic styling and enhanced user feedback for data export operations.

### Button Group Container

**Flex Layout with Gap:**
```css
.export-buttons-container {
  display: flex;
  gap: var(--spacing-3);
  flex-wrap: wrap;
  justify-content: space-between;
  
  /* Glassmorphic background */
  background: var(--glass-surface-2);
  backdrop-filter: var(--glass-blur-sm);
  border: 1px solid var(--glass-border-1);
  border-radius: var(--radius-xl);
  padding: var(--spacing-4);
}

@media (max-width: 767px) {
  .export-buttons-container {
    flex-direction: column;
    gap: var(--spacing-2);
  }
}
```

### Individual Export Buttons

**JSON Export Button:**
```css
.export-button-json {
  background: var(--gradient-info-subtle);
  border: 1px solid var(--accent-info);
  color: var(--accent-info);
  
  /* Icon integration */
  display: flex;
  align-items: center;
  gap: var(--spacing-2);
}

.export-button-json::before {
  content: '📄';
  font-size: var(--font-size-h6);
}

.export-button-json:hover:not(:disabled) {
  background: var(--accent-info);
  color: var(--text-primary);
  transform: translateY(-2px) var(--gpu-acceleration);
}
```

**Markdown Export Button:**
```css
.export-button-markdown {
  background: var(--gradient-success-subtle);
  border: 1px solid var(--accent-success);
  color: var(--accent-success);
}

.export-button-markdown::before {
  content: '📝';
  font-size: var(--font-size-h6);
}
```

**Copy to Clipboard Button:**
```css
.export-button-copy {
  background: var(--gradient-trust-subtle);
  border: 1px solid var(--accent-trust);
  color: var(--accent-trust);
}

.export-button-copy::before {
  content: '📋';
  font-size: var(--font-size-h6);
}
```

### Success Feedback States

**Success Indicator Animation:**
```css
.export-button.success {
  animation: priceFlash var(--timing-medium) var(--ease-bullish);
  background: var(--gradient-success);
  border-color: var(--accent-success);
  color: var(--text-primary);
}

.export-button.success::after {
  content: '✓ Exported';
  position: absolute;
  top: -30px;
  left: 50%;
  transform: translateX(-50%);
  
  background: var(--accent-success);
  color: var(--text-primary);
  padding: var(--spacing-1) var(--spacing-3);
  border-radius: var(--radius-md);
  font-size: var(--font-size-small);
  
  animation: fadeInDown var(--timing-base) var(--ease-out);
}
```

### Loading States

**Processing Indicator:**
```css
.export-button.loading {
  cursor: wait;
  position: relative;
}

.export-button.loading::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  
  width: 16px;
  height: 16px;
  border: 2px solid var(--glass-border-2);
  border-top: 2px solid var(--accent-trust);
  border-radius: var(--radius-full);
  
  animation: spin 1s linear infinite;
}
```

### Usage Example

```tsx
<div className="export-buttons-container">
  <button
    className={`export-button export-button-json ${jsonExportState}`}
    onClick={handleJsonExport}
    disabled={messages.length === 0 || isExporting}
    aria-label="Export conversation as JSON"
  >
    <span>Export JSON</span>
    {jsonExportState === 'loading' && (
      <div className="loading-spinner animate-spin" />
    )}
  </button>
  
  <button
    className={`export-button export-button-markdown ${markdownExportState}`}
    onClick={handleMarkdownExport}
    disabled={messages.length === 0 || isExporting}
    aria-label="Export conversation as Markdown"
  >
    <span>Export Markdown</span>
  </button>
  
  <button
    className={`export-button export-button-copy ${copyState}`}
    onClick={handleCopyToClipboard}
    disabled={messages.length === 0 || isExporting}
    aria-label="Copy conversation to clipboard"
  >
    <span>Copy All</span>
    {copyState === 'success' && (
      <div className="success-indicator animate-fade-in">Copied!</div>
    )}
  </button>
</div>
```

---

## DebugPanel

### Component Overview

Developer-focused information panel with performance metrics display, real-time data updates, and collapsible glassmorphic design.

### Panel Container Styling

**Collapsible Panel Design:**
```css
.debug-panel {
  background: var(--glass-surface-1);
  backdrop-filter: var(--glass-blur-xs);
  border: 1px solid var(--glass-border-1);
  border-radius: var(--radius-lg);
  padding: var(--spacing-3);
  
  /* Typography for technical data */
  font-family: var(--font-mono);
  font-size: var(--font-size-small);
  color: var(--text-secondary);
  
  /* Collapsed by default */
  max-height: 40px;
  overflow: hidden;
  transition: max-height var(--timing-medium) var(--ease-out);
}

.debug-panel.expanded {
  max-height: 200px;
}
```

### Header Toggle Design

**Clickable Header with Indicator:**
```css
.debug-panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  
  font-weight: var(--font-weight-medium);
  color: var(--neutral-color);
  transition: color var(--timing-fast) var(--ease-out);
}

.debug-panel-header:hover {
  color: var(--accent-info);
}

.debug-panel-toggle {
  font-size: var(--font-size-h6);
  transition: transform var(--timing-base) var(--ease-out);
}

.debug-panel.expanded .debug-panel-toggle {
  transform: rotate(180deg);
}
```

### Metrics Display Styling

**Performance Metrics Grid:**
```css
.debug-panel-content {
  margin-top: var(--spacing-3);
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: var(--spacing-3);
}

.debug-metric {
  display: flex;
  justify-content: space-between;
  align-items: center;
  
  padding: var(--spacing-2);
  background: var(--glass-surface-2);
  border-radius: var(--radius-md);
  border: 1px solid var(--glass-border-1);
}

.debug-metric-label {
  font-size: var(--font-size-micro);
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: var(--letter-spacing-wide);
}

.debug-metric-value {
  font-weight: var(--font-weight-semibold);
  color: var(--text-primary);
  font-variant-numeric: tabular-nums;
}
```

### Real-Time Data Indicators

**Live Update Animations:**
```css
.debug-metric.updated {
  animation: priceFlash var(--timing-medium) var(--ease-out);
  border-color: var(--accent-info);
}

.debug-metric-value.positive {
  color: var(--accent-success);
}

.debug-metric-value.negative {
  color: var(--accent-error);
}

.debug-metric-value.neutral {
  color: var(--neutral-color);
}
```

### Response Time Display

**Specialized Time Formatting:**
```css
.response-time-display {
  display: flex;
  align-items: center;
  gap: var(--spacing-2);
}

.response-time-value {
  font-family: var(--font-mono);
  font-weight: var(--font-weight-bold);
  font-variant-numeric: tabular-nums;
}

.response-time-value.fast {
  color: var(--accent-success); /* < 1s */
}

.response-time-value.medium {
  color: var(--accent-warning); /* 1-3s */
}

.response-time-value.slow {
  color: var(--accent-error); /* > 3s */
}

.response-time-indicator {
  width: 8px;
  height: 8px;
  border-radius: var(--radius-full);
  background: currentColor;
  animation: heartbeat 2s infinite;
}
```

### Usage Example

```tsx
<div className={`debug-panel ${isExpanded ? 'expanded' : ''}`}>
  <div 
    className="debug-panel-header"
    onClick={() => setIsExpanded(!isExpanded)}
    role="button"
    tabIndex={0}
    aria-expanded={isExpanded}
    aria-label="Toggle debug information"
  >
    <span>Debug Information</span>
    <span className="debug-panel-toggle">▼</span>
  </div>
  
  {isExpanded && (
    <div className="debug-panel-content">
      <div className="debug-metric">
        <span className="debug-metric-label">Last Response Time</span>
        <div className="response-time-display">
          <span className={`response-time-value ${getTimeClass(latestResponseTime)}`}>
            {latestResponseTime ? `${latestResponseTime.toFixed(2)}s` : 'N/A'}
          </span>
          <div className="response-time-indicator" />
        </div>
      </div>
      
      <div className="debug-metric">
        <span className="debug-metric-label">Total Messages</span>
        <span className="debug-metric-value">{messageCount}</span>
      </div>
      
      <div className="debug-metric">
        <span className="debug-metric-label">Session Duration</span>
        <span className="debug-metric-value">{sessionDuration}</span>
      </div>
      
      <div className="debug-metric">
        <span className="debug-metric-label">API Status</span>
        <span className={`debug-metric-value ${apiStatus}`}>
          {apiStatus.toUpperCase()}
        </span>
      </div>
    </div>
  )}
</div>
```

---

## Performance Optimization Guidelines

### GPU Acceleration Best Practices

**Transform-Based Animations:**
```css
/* ✅ Good: GPU-accelerated */
.element {
  transform: translateY(-2px) translateZ(0);
  transition: transform 0.2s ease;
}

/* ❌ Avoid: Layout-triggering */
.element {
  top: -2px;
  transition: top 0.2s ease;
}
```

### Will-Change Management

**Optimized Performance Declaration:**
```css
.interactive-element {
  will-change: transform, opacity;
}

/* Reset after animation completes */
.interactive-element:not(:hover):not(:focus):not(:active) {
  will-change: auto;
}
```

### Lazy Loading Implementation

**Component-Level Code Splitting:**
```tsx
// Lazy load non-critical components
const ExportButtons = lazy(() =>
  import('./ExportButtons').then(module => ({ 
    default: module.default 
  }))
);

// Usage with Suspense
<Suspense fallback={<div className="loading-shimmer">Loading...</div>}>
  <ExportButtons messages={messages} />
</Suspense>
```

---

## Troubleshooting Guide

### Common Styling Issues

**1. Glassmorphic Effects Not Showing**
```css
/* Ensure backdrop-filter support */
@supports (backdrop-filter: blur(8px)) {
  .glass-element {
    backdrop-filter: var(--glass-blur-md);
  }
}

@supports not (backdrop-filter: blur(8px)) {
  .glass-element {
    background: var(--background-secondary);
  }
}
```

**2. Animation Performance Issues**
```css
/* Check GPU acceleration */
.animated-element {
  transform: translateZ(0); /* Force GPU layer */
  will-change: transform;   /* Optimize for transforms */
}
```

**3. Focus States Not Visible**
```css
/* Ensure focus-visible polyfill */
.interactive-element:focus-visible {
  outline: 2px solid var(--focus-ring);
  outline-offset: 2px;
}
```

**4. Mobile Scaling Issues**
```css
/* Prevent zoom on input focus */
input, textarea, select {
  font-size: 16px !important;
}

/* Handle safe areas */
.container {
  padding-bottom: env(safe-area-inset-bottom);
}
```

**5. Dark Mode Contrast Problems**
```css
/* Check color contrast ratios */
@media (prefers-contrast: high) {
  .text-element {
    color: #ffffff;
    background: #000000;
  }
}
```

---

## Development Best Practices

### Component Architecture

1. **Single Responsibility**: Each component handles one specific UI concern
2. **Composition Over Inheritance**: Use component composition patterns
3. **Performance First**: Lazy load non-critical components
4. **Accessibility Built-In**: Include ARIA labels and semantic HTML
5. **Responsive by Default**: Mobile-first responsive design

### Styling Patterns

1. **CSS Custom Properties**: Use design system variables exclusively
2. **BEM Methodology**: Follow Block-Element-Modifier naming
3. **Performance-Optimized**: Prefer transforms over layout properties
4. **Progressive Enhancement**: Layer glassmorphic effects with fallbacks
5. **Semantic Classes**: Use meaningful, context-aware class names

### Testing Considerations

1. **Visual Regression**: Test glassmorphic effects across browsers
2. **Accessibility**: Verify keyboard navigation and screen readers
3. **Performance**: Monitor animation frame rates and memory usage
4. **Responsive**: Test across device sizes and orientations
5. **Cross-Browser**: Validate backdrop-filter support and fallbacks

---

This comprehensive component styling guide provides the foundation for maintaining and extending the fintech glassmorphic design system with professional quality and optimal performance.