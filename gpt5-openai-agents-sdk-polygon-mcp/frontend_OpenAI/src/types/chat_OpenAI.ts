export interface Message {
  id: string;
  content: string;
  sender: 'user' | 'ai';
  timestamp: Date;
}

export interface ChatResponse {
  response: string;
  success: boolean;
  error?: string;
}

export interface ApiError {
  error: string;
}
