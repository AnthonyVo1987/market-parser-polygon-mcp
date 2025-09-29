/// <reference types="@welldone-software/why-did-you-render" />
import React from 'react';

// React Scan integration for performance monitoring
import { scan } from 'react-scan/all-environments';

if (typeof window !== 'undefined' && import.meta.env?.MODE === 'development') {
  // Configure React Scan for performance monitoring
  scan({
    enabled: import.meta.env?.MODE === 'development',
    log: false,
    showToolbar: true,
    animationSpeed: 'fast',
    trackUnnecessaryRenders: true,
    onRender: (fiber, renders) => {
      try {
        if (renders.length > 1) {
          // eslint-disable-next-line no-console
          console.warn(
            `🔄 Unnecessary render detected: ${(fiber.type as { name?: string })?.name || 'Unknown'}`,
            {
              component: (fiber.type as { name?: string })?.name || 'Unknown',
              renderCount: renders.length,
              props: fiber.memoizedProps,
              state: fiber.memoizedState,
            }
          );
        }
      } catch (error) {
        // eslint-disable-next-line no-console
        console.error('React Scan onRender error:', error);
      }
    },
  });

  void import('@welldone-software/why-did-you-render').then(
    whyDidYouRenderModule => {
      const whyDidYouRender = whyDidYouRenderModule.default;
      whyDidYouRender(React, {
        trackAllPureComponents: true,
        trackHooks: true,
        logOnDifferentValues: true,
        collapseGroups: false,
        include: [/^ChatInterface_OpenAI/],
        titleColor: 'red',
        diffNameColor: 'orange',
        diffPathColor: 'gray',
        notifier: (options: any) => {
          const {
            Component,
            displayName,
            hookName,
            prevProps: _prevProps,
            prevState: _prevState,
            prevHookResult: _prevHookResult,
            nextProps: _nextProps,
            nextState: _nextState,
            nextHookResult: _nextHookResult,
            reason: _reason,
          } = options as {
            Component?: React.ComponentType<unknown>;
            displayName?: string;
            hookName?: string;
            prevProps: unknown;
            prevState: unknown;
            prevHookResult: unknown;
            nextProps: unknown;
            nextState: unknown;
            nextHookResult: unknown;
            reason: unknown;
          };
          // Custom notification for excessive re-renders using minimal logger
          const componentName =
            displayName || hookName || Component?.name || 'Unknown';
          // Use the componentName variable to avoid unused variable warning
          if (componentName) {
            // Component name is available for logging
          }
        },
      });
    }
  );
}
