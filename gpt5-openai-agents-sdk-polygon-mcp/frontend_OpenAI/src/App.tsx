import ChatInterface_OpenAI, { interfaceStyles } from './components/ChatInterface_OpenAI';
import { messageStyles } from './components/ChatMessage_OpenAI';
import { inputStyles } from './components/ChatInput_OpenAI';

export default function App() {
  return (
    <>
      <style>{interfaceStyles}</style>
      <style>{messageStyles}</style>
      <style>{inputStyles}</style>
      <ChatInterface_OpenAI />
    </>
  );
}