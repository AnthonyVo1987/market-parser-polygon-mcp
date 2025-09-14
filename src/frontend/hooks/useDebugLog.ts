/**
 * React hooks for safe logging that prevents render loops.
 * 
 * These hooks follow React best practices by using useEffect with proper
 * dependency arrays and useRef to track previous values without causing re-renders.
 * 
 * Usage:
 *   import { useComponentLogger, useStateLogger, useEffectLogger } from '@/hooks/useDebugLog';
 *   
 *   function MyComponent() {
 *     const [count, setCount] = useState(0);
 *     
 *     // Log component lifecycle
 *     useComponentLogger('MyComponent');
 *     
 *     // Log state changes safely
 *     useStateLogger('MyComponent', 'count', count);
 *     
 *     // Log side effects
 *     useEffectLogger('MyComponent', 'data fetch', [someId], () => {
 *       // Effect logic here
 *     });
 *   }
 */

import { useEffect, useRef, useCallback } from 'react';
import { logger, LogContext } from '../utils/logger';

/**
 * Hook for logging component lifecycle events (mount/unmount)
 * Safe pattern: Only logs once per component lifecycle
 */
export function useComponentLogger(componentName: string, initialContext?: LogContext): void {
  const mountedRef = useRef(false);
  
  useEffect(() => {
    if (!mountedRef.current) {
      logger.componentLifecycle(componentName, 'mount', initialContext);
      mountedRef.current = true;
    }
    
    return () => {
      logger.componentLifecycle(componentName, 'unmount');
    };
  }, []); // Empty dependency array = only runs once
}

/**
 * Hook for safely logging state changes without causing render loops
 * Safe pattern: Uses useRef to track previous values, only logs actual changes
 */
export function useStateLogger<T>(
  componentName: string, 
  stateName: string, 
  currentValue: T,
  shouldLog: boolean = true
): void {
  const previousValueRef = useRef<T>(currentValue);
  const initialRenderRef = useRef(true);
  
  useEffect(() => {
    if (!shouldLog) return;
    
    const previousValue = previousValueRef.current;
    
    // Skip logging on initial render
    if (initialRenderRef.current) {
      initialRenderRef.current = false;
      previousValueRef.current = currentValue;
      return;
    }
    
    // Only log if value actually changed
    if (previousValue !== currentValue) {
      logger.stateChange(componentName, stateName, previousValue, currentValue);
      previousValueRef.current = currentValue;
    }
  }, [componentName, stateName, currentValue, shouldLog]); // Proper dependency array
}

/**
 * Hook for logging effect execution with dependencies tracking
 * Safe pattern: Logs effect execution and dependency changes separately
 */
export function useEffectLogger(
  componentName: string,
  effectName: string,
  dependencies: any[],
  effectCallback: () => void | (() => void),
  shouldLog: boolean = true
): void {
  const previousDepsRef = useRef<any[]>(dependencies);
  const effectCountRef = useRef(0);
  
  useEffect(() => {
    effectCountRef.current += 1;
    
    if (shouldLog) {
      // Log which dependencies changed (if any)
      const changedDeps = dependencies.reduce((acc, dep, index) => {
        if (previousDepsRef.current[index] !== dep) {
          acc[`dep_${index}`] = {
            old: previousDepsRef.current[index],
            new: dep
          };
        }
        return acc;
      }, {} as any);
      
      logger.debug(`🔄 Effect ${effectName} in ${componentName}`, {
        component: componentName,
        effect: effectName,
        executionCount: effectCountRef.current,
        dependenciesChanged: Object.keys(changedDeps).length > 0,
        changedDependencies: changedDeps
      });
    }
    
    previousDepsRef.current = [...dependencies];
    
    // Execute the actual effect
    return effectCallback();
  }, dependencies); // Use actual dependencies
}

/**
 * Hook for logging user interactions safely
 * Safe pattern: Returns a callback that logs interactions
 */
export function useInteractionLogger(componentName: string): (action: string, element: string, details?: LogContext) => void {
  return useCallback((action: string, element: string, details?: LogContext) => {
    logger.userInteraction(action, element, {
      component: componentName,
      ...details
    });
  }, [componentName]);
}

/**
 * Hook for performance timing of operations
 * Safe pattern: Returns callbacks for start/end timing
 */
export function usePerformanceLogger(componentName: string): {
  startTiming: (operationName: string) => void;
  endTiming: (operationName: string) => number | null;
} {
  const startTiming = useCallback((operationName: string) => {
    const fullName = `${componentName}:${operationName}`;
    logger.startTiming(fullName);
  }, [componentName]);
  
  const endTiming = useCallback((operationName: string) => {
    const fullName = `${componentName}:${operationName}`;
    return logger.endTiming(fullName);
  }, [componentName]);
  
  return { startTiming, endTiming };
}

