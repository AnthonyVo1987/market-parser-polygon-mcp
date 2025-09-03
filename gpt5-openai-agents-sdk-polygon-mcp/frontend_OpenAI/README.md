# OpenAI Chat Frontend

A simple React frontend for the OpenAI chatbot interface, built with Vite and TypeScript.

## Setup

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

## Project Structure

```
frontend_OpenAI/
├── src/
│   ├── components/
│   │   ├── ChatInterface_OpenAI.tsx    # Main chat container
│   │   ├── ChatInput_OpenAI.tsx        # Message input form
│   │   └── ChatMessage_OpenAI.tsx      # Individual message display
│   ├── services/
│   │   └── api_OpenAI.ts               # API service for FastAPI calls
│   ├── types/
│   │   └── chat_OpenAI.ts              # TypeScript interfaces
│   ├── App.tsx                         # Main app component
│   └── main.tsx                        # React entry point
├── package.json
├── vite.config.ts
├── tsconfig.json
└── index.html
```

## Features

- Simple, deterministic React chat interface
- TypeScript for type safety
- Minimal dependencies (React + Vite + TypeScript)
- Simple fetch() calls to FastAPI backend at `http://localhost:8000/chat`
- Real-time chat with loading states
- Error handling and display
- Clean, modern UI with inline styles

## API Integration

The frontend expects a FastAPI backend running on `http://localhost:8000` with a `/chat` endpoint that:

- Accepts POST requests with JSON body: `{ "message": "user message here" }`
- Returns JSON response: `{ "message": "AI response here" }`
- Returns error responses: `{ "error": "error message" }`

## Development Commands

- `npm run dev` - Start development server
- `npm run build` - Build for production  
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## Architecture Notes

- Uses simple `useState` for message state management
- No complex React patterns or useEffect dependency arrays
- Deterministic behavior with straightforward data flow
- All components use "_OpenAI" naming convention
- Inline styles for simplicity (production apps should use CSS modules/styled-components)