/// <reference types="@welldone-software/why-did-you-render" />
import React from 'react';

// eslint-disable-next-line @typescript-eslint/no-unsafe-member-access
if (process.env.NODE_ENV === 'development') {
  void import('@welldone-software/why-did-you-render').then((whyDidYouRenderModule) => {
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
    notifier: ({ Component, displayName, hookName, prevProps, prevState, prevHookResult, nextProps, nextState, nextHookResult, reason, _options }) => {
      // Custom notification for excessive re-renders
      // eslint-disable-next-line no-console
      console.group(`🔄 Why Did You Render: ${displayName || hookName || Component?.name || 'Unknown'}`);
      // eslint-disable-next-line no-console
      console.log('Reason:', reason);
      // eslint-disable-next-line no-console
      console.log('Previous:', { props: prevProps as unknown, state: prevState as unknown, hookResult: prevHookResult as unknown });
      // eslint-disable-next-line no-console
      console.log('Next:', { props: nextProps as unknown, state: nextState as unknown, hookResult: nextHookResult as unknown });
      // eslint-disable-next-line no-console
      console.groupEnd();
    }
    });
  });
}