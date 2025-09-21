import { FC } from 'react';
import { Message } from '../types';

interface ChatMessageProps {
  message: Message;
}

const ChatMessage_OpenAI: FC<ChatMessageProps> = ({ message }) => {
  return (
    <div className={`chat-message ${message.sender}`} data-testid={`chat-message-${message.sender}`}>
      <div className="message-content">
        {message.content}
      </div>
      <div className="message-timestamp">
        {message.timestamp.toLocaleTimeString()}
      </div>
      {message.metadata?.processingTime && (
        <div className="message-processing-time">
          Response time: {message.metadata.processingTime.toFixed(2)}s
        </div>
      )}
    </div>
  );
};

export default ChatMessage_OpenAI;