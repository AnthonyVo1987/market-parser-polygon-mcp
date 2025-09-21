// React Core - ALL REQUIRED HOOKS AND TYPES

// React Event Types - REQUIRED FOR EVENT HANDLERS
import type {
  ChangeEvent,
  FormEvent,
  KeyboardEvent
} from 'react';

// TypeScript Types - COMPLETE INTERFACE DEFINITIONS
export interface Message {
  id: string;
  content: string;
  sender: 'user' | 'ai';
  timestamp: Date;
  metadata?: {
    processingTime?: number;
    isError?: boolean;
  };
}

export interface AnalysisButtonsProps {
  onSnapshot: () => void;
  onSupportResistance: () => void;
  onTechnicalAnalysis: () => void;
  disabled?: boolean;
}

export interface ChatInputProps {
  onSendMessage: (message: string) => void;
  disabled?: boolean;
  placeholder?: string;
}

export interface TickerInputProps {
  value: string;
  onChange: (value: string) => void;
  onAnalyze: () => void;
  disabled?: boolean;
  required?: boolean;
}

// Additional Required Types for Complete Implementation
export interface AnalysisButtonsProps {
  onSnapshot: () => void;
  onSupportResistance: () => void;
  onTechnicalAnalysis: () => void;
  disabled?: boolean;
}

export interface DebugPanelProps {
  responseTime?: number;
  messageCount?: number;
  lastUpdate?: Date;
  isConnected?: boolean;
}

// Event Handler Types
export type FormEventHandler = (e: FormEvent) => void;
export type KeyboardEventHandler = (e: KeyboardEvent) => void;
export type ChangeEventHandler = (e: ChangeEvent<HTMLInputElement>) => void;