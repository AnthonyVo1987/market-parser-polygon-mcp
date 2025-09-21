import { FC, useCallback, useEffect, useState } from 'react';
import { Message } from '../types';
import AnalysisButtons from './AnalysisButtons';
import ChatInput_OpenAI from './ChatInput_OpenAI';
import ChatMessage_OpenAI from './ChatMessage_OpenAI';
import DebugPanel from './DebugPanel';
import SharedTickerInput from './SharedTickerInput';

// Mock functions for parts of the old implementation that are not in the new plan.
// This is to ensure the component is self-contained and runnable as per the plan.
const sendChatMessage = async (message: string, _model: string) => {
  await new Promise(resolve => setTimeout(resolve, 1500));
  return {
    response: `This is a mock AI response to your message: "${message}"`,
    metadata: {
      response_time: '1.50s'
    }
  };
};

const ChatInterface_OpenAI: FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [messageSentStatus, setMessageSentStatus] = useState(false);
  const [tickerValue, setTickerValue] = useState('AAPL');
  const [lastResponseTime, setLastResponseTime] = useState(0);
  const [currentModel] = useState('mock-model');

  // Add screen reader announcements for message sent status
  useEffect(() => {
    if (messageSentStatus) {
      // Announce to screen readers
      const announcement = document.createElement('div');
      announcement.setAttribute('aria-live', 'assertive');
      announcement.setAttribute('aria-atomic', 'true');
      announcement.className = 'sr-only';
      announcement.textContent = 'Message sent. Please wait for AI response.';
      document.body.appendChild(announcement);

      return () => {
        if (document.body.contains(announcement)) {
          document.body.removeChild(announcement);
        }
      };
    }
  }, [messageSentStatus]);

  const handleSendMessage = useCallback(async (messageContent: string) => {
    const messageId = Date.now().toString();
    const userMessage: Message = {
      id: messageId,
      content: messageContent,
      sender: 'user',
      timestamp: new Date(),
    };

    setMessageSentStatus(true);
    setMessages(prev => [...prev, userMessage]);

    try {
      const apiResponse = await sendChatMessage(messageContent, currentModel);

      const responseTime = apiResponse.metadata?.response_time
        ? parseFloat(apiResponse.metadata.response_time.replace('s', ''))
        : 0;

      const aiMessage: Message = {
        id: Date.now().toString() + Math.random().toString(36).substr(2, 9),
        content: apiResponse.response,
        sender: 'ai',
        timestamp: new Date(),
        metadata: { processingTime: responseTime },
      };

      setMessages(prev => [...prev, aiMessage]);
      setLastResponseTime(responseTime);
    } catch (err: unknown) {
      const errorMessage =
        err instanceof Error ? err.message : 'Failed to send message';

      const aiMessage: Message = {
        id: Date.now().toString() + Math.random().toString(36).substr(2, 9),
        content: `Error: ${errorMessage}`,
        sender: 'ai',
        timestamp: new Date(),
        metadata: { isError: true },
      };

      setMessages(prev => [...prev, aiMessage]);
    } finally {
      setMessageSentStatus(false);
    }
  }, [currentModel]);

  const handleSnapshot = useCallback(() => {
    handleSendMessage(`Take a snapshot of ${tickerValue}`);
  }, [handleSendMessage, tickerValue]);

  const handleSupportResistance = useCallback(() => {
    handleSendMessage(`Analyze support and resistance for ${tickerValue}`);
  }, [handleSendMessage, tickerValue]);

  const handleTechnicalAnalysis = useCallback(() => {
    handleSendMessage(`Perform technical analysis for ${tickerValue}`);
  }, [handleSendMessage, tickerValue]);

  const handleTickerAnalysis = useCallback(() => {
    handleSendMessage(`Analyze ticker ${tickerValue}`);
  }, [handleSendMessage, tickerValue]);

  const handleExport = useCallback(() => {
    // In a real app, this would trigger a download or copy to clipboard.
    console.log("Exporting chat:", JSON.stringify(messages, null, 2));
    alert("Chat exported! Check the console.");
  }, [messages]);

  return (
    <div className="chat-interface-container">
      <header className="chat-header">
        <h1>Market Parser - AI Financial Analysis</h1>
      </header>

      <div className="messages-container">
        {messages.map((message) => (
          <ChatMessage_OpenAI key={message.id} message={message} />
        ))}
      </div>

      <ChatInput_OpenAI
        onSendMessage={handleSendMessage}
        disabled={messageSentStatus}
      />

      <SharedTickerInput
        value={tickerValue}
        onChange={setTickerValue}
        onAnalyze={handleTickerAnalysis}
        disabled={messageSentStatus}
      />

      <AnalysisButtons
        onSnapshot={handleSnapshot}
        onSupportResistance={handleSupportResistance}
        onTechnicalAnalysis={handleTechnicalAnalysis}
        disabled={messageSentStatus}
      />

      <div className="export-buttons">
        <button onClick={handleExport}>Export Chat</button>
      </div>

      <DebugPanel
        responseTime={lastResponseTime}
        messageCount={messages.length}
        lastUpdate={new Date()}
        isConnected={true}
      />

      {messageSentStatus && (
        <div className="message-sent-overlay" role="status" aria-live="assertive">
          <div className="message-sent-content">
            <h2 className="message-sent-title">MESSAGE SENT</h2>
            <p className="message-sent-subtitle">PLEASE WAIT FOR AI RESPONSE</p>
            <div className="message-sent-indicator" aria-hidden="true">
              <div className="status-dot"></div>
              <div className="status-dot"></div>
              <div className="status-dot"></div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ChatInterface_OpenAI;
