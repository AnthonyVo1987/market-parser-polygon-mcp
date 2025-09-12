import { inputStyles } from './components/ChatInput_OpenAI';
import ChatInterface_OpenAI, {
  interfaceStyles,
} from './components/ChatInterface_OpenAI';
import { messageStyles } from './components/ChatMessage_OpenAI';
import ErrorBoundary, { errorBoundaryStyles } from './components/ErrorBoundary';

export default function App() {
  const handleError = (
    _error: Error,
    _errorInfo: { componentStack: string }
  ) => {
    // In a real app, you might send this to an error reporting service
    // Error handling delegated to ErrorBoundary component
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