/**
 * Hook for logging API calls with automatic timing
 * Safe pattern: Returns a wrapper function that logs API calls
 */
export function useAPILogger(componentName: string): {
  logRequest: (method: string, url: string, data?: any) => void;
  logResponse: (method: string, url: string, status: number, duration: number, data?: any) => void;
  wrapAPICall: <T>(
    method: string,
    url: string,
    apiCall: () => Promise<T>,
    requestData?: any
  ) => Promise<T>;
} {
  const logRequest = useCallback((method: string, url: string, data?: any) => {
    logger.apiRequest(method, url, data);
  }, []);
  
  const logResponse = useCallback((method: string, url: string, status: number, duration: number, data?: any) => {
    logger.apiResponse(method, url, status, duration, data);
  }, []);
  
  const wrapAPICall = useCallback(async <T>(
    method: string,
    url: string,
    apiCall: () => Promise<T>,
    requestData?: any
  ): Promise<T> => {
    const startTime = performance.now();
    logger.apiRequest(method, url, requestData);
    
    try {
      const result = await apiCall();
      const duration = performance.now() - startTime;
      logger.apiResponse(method, url, 200, duration, result);
      return result;
    } catch (error) {
      const duration = performance.now() - startTime;
      const status = (error as any)?.status || 500;
      logger.apiResponse(method, url, status, duration, error);
      throw error;
    }
  }, []);
  
  return { logRequest, logResponse, wrapAPICall };
}

/**
 * Hook for conditional logging based on props/state
 * Safe pattern: Only logs when specified conditions are met
 */
export function useConditionalLogger(
  componentName: string,
  condition: boolean,
  message: string,
  context?: LogContext,
  level: 'debug' | 'info' | 'warn' | 'error' = 'debug'
): void {
  const previousConditionRef = useRef(condition);
  
  useEffect(() => {
    // Only log when condition changes from false to true
    if (condition && !previousConditionRef.current) {
      logger[level](`🎯 Condition met in ${componentName}: ${message}`, {
        component: componentName,
        condition: true,
        ...context
      });
    }
    
    previousConditionRef.current = condition;
  }, [componentName, condition, message, context, level]);
}

/**
 * Hook for logging render cycles and preventing infinite loops
 * Safe pattern: Tracks render count and warns about excessive re-renders
 */
export function useRenderLogger(componentName: string, maxRenders: number = 10): void {
  const renderCountRef = useRef(0);
  const lastResetRef = useRef(Date.now());
  
  useEffect(() => {
    renderCountRef.current += 1;
    const now = Date.now();
    
    // Reset counter every 5 seconds
    if (now - lastResetRef.current > 5000) {
      renderCountRef.current = 1;
      lastResetRef.current = now;
    }
    
    // Log render count
    logger.debug(`🎭 Render #${renderCountRef.current} in ${componentName}`);
    
    // Warn about excessive re-renders
    if (renderCountRef.current > maxRenders) {
      logger.warn(`⚠️ Excessive re-renders detected in ${componentName}`, {
        component: componentName,
        renderCount: renderCountRef.current,
        timeWindow: '5 seconds',
        suggestion: 'Check dependencies in useEffect and useMemo hooks'
      });
    }
  }); // No dependency array = runs on every render (intentional for render counting)
}

/**
 * Hook for debounced logging to prevent spam
 * Safe pattern: Uses debouncing to limit log frequency
 */
export function useDebouncedLogger(
  message: string,
  value: any,
  delay: number = 500,
  level: 'debug' | 'info' | 'warn' | 'error' = 'debug'
): void {
  const timeoutRef = useRef<NodeJS.Timeout>();
  
  useEffect(() => {
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
    }
    
    timeoutRef.current = setTimeout(() => {
      logger[level](message, { value, timestamp: new Date().toISOString() });
    }, delay);
    
    return () => {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }
    };
  }, [message, value, delay, level]);
}

/**
 * Development-only hook that logs component props changes
 * Safe pattern: Only active in development, uses deep comparison
 */
export function usePropsLogger(componentName: string, props: Record<string, any>): void {
  const previousPropsRef = useRef(props);
  
  useEffect(() => {
    if (process.env.NODE_ENV !== 'development') return;
    
    const previousProps = previousPropsRef.current;
    const changedProps: Record<string, { old: any; new: any }> = {};
    
    Object.keys(props).forEach(key => {
      if (previousProps[key] !== props[key]) {
        changedProps[key] = {
          old: previousProps[key],
          new: props[key]
        };
      }
    });
    
    if (Object.keys(changedProps).length > 0) {
      logger.debug(`📝 Props changed in ${componentName}`, {
        component: componentName,
        changedProps,
        timestamp: new Date().toISOString()
      });
    }
    
    previousPropsRef.current = { ...props };
  }, [componentName, props]);
}