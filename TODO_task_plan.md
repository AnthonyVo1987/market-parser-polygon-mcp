# 🔴 CRITICAL: MANDATORY TOOL USAGE Implementation Plan - GUI Component Updates

## **PHASE 1: AI MODEL SELECTOR IMPLEMENTATION**

### **Task 1.1: Create useAIModel Hook**

- **File**: `src/frontend/hooks/useAIModel.ts`
- **Purpose**: State management for AI model selection
- **Features**:
  - Fetch available models from API
  - Manage current model selection
  - Handle loading and error states
  - Provide model selection function
- **Dependencies**: `src/frontend/services/api_OpenAI.ts`, `src/frontend/types/ai_models.ts`

### **Task 1.2: Create AIModelSelector Component**

- **File**: `src/frontend/components/AIModelSelector.tsx`
- **Purpose**: Dropdown component for model selection
- **Features**:
  - Dropdown with available models
  - Current model display
  - Loading and error states
  - Accessibility support
- **Props**: `models`, `currentModel`, `onModelChange`, `loading`, `error`
- **Styling**: Match existing design system

### **Task 1.3: Update ChatInput Component**

- **File**: `src/frontend/components/ChatInput_OpenAI.tsx`
- **Purpose**: Integrate AI Model Selector next to send button
- **Changes**:
  - Add AIModelSelector component
  - Update layout to accommodate selector
  - Pass model selection to parent
  - Maintain responsive design
- **Layout**: Horizontal layout with textarea, selector, and send button

### **Task 1.4: Update ChatInterface Component**

- **File**: `src/frontend/components/ChatInterface_OpenAI.tsx`
- **Purpose**: Integrate useAIModel hook and pass model to API
- **Changes**:
  - Uncomment and implement useAIModel hook
  - Pass selected model to sendChatMessage
  - Handle model selection state
  - Update error handling for model selection

## **PHASE 2: PANEL CONSOLIDATION**

### **Task 2.1: Create Consolidated Debug Panel**

- **File**: `src/frontend/components/ConsolidatedDebugPanel.tsx`
- **Purpose**: Combine Debug and Status information into single panel
- **Features**:
  - Debug information (connection status, version, last update)
  - Status information (message count, processing status)
  - Performance metrics (FCP, LCP, CLS)
  - Organized sections within single panel
- **Props**: `messageCount`, `isLoading`, `lastUpdate`, `isConnected`, `performanceMetrics`

### **Task 2.2: Update ChatInterface Layout**

- **File**: `src/frontend/components/ChatInterface_OpenAI.tsx`
- **Purpose**: Replace separate panels with consolidated panel
- **Changes**:
  - Remove separate Debug Information panel
  - Remove separate Status Information panel
  - Remove separate Performance Metrics panel
  - Add single Consolidated Debug Panel
  - Update panel titles and organization

### **Task 2.3: Remove Session Components**

- **Files**: Search and remove any Session-related components
- **Purpose**: Clean up unused Session functionality
- **Changes**:
  - Remove Session references from DebugPanel
  - Remove Session-related props and state
  - Clean up unused imports and types

## **PHASE 3: STYLING AND RESPONSIVENESS**

### **Task 3.1: Update CSS for New Layout**

- **File**: `src/frontend/components/ChatInterface_OpenAI.tsx` (styles section)
- **Purpose**: Update styles for consolidated panels and model selector
- **Changes**:
  - Update bottom control panels layout
  - Add styles for AI Model Selector
  - Ensure responsive design for mobile
  - Update panel spacing and organization

### **Task 3.2: Create AIModelSelector Styles**

- **File**: `src/frontend/components/AIModelSelector.tsx` (inline styles)
- **Purpose**: Style the model selector dropdown
- **Features**:
  - Match existing design system
  - Responsive design
  - Accessibility support
  - Loading and error states

## **PHASE 4: TESTING AND VALIDATION**

### **Task 4.1: Test with GPT-5 Nano Model**

- **Command**: `test_7_prompts_comprehensive.sh`
- **Purpose**: Validate functionality with default model
- **Validation**:
  - All 7 tests pass
  - Model selector shows correct model
  - API calls use selected model
  - UI layout is correct

### **Task 4.2: Test with GPT-5 Mini Model**

- **Command**: `test_7_prompts_comprehensive.sh` (after model selection)
- **Purpose**: Validate model switching functionality
- **Validation**:
  - Model selector allows switching
  - API calls use new model
  - All functionality works with Mini model
  - Performance is acceptable

### **Task 4.3: Test Panel Consolidation**

- **Purpose**: Validate consolidated debug panel
- **Validation**:
  - Single panel shows all information
  - No duplicate information
  - Panel is collapsible and functional
  - Mobile responsiveness works

## **PHASE 5: CLEANUP AND OPTIMIZATION**

### **Task 5.1: Remove Unused Code**

- **Files**: Various component files
- **Purpose**: Clean up removed functionality
- **Changes**:
  - Remove unused imports
  - Remove unused props and state
  - Remove unused CSS classes
  - Clean up type definitions

### **Task 5.2: Update Type Definitions**

- **File**: `src/frontend/types/index.ts` (if exists)
- **Purpose**: Update types for new components
- **Changes**:
  - Add AIModelSelector props types
  - Update ConsolidatedDebugPanel props
  - Remove unused Status/Session types

### **Task 5.3: Documentation Updates**

- **Files**: Component files and README
- **Purpose**: Update documentation for new features
- **Changes**:
  - Add JSDoc comments for new components
  - Update component descriptions
  - Document new props and usage

## **PHASE 6: FINAL VALIDATION**

### **Task 6.1: Comprehensive Testing**

- **Command**: `test_7_prompts_comprehensive.sh`
- **Purpose**: Final validation of all changes
- **Validation**:
  - All 7 tests pass with both models
  - UI is responsive and accessible
  - No console errors or warnings
  - Performance is maintained

### **Task 6.2: Code Quality Check**

- **Command**: `npm run lint:all`
- **Purpose**: Ensure code quality standards
- **Validation**:
  - No linting errors
  - TypeScript compilation successful
  - Code follows project conventions

## **SUCCESS CRITERIA**

✅ **AI Model Selector**:

- Dropdown appears next to send button
- Allows switching between GPT-5 Nano and Mini
- API calls use selected model
- Loading and error states handled

✅ **Panel Consolidation**:

- Single consolidated debug panel
- Contains all debug, status, and performance info
- Status Information panel removed
- Session components removed

✅ **Functionality**:

- All 7 comprehensive tests pass
- Both models work correctly
- UI is responsive and accessible
- No regressions in existing features

✅ **Code Quality**:

- No linting errors
- Clean, maintainable code
- Proper TypeScript types
- Good component organization

## **IMPLEMENTATION NOTES**

- **Tool Usage**: Use ALL mandatory toolkit tools throughout implementation
- **Testing**: Test after each major change
- **Incremental**: Implement changes incrementally and test frequently
- **Documentation**: Update documentation as changes are made
- **Accessibility**: Ensure all new components are accessible
- **Responsiveness**: Test on mobile and desktop viewports
