feat: complete GPT-5 configuration optimization with rate limiting removal and performance maximization

- Remove ALL OpenAI rate limiting code/config for maximum model performance
- Update max_tokens from 4096/8192 to 128000 (16x improvement) for GPT-5 models
- Increase max_context_length from 128000 to 400000 (3x improvement)
- Optimize temperature to 0.2 for financial analysis (moved to extra_args)
- Implement ModelSettings with GPT-5 specific optimizations:
  * Reasoning effort set to "low" for optimal performance
  * Verbosity set to "low" for concise financial responses
  * Service tier and user tracking via extra_args
- Remove rate limiting from Settings class, dependencies.py, and app.config.json
- Update TypeScript interface to remove rate limiting properties
- Fix temperature parameter conflicts in ModelSettings configuration
- Maintain 9.99/10 Python linting score and resolve TypeScript type errors

Files modified:
- src/backend/config.py: Remove rate limiting, update AI config defaults
- src/backend/dependencies.py: Remove get_model_rate_limits function
- src/backend/routers/models.py: Update max_tokens to 128000
- src/backend/services/agent_service.py: Add ModelSettings optimization
- config/app.config.json: Remove rate limiting, update context length
- src/frontend/config/config.loader.ts: Update TypeScript interface

Testing: CLI tests pass (7/7) with real market data responses
Performance: 16x output capacity, 3x input capacity, zero rate limiting constraints