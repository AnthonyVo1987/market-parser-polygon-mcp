import ChatInterface_OpenAI from './components/ChatInterface_OpenAI';
import ErrorBoundary from './components/ErrorBoundary';

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
      <ChatInterface_OpenAI />
    </ErrorBoundary>
  );
}
