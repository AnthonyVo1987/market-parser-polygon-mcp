import { inputStyles } from './components/ChatInput_OpenAI';
import ChatInterface_OpenAI, {
  interfaceStyles,
} from './components/ChatInterface_OpenAI';
import { messageStyles } from './components/ChatMessage_OpenAI';
import ErrorBoundary, { errorBoundaryStyles } from './components/ErrorBoundary';

export default function App() {
  const handleError = (error: Error, errorInfo: { componentStack: string }) => {
    // In a real app, you might send this to an error reporting service
    console.error('App Error Boundary:', error, errorInfo);
  };

  return (
    <ErrorBoundary onError={handleError}>
      <style>{interfaceStyles}</style>
      <style>{messageStyles}</style>
      <style>{inputStyles}</style>
      <style>{errorBoundaryStyles}</style>
      <ChatInterface_OpenAI />
    </ErrorBoundary>
  );
}
