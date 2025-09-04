import { Message } from '../types/chat_OpenAI';

// Security configuration constants
const ALLOWED_MIME_TYPES = [
  'text/plain',
  'text/markdown', 
  'application/json',
  'text/csv'
] as const;

const MAX_FILENAME_LENGTH = 100;
const DANGEROUS_FILENAME_CHARS = /[<>:"|?*\\\/.]/g;
const PATH_TRAVERSAL_PATTERNS = /\.\.[\\/]|\.[\\/]|^[\\/]/g;

/**
 * Sanitizes content to prevent XSS attacks while preserving legitimate formatting
 * @param content Raw content that may contain malicious scripts
 * @returns Sanitized content safe for export
 */
const sanitizeContent = (content: string): string => {
  if (typeof content !== 'string') {
    return '';
  }
  
  // Remove potentially dangerous HTML tags and attributes
  let sanitized = content
    // Remove script tags and content
    .replace(/<script[^>]*>.*?<\/script>/gis, '')
    // Remove style tags that could contain malicious CSS
    .replace(/<style[^>]*>.*?<\/style>/gis, '')
    // Remove dangerous HTML tags while preserving content
    .replace(/<(iframe|object|embed|applet|form|input|button|textarea)[^>]*>/gi, '')
    // Remove event handlers (onclick, onload, etc.)
    .replace(/\s*on\w+\s*=\s*["'][^"']*["']/gi, '')
    // Remove javascript: protocol
    .replace(/javascript:/gi, '')
    // Remove data: URLs that could contain scripts
    .replace(/data:\s*text\/html/gi, 'data:text/plain')
    // Clean up excessive whitespace but preserve formatting
    .replace(/\s{3,}/g, '  ');
    
  // Preserve legitimate emojis and markdown formatting
  // This regex allows Unicode emoji ranges and common markdown syntax
  sanitized = sanitized.replace(/[^\w\s\p{Emoji}\p{Emoji_Presentation}\p{Emoji_Modifier}\p{Emoji_Component}\n\r\t.,;:!?()\[\]{}"'`~@#$%^&*+=|\-_/\\<>]/gu, '');
  
  return sanitized.trim();
};

/**
 * Validates MIME type against whitelist to prevent arbitrary file type attacks
 * @param mimeType MIME type to validate
 * @returns true if MIME type is safe and allowed
 */
const validateMimeType = (mimeType: string): boolean => {
  if (typeof mimeType !== 'string') {
    return false;
  }
  
  const normalizedMimeType = mimeType.toLowerCase().trim();
  return ALLOWED_MIME_TYPES.includes(normalizedMimeType as any);
};

/**
 * Enhanced filename sanitization with path traversal protection and length limits
 * @param filename Raw filename that may contain dangerous characters
 * @returns Safe filename with path traversal protection and length limits
 */
const sanitizeFilename = (filename: string): string => {
  if (typeof filename !== 'string' || !filename.trim()) {
    return 'export_file';
  }
  
  let sanitized = filename
    // Remove path traversal attempts
    .replace(PATH_TRAVERSAL_PATTERNS, '')
    // Replace dangerous characters with underscores
    .replace(DANGEROUS_FILENAME_CHARS, '_')
    // Remove control characters
    .replace(/[\x00-\x1f\x7f-\x9f]/g, '')
    // Normalize whitespace
    .replace(/\s+/g, '_')
    // Remove leading/trailing dots and underscores
    .replace(/^[._]+|[._]+$/g, '')
    // Ensure it's not empty after cleaning
    .trim();
    
  // Enforce length limit
  if (sanitized.length > MAX_FILENAME_LENGTH) {
    // Preserve file extension if present
    const lastDotIndex = sanitized.lastIndexOf('.');
    if (lastDotIndex > 0 && lastDotIndex > sanitized.length - 10) {
      const extension = sanitized.substring(lastDotIndex);
      const nameWithoutExt = sanitized.substring(0, lastDotIndex);
      const maxNameLength = MAX_FILENAME_LENGTH - extension.length;
      sanitized = nameWithoutExt.substring(0, maxNameLength) + extension;
    } else {
      sanitized = sanitized.substring(0, MAX_FILENAME_LENGTH);
    }
  }
  
  // Final fallback
  return sanitized || 'export_file';
};

/**
 * Converts chat messages to markdown format with proper structure and timestamps
 * @param messages Array of chat messages to convert
 * @returns Formatted markdown string ready for export
 */
export const convertToMarkdown = (messages: Message[]): string => {
  try {
    const exportDate = new Date().toLocaleString();
    const title = `# Chat Export\n\n**Exported on:** ${exportDate}\n**Messages:** ${messages.length}\n\n---\n\n`;
    
    const formattedMessages = messages.map(message => {
      const sender = message.sender === 'user' ? '👤 User' : '🤖 AI Assistant';
      const timestamp = message.timestamp.toLocaleString();
      
      // Apply content sanitization to prevent XSS while preserving formatting
      const content = sanitizeContent(message.content.trim());
      
      return `## ${sender} - ${timestamp}\n\n${content}\n\n---\n`;
    }).join('\n');
    
    return title + formattedMessages;
  } catch (error) {
    throw new Error(`Failed to convert messages to markdown: ${error instanceof Error ? error.message : 'Unknown error'}`);
  }
};

/**
 * Converts chat messages to JSON format with export metadata
 * @param messages Array of chat messages to serialize
 * @returns Pretty-formatted JSON string with metadata
 */
export const convertToJSON = (messages: Message[]): string => {
  try {
    const exportData = {
      exportMetadata: {
        exportDate: new Date().toISOString(),
        title: "Chat Export",
        messageCount: messages.length,
        version: "1.0"
      },
      messages: messages.map(msg => ({
        id: msg.id,
        content: sanitizeContent(msg.content), // Apply content sanitization
        sender: msg.sender,
        timestamp: msg.timestamp.toISOString()
      }))
    };
    
    return JSON.stringify(exportData, null, 2);
  } catch (error) {
    throw new Error(`Failed to convert messages to JSON: ${error instanceof Error ? error.message : 'Unknown error'}`);
  }
};

/**
 * Copies text to clipboard using modern Clipboard API with fallback
 * @param text Text content to copy to clipboard
 * @returns Promise that resolves when copy operation completes
 */
export const copyToClipboard = async (text: string): Promise<void> => {
  try {
    // Use modern Clipboard API if available (HTTPS required)
    if (navigator.clipboard && window.isSecureContext) {
      await navigator.clipboard.writeText(text);
      return;
    }
    
    // Fallback method for older browsers or non-secure contexts
    const textArea = document.createElement('textarea');
    textArea.value = text;
    textArea.style.position = 'fixed';
    textArea.style.left = '-999999px';
    textArea.style.top = '-999999px';
    textArea.style.opacity = '0';
    textArea.setAttribute('readonly', '');
    textArea.setAttribute('aria-hidden', 'true');
    
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    
    const successful = document.execCommand('copy');
    textArea.remove();
    
    if (!successful) {
      throw new Error('Copy command was unsuccessful');
    }
  } catch (error) {
    throw new Error(`Failed to copy to clipboard: ${error instanceof Error ? error.message : 'Unknown error'}`);
  }
};

/**
 * Downloads content as a file by creating a temporary blob and anchor element
 * @param content File content to download
 * @param filename Name for the downloaded file
 * @param mimeType MIME type for the file (e.g., 'text/plain', 'application/json')
 */
export const downloadFile = (content: string, filename: string, mimeType: string): void => {
  try {
    // Validate MIME type against whitelist
    if (!validateMimeType(mimeType)) {
      throw new Error(`Invalid or unsafe MIME type: ${mimeType}. Allowed types: ${ALLOWED_MIME_TYPES.join(', ')}`);
    }
    
    // Sanitize filename for security
    const safeFilename = sanitizeFilename(filename);
    
    // Create blob with validated MIME type
    const blob = new Blob([content], { type: mimeType });
    const url = URL.createObjectURL(blob);
    
    // Create temporary anchor element for download
    const anchor = document.createElement('a');
    anchor.href = url;
    anchor.download = safeFilename;
    anchor.style.display = 'none';
    anchor.setAttribute('aria-hidden', 'true');
    
    // Trigger download
    document.body.appendChild(anchor);
    anchor.click();
    
    // Cleanup
    document.body.removeChild(anchor);
    URL.revokeObjectURL(url);
  } catch (error) {
    throw new Error(`Failed to download file: ${error instanceof Error ? error.message : 'Unknown error'}`);
  }
};

/**
 * Utility function to generate safe filename with timestamp
 * @param baseName Base name for the file (without extension)
 * @param extension File extension (with or without dot)
 * @returns Safe filename with timestamp
 */
export const generateSafeFilename = (baseName: string, extension: string): string => {
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
  
  // Use enhanced sanitization for base name
  const safeBaseName = sanitizeFilename(baseName).toLowerCase() || 'export';
  
  // Sanitize and validate extension
  const cleanExtension = extension.replace(/[^a-z0-9.]/gi, '');
  const safeExtension = cleanExtension.startsWith('.') ? cleanExtension : `.${cleanExtension}`;
  
  // Validate extension is reasonable
  if (safeExtension.length > 10 || !/^\.[a-z0-9]{1,8}$/i.test(safeExtension)) {
    throw new Error(`Invalid file extension: ${extension}`);
  }
  
  const filename = `${safeBaseName}_${timestamp}${safeExtension}`;
  
  // Final length check
  if (filename.length > MAX_FILENAME_LENGTH) {
    const maxBaseLength = MAX_FILENAME_LENGTH - timestamp.length - safeExtension.length - 1;
    const truncatedBase = safeBaseName.substring(0, maxBaseLength);
    return `${truncatedBase}_${timestamp}${safeExtension}`;
  }
  
  return filename;
};

/**
 * Validates messages array before export operations
 * @param messages Array of messages to validate
 * @throws Error if messages array is invalid
 */
export const validateMessages = (messages: Message[]): void => {
  if (!Array.isArray(messages)) {
    throw new Error('Messages must be an array');
  }
  
  if (messages.length === 0) {
    throw new Error('Cannot export empty message list');
  }
  
  // Validate each message structure
  messages.forEach((message, index) => {
    if (!message.id || typeof message.id !== 'string') {
      throw new Error(`Invalid message ID at index ${index}`);
    }
    
    if (!message.content || typeof message.content !== 'string') {
      throw new Error(`Invalid message content at index ${index}`);
    }
    
    if (!message.sender || !['user', 'ai'].includes(message.sender)) {
      throw new Error(`Invalid message sender at index ${index}`);
    }
    
    if (!message.timestamp || !(message.timestamp instanceof Date)) {
      throw new Error(`Invalid message timestamp at index ${index}`);
    }
  });
};

/**
 * Converts a single message to markdown format with proper structure and timestamp
 * @param message Individual message to convert
 * @returns Formatted markdown string for the single message
 */
export const convertSingleMessageToMarkdown = (message: Message): string => {
  try {
    // Validate the single message structure
    if (!message.id || typeof message.id !== 'string') {
      throw new Error('Invalid message ID');
    }
    
    if (!message.content || typeof message.content !== 'string') {
      throw new Error('Invalid message content');
    }
    
    if (!message.sender || !['user', 'ai'].includes(message.sender)) {
      throw new Error('Invalid message sender');
    }
    
    if (!message.timestamp || !(message.timestamp instanceof Date)) {
      throw new Error('Invalid message timestamp');
    }

    const sender = message.sender === 'user' ? '👤 User' : '🤖 AI Assistant';
    const timestamp = message.timestamp.toLocaleString();
    
    // Apply content sanitization to prevent XSS while preserving formatting
    const content = sanitizeContent(message.content.trim());
    
    return `## ${sender} - ${timestamp}\n\n${content}`;
  } catch (error) {
    throw new Error(`Failed to convert message to markdown: ${error instanceof Error ? error.message : 'Unknown error'}`);
  }
};

/**
 * Gets the most recent message of a specific sender type from messages array
 * @param messages Array of messages to search through
 * @param sender The sender type to find ('user' or 'ai')
 * @returns The most recent message of the specified sender type, or null if not found
 */
export const getMostRecentMessage = (messages: Message[], sender: 'user' | 'ai'): Message | null => {
  try {
    if (!Array.isArray(messages)) {
      return null;
    }
    
    if (messages.length === 0) {
      return null;
    }
    
    // Filter messages by sender type and get the last one
    const filteredMessages = messages.filter(message => message.sender === sender);
    
    if (filteredMessages.length === 0) {
      return null;
    }
    
    return filteredMessages[filteredMessages.length - 1];
  } catch (error) {
    console.warn('Failed to get most recent message:', error);
    return null;
  }
};

// Export utility object for easier importing
export const exportHelpers = {
  convertToMarkdown,
  convertToJSON,
  copyToClipboard,
  downloadFile,
  generateSafeFilename,
  validateMessages,
  convertSingleMessageToMarkdown,
  getMostRecentMessage
};