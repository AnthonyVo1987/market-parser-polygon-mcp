/// <reference types="@welldone-software/why-did-you-render" />
import React from 'react';

if (process.env.NODE_ENV === 'development') {
  import('@welldone-software/why-did-you-render').then((whyDidYouRenderModule) => {
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
    notifier: ({ Component, displayName, hookName, prevProps, prevState, prevHookResult, nextProps, nextState, nextHookResult, reason, options }) => {
      // Custom notification for excessive re-renders
      console.group(`🔄 Why Did You Render: ${displayName || hookName || Component?.name || 'Unknown'}`);
      console.log('Reason:', reason);
      console.log('Previous:', { props: prevProps, state: prevState, hookResult: prevHookResult });
      console.log('Next:', { props: nextProps, state: nextState, hookResult: nextHookResult });
      console.groupEnd();
    }
    });
  });
}