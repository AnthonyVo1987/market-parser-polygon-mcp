# Market Parser API Security & Performance Guide

## Server Configuration

**Static Endpoints:**
- **Backend API**: http://127.0.0.1:8000
- **Frontend Development**: http://127.0.0.1:3000
- **Frontend Production**: http://127.0.0.1:5500

**One-Click Startup:**
```bash
npm run start:app
```

## Security Architecture

### 1. Authentication & Authorization

#### Current Implementation
The current system operates without authentication for development simplicity. For production deployment, consider implementing:

**Option A: API Key Authentication (Recommended for MVP)**
```python
# Simple API key middleware
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer(auto_error=False)

async def verify_api_key(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if not credentials:
        raise HTTPException(status_code=401, detail="API key required")
    
    # Simple API key validation
    valid_keys = {"your-api-key-here", "frontend-key-123"}
    if credentials.credentials not in valid_keys:
        raise HTTPException(status_code=403, detail="Invalid API key")
    
    return credentials.credentials

# Apply to endpoints
@app.post("/api/v1/analysis/chat")
async def process_chat(request: ChatRequest, api_key: str = Depends(verify_api_key)):
    # Implementation here
    pass
```

**Option B: JWT Token Authentication (For Multi-User Systems)**
```python
from jose import JWTError, jwt
from datetime import datetime, timedelta

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def verify_token(token: str = Depends(security)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        return user_id
    except JWTError:
        raise credentials_exception
```

### 2. Input Validation & Sanitization

#### Comprehensive Input Validation
```python
from pydantic import BaseModel, validator, Field
import re
from typing import Optional

class SecureChatRequest(BaseModel):
    message: str = Field(..., min_length=2, max_length=2000)
    source: str = Field(..., regex="^(button|user)$")
    analysis_type: Optional[str] = Field(None, regex="^(snapshot|support_resistance|technical)$")
    ticker: Optional[str] = Field(None, regex="^[A-Z]{1,5}$")
    session_id: Optional[str] = Field(None, max_length=100)
    
    @validator('message')
    def sanitize_message(cls, v):
        # Remove potentially harmful content
        cleaned = re.sub(r'<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>', '', v, flags=re.IGNORECASE)
        cleaned = re.sub(r'javascript:', '', cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r'on\w+\s*=', '', cleaned, flags=re.IGNORECASE)
        return cleaned.strip()
    
    @validator('ticker')
    def validate_ticker(cls, v):
        if v is None:
            return v
        
        # Blacklist of reserved/test tickers
        blacklist = {'TEST', 'NULL', 'ADMIN', 'DEBUG', 'SAMPLE'}
        if v.upper() in blacklist:
            raise ValueError('Invalid ticker symbol')
        
        return v.upper()
    
    @validator('session_id')
    def validate_session_id(cls, v):
        if v is None:
            return v
        
        # Only allow alphanumeric and underscores
        if not re.match(r'^[a-zA-Z0-9_]+$', v):
            raise ValueError('Invalid session ID format')
        
        return v

# XSS Protection for responses
from html import escape

def sanitize_response(content: str) -> str:
    """Sanitize response content to prevent XSS attacks"""
    # Escape HTML entities but preserve markdown formatting
    content = escape(content)
    
    # Allow specific markdown tags (whitelist approach)
    allowed_tags = {
        '**': '<strong>',
        '**': '</strong>',
        '*': '<em>',
        '*': '</em>',
        '`': '<code>',
        '`': '</code>'
    }
    
    # Note: For production, use a proper markdown sanitizer like bleach
    return content
```

### 3. Rate Limiting & DDoS Protection

#### Advanced Rate Limiting
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import redis
from functools import wraps

# Redis-backed rate limiting for production
limiter = Limiter(
    key_func=get_remote_address,
    storage_uri="redis://localhost:6379",
    default_limits=["200 per day", "50 per hour"]
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Different limits for different endpoints
@app.post("/api/v1/analysis/chat")
@limiter.limit("10/minute")  # Expensive AI operations
async def process_chat(request: Request, chat_request: ChatRequest):
    pass

@app.get("/api/v1/prompts/templates")
@limiter.limit("100/minute")  # Cheap template retrieval
async def get_templates(request: Request):
    pass

# Advanced rate limiting with user tiers
def rate_limit_by_tier(tier: str):
    """Apply different rate limits based on user tier"""
    limits = {
        "free": "5/minute",
        "premium": "20/minute", 
        "enterprise": "100/minute"
    }
    
    def decorator(func):
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            # Extract user tier from API key or JWT token
            user_tier = extract_user_tier(request)  # Implement this
            limit = limits.get(user_tier, "5/minute")
            
            # Apply dynamic rate limiting
            await limiter.limit(limit)(request)
            return await func(request, *args, **kwargs)
        return wrapper
    return decorator
```

### 4. CORS Security Configuration

#### Production CORS Setup
```python
from fastapi.middleware.cors import CORSMiddleware

# Production CORS configuration
origins = [
    "https://your-production-domain.com",
    "https://api.your-domain.com",
    # Add staging domains
    "https://staging.your-domain.com"
]

# Development CORS (only for local development)
if settings.ENVIRONMENT == "development":
    origins.extend([
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000"
    ])

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],  # Only needed methods
    allow_headers=["Content-Type", "Authorization", "X-API-Key"],
    expose_headers=["X-RateLimit-Remaining", "X-RateLimit-Reset"]
)
```

### 5. Data Privacy & Compliance

#### Sensitive Data Handling
```python
import hashlib
from datetime import datetime, timedelta

class DataPrivacyManager:
    """Manage sensitive data and compliance requirements"""
    
    @staticmethod
    def hash_session_id(session_id: str) -> str:
        """Hash session IDs for privacy"""
        return hashlib.sha256(session_id.encode()).hexdigest()[:16]
    
    @staticmethod
    def sanitize_logs(log_data: dict) -> dict:
        """Remove sensitive information from logs"""
        sensitive_fields = ['api_key', 'session_id', 'user_id']
        
        sanitized = log_data.copy()
        for field in sensitive_fields:
            if field in sanitized:
                sanitized[field] = "***REDACTED***"
        
        return sanitized
    
    @staticmethod
    def should_store_data(user_consent: bool, data_type: str) -> bool:
        """Check if data can be stored based on user consent"""
        if not user_consent:
            return False
        
        # Different retention policies for different data types
        storage_policies = {
            "chat_history": user_consent,
            "analysis_results": user_consent,
            "performance_metrics": True,  # Anonymous metrics always allowed
            "error_logs": True  # Error logs for debugging
        }
        
        return storage_policies.get(data_type, False)

# Usage in logging
import logging
from pythonjsonlogger import jsonlogger

# Configure secure logging
class SecureJSONFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        
        # Add timestamp
        log_record['timestamp'] = datetime.utcnow().isoformat()
        
        # Sanitize sensitive data
        privacy_manager = DataPrivacyManager()
        for key, value in list(log_record.items()):
            if key in ['session_id', 'api_key', 'user_id']:
                log_record[key] = "***REDACTED***"

# Apply secure logging
logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = SecureJSONFormatter('%(timestamp)s %(level)s %(name)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
```

## Performance Optimization

### 1. Caching Strategy

#### Multi-Level Caching
```python
from functools import lru_cache
import redis
import pickle
import json
from datetime import datetime, timedelta

class CacheManager:
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.redis_client = redis.from_url(redis_url)
        self.local_cache = {}
        self.cache_ttl = {
            "templates": timedelta(hours=24),      # Templates rarely change
            "company_names": timedelta(hours=12),  # Company names stable
            "market_status": timedelta(minutes=5), # Market status changes
            "analysis_results": timedelta(minutes=30)  # Cache expensive analyses
        }
    
    def get(self, key: str, cache_type: str = "default"):
        """Get value from cache with fallback levels"""
        # Level 1: In-memory cache (fastest)
        if key in self.local_cache:
            item = self.local_cache[key]
            if datetime.now() < item['expires']:
                return item['data']
            else:
                del self.local_cache[key]
        
        # Level 2: Redis cache (network call but persistent)
        try:
            cached = self.redis_client.get(key)
            if cached:
                data = pickle.loads(cached)
                
                # Store in local cache for next access
                ttl = self.cache_ttl.get(cache_type, timedelta(minutes=5))
                self.local_cache[key] = {
                    'data': data,
                    'expires': datetime.now() + ttl
                }
                
                return data
        except Exception as e:
            logger.warning(f"Redis cache error: {e}")
        
        return None
    
    def set(self, key: str, value: any, cache_type: str = "default"):
        """Set value in both cache levels"""
        ttl = self.cache_ttl.get(cache_type, timedelta(minutes=5))
        
        # Set in local cache
        self.local_cache[key] = {
            'data': value,
            'expires': datetime.now() + ttl
        }
        
        # Set in Redis cache
        try:
            self.redis_client.setex(
                key, 
                int(ttl.total_seconds()), 
                pickle.dumps(value)
            )
        except Exception as e:
            logger.warning(f"Redis cache set error: {e}")

# Cache integration with API endpoints
cache_manager = CacheManager()

@lru_cache(maxsize=100)
def get_cached_templates():
    """Cache templates in memory since they rarely change"""
    return template_manager.get_templates()

async def get_company_name(ticker: str) -> str:
    """Cache company name lookups"""
    cache_key = f"company_name:{ticker}"
    cached = cache_manager.get(cache_key, "company_names")
    
    if cached:
        return cached
    
    # Expensive lookup
    company_name = await external_api.get_company_name(ticker)
    cache_manager.set(cache_key, company_name, "company_names")
    
    return company_name
```

### 2. Request Optimization

#### Connection Pooling & Async Optimization
```python
import httpx
from contextlib import asynccontextmanager

class OptimizedHTTPClient:
    """HTTP client with connection pooling and retry logic"""
    
    def __init__(self):
        # Connection pooling for external API calls
        limits = httpx.Limits(max_keepalive_connections=20, max_connections=100)
        timeout = httpx.Timeout(10.0, connect=5.0)
        
        self.client = httpx.AsyncClient(
            limits=limits,
            timeout=timeout,
            headers={"User-Agent": "MarketParser/1.0"}
        )
    
    async def get_with_retry(self, url: str, retries: int = 3) -> dict:
        """GET request with exponential backoff retry"""
        for attempt in range(retries):
            try:
                response = await self.client.get(url)
                response.raise_for_status()
                return response.json()
            except httpx.RequestError as e:
                if attempt == retries - 1:
                    raise
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
        
        return {}
    
    async def close(self):
        await self.client.aclose()

# Global HTTP client instance
http_client = OptimizedHTTPClient()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting optimized HTTP client")
    yield
    # Shutdown
    await http_client.close()
    logger.info("Closed HTTP client connections")

# Apply to FastAPI app
app = FastAPI(lifespan=lifespan)
```

#### Request Batching
```python
import asyncio
from collections import defaultdict
from typing import List, Dict

class BatchProcessor:
    """Batch similar requests to reduce API calls"""
    
    def __init__(self, batch_size: int = 10, wait_time: float = 0.1):
        self.batch_size = batch_size
        self.wait_time = wait_time
        self.pending_requests = defaultdict(list)
        self.batch_tasks = {}
    
    async def batch_ticker_data(self, tickers: List[str]) -> Dict[str, dict]:
        """Batch multiple ticker requests into single API call"""
        if len(tickers) == 1:
            # Single request, process immediately
            return await self._fetch_single_ticker(tickers[0])
        
        # Group tickers for batch processing
        batch_key = "ticker_batch"
        
        if batch_key not in self.batch_tasks:
            # Start new batch task
            self.batch_tasks[batch_key] = asyncio.create_task(
                self._process_ticker_batch(batch_key)
            )
        
        # Add tickers to pending batch
        future = asyncio.Future()
        self.pending_requests[batch_key].extend([
            (ticker, future) for ticker in tickers
        ])
        
        # Wait for batch processing
        return await future
    
    async def _process_ticker_batch(self, batch_key: str):
        """Process a batch of ticker requests"""
        await asyncio.sleep(self.wait_time)  # Wait for batch to fill
        
        if batch_key not in self.pending_requests:
            return
        
        requests = self.pending_requests[batch_key][:self.batch_size]
        del self.pending_requests[batch_key][:self.batch_size]
        
        if not requests:
            return
        
        # Extract tickers and futures
        tickers = [req[0] for req in requests]
        futures = [req[1] for req in requests]
        
        try:
            # Make batch API call
            batch_data = await self._fetch_batch_ticker_data(tickers)
            
            # Resolve futures with individual results
            for ticker, future in zip(tickers, futures):
                if not future.done():
                    future.set_result(batch_data.get(ticker, {}))
                    
        except Exception as e:
            # Handle errors by failing all futures
            for _, future in requests:
                if not future.done():
                    future.set_exception(e)
        
        # Clean up
        if batch_key in self.batch_tasks:
            del self.batch_tasks[batch_key]
    
    async def _fetch_batch_ticker_data(self, tickers: List[str]) -> Dict[str, dict]:
        """Fetch data for multiple tickers in single request"""
        # Implementation depends on your data source API
        # Many financial APIs support comma-separated ticker lists
        ticker_list = ",".join(tickers)
        url = f"https://api.polygon.io/v2/aggs/grouped/locale/us/market/stocks/{datetime.now().date()}"
        
        response = await http_client.get_with_retry(url)
        
        # Transform response to ticker -> data mapping
        return {ticker: data for ticker, data in response.get("results", {}).items()}

# Usage in endpoints
batch_processor = BatchProcessor()

@app.post("/api/v1/analysis/batch")
async def batch_analysis(tickers: List[str]):
    """Process multiple tickers efficiently"""
    ticker_data = await batch_processor.batch_ticker_data(tickers)
    
    # Process each ticker's data
    results = []
    for ticker, data in ticker_data.items():
        analysis = await process_ticker_analysis(ticker, data)
        results.append(analysis)
    
    return {"results": results}
```

### 3. Database Optimization (If Using Database)

#### Connection Pooling & Query Optimization
```python
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.pool import StaticPool

# Optimized database configuration
engine = create_async_engine(
    "sqlite+aiosqlite:///./market_parser.db",
    echo=False,  # Set to True for debugging
    poolclass=StaticPool,
    pool_pre_ping=True,  # Validate connections
    pool_recycle=3600,   # Recycle connections every hour
    connect_args={
        "check_same_thread": False,
        "timeout": 10
    }
)

async_session = async_sessionmaker(
    engine, 
    expire_on_commit=False,
    autoflush=True
)

# Database query optimization
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

class OptimizedQueries:
    """Optimized database queries for common operations"""
    
    @staticmethod
    async def get_user_sessions_with_messages(user_id: int, limit: int = 50):
        """Efficient query with eager loading"""
        async with async_session() as session:
            stmt = (
                select(ChatSession)
                .options(selectinload(ChatSession.messages))  # Eager load messages
                .where(ChatSession.user_id == user_id)
                .order_by(ChatSession.created_at.desc())
                .limit(limit)
            )
            
            result = await session.execute(stmt)
            return result.scalars().all()
    
    @staticmethod
    async def get_popular_tickers(days: int = 7, limit: int = 10):
        """Get most analyzed tickers with aggregation"""
        async with async_session() as session:
            # Use SQL aggregation instead of Python grouping
            stmt = (
                select(
                    AnalysisRequest.ticker,
                    func.count(AnalysisRequest.id).label('request_count')
                )
                .where(AnalysisRequest.created_at >= datetime.now() - timedelta(days=days))
                .group_by(AnalysisRequest.ticker)
                .order_by(func.count(AnalysisRequest.id).desc())
                .limit(limit)
            )
            
            result = await session.execute(stmt)
            return result.all()
```

### 4. Memory Management

#### Efficient Response Processing
```python
import psutil
import gc
from typing import Generator

class MemoryOptimizedProcessor:
    """Process large responses with memory efficiency"""
    
    def __init__(self, memory_threshold: float = 0.8):
        self.memory_threshold = memory_threshold
        
    def check_memory_usage(self) -> float:
        """Check current memory usage percentage"""
        memory = psutil.virtual_memory()
        return memory.percent / 100.0
    
    async def process_large_analysis(self, data: dict) -> Generator[dict, None, None]:
        """Process analysis in chunks to manage memory"""
        # Process data in smaller chunks
        chunk_size = 100
        
        for i in range(0, len(data.get("time_series", [])), chunk_size):
            # Check memory usage
            if self.check_memory_usage() > self.memory_threshold:
                # Force garbage collection
                gc.collect()
                
                # If still high memory usage, wait briefly
                if self.check_memory_usage() > self.memory_threshold:
                    await asyncio.sleep(0.1)
            
            # Process chunk
            chunk = data["time_series"][i:i+chunk_size]
            processed_chunk = await self._process_data_chunk(chunk)
            
            yield {
                "chunk_index": i // chunk_size,
                "data": processed_chunk,
                "has_more": i + chunk_size < len(data["time_series"])
            }
    
    async def _process_data_chunk(self, chunk: list) -> dict:
        """Process individual data chunk"""
        # Implement your chunk processing logic
        return {"processed_count": len(chunk), "summary": "processed"}

# Usage with streaming response
from fastapi.responses import StreamingResponse
import json

@app.post("/api/v1/analysis/large-dataset")
async def analyze_large_dataset(request: LargeDataRequest):
    """Handle large dataset analysis with streaming"""
    
    processor = MemoryOptimizedProcessor()
    
    async def generate_response():
        async for chunk in processor.process_large_analysis(request.data):
            yield f"data: {json.dumps(chunk)}\n\n"
        
        yield f"data: {json.dumps({'type': 'complete'})}\n\n"
    
    return StreamingResponse(
        generate_response(),
        media_type="text/plain",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive"
        }
    )
```

### 5. Monitoring & Observability

#### Performance Monitoring
```python
from prometheus_client import Counter, Histogram, Gauge, generate_latest
from starlette.middleware.base import BaseHTTPMiddleware
import time

# Prometheus metrics
REQUEST_COUNT = Counter(
    'api_requests_total', 
    'Total API requests',
    ['method', 'endpoint', 'status_code']
)

REQUEST_DURATION = Histogram(
    'api_request_duration_seconds',
    'Request duration in seconds',
    ['method', 'endpoint']
)

ACTIVE_CONNECTIONS = Gauge(
    'active_connections',
    'Active WebSocket connections'
)

CACHE_HITS = Counter('cache_hits_total', 'Cache hits', ['cache_type'])
CACHE_MISSES = Counter('cache_misses_total', 'Cache misses', ['cache_type'])

class MonitoringMiddleware(BaseHTTPMiddleware):
    """Middleware to collect performance metrics"""
    
    async def dispatch(self, request, call_next):
        start_time = time.time()
        
        # Extract endpoint info
        method = request.method
        path = request.url.path
        
        try:
            response = await call_next(request)
            status_code = response.status_code
        except Exception as e:
            status_code = 500
            raise
        finally:
            # Record metrics
            duration = time.time() - start_time
            
            REQUEST_COUNT.labels(
                method=method,
                endpoint=path,
                status_code=status_code
            ).inc()
            
            REQUEST_DURATION.labels(
                method=method,
                endpoint=path
            ).observe(duration)
        
        return response

# Add monitoring middleware
app.add_middleware(MonitoringMiddleware)

# Metrics endpoint
@app.get("/metrics")
async def get_metrics():
    """Prometheus metrics endpoint"""
    return Response(generate_latest(), media_type="text/plain")

# Health check with detailed status
@app.get("/api/v1/health/detailed")
async def detailed_health_check():
    """Detailed health check with performance metrics"""
    # Check external service health
    services_health = {}
    
    # Check Polygon API
    try:
        start_time = time.time()
        # Make a simple API call
        response = await http_client.get_with_retry("https://api.polygon.io/v3/reference/tickers?limit=1")
        services_health["polygon_api"] = {
            "status": "healthy",
            "response_time_ms": int((time.time() - start_time) * 1000)
        }
    except Exception as e:
        services_health["polygon_api"] = {
            "status": "unhealthy",
            "error": str(e)
        }
    
    # Check OpenAI API
    try:
        start_time = time.time()
        # Make a simple API call to OpenAI
        # Implementation depends on your OpenAI client setup
        services_health["openai_api"] = {
            "status": "healthy",
            "response_time_ms": int((time.time() - start_time) * 1000)
        }
    except Exception as e:
        services_health["openai_api"] = {
            "status": "unhealthy",
            "error": str(e)
        }
    
    # System metrics
    memory = psutil.virtual_memory()
    cpu_percent = psutil.cpu_percent(interval=1)
    
    return {
        "overall_status": "healthy" if all(s["status"] == "healthy" for s in services_health.values()) else "degraded",
        "services": services_health,
        "system_metrics": {
            "memory_usage_percent": memory.percent,
            "memory_available_mb": memory.available // 1024 // 1024,
            "cpu_usage_percent": cpu_percent
        },
        "timestamp": datetime.utcnow().isoformat()
    }
```

## Production Deployment Checklist

### Security Hardening
- [ ] Enable HTTPS with valid SSL certificates
- [ ] Configure secure headers (HSTS, CSP, etc.)
- [ ] Implement rate limiting with Redis backend
- [ ] Set up API key or JWT authentication
- [ ] Enable request logging and monitoring
- [ ] Configure CORS for production domains only
- [ ] Implement input sanitization and validation
- [ ] Set up secure session management
- [ ] Enable SQL injection protection (if using database)
- [ ] Configure environment variable security

### Performance Optimization
- [ ] Set up Redis caching layer
- [ ] Configure connection pooling
- [ ] Enable response compression (gzip)
- [ ] Set up CDN for static assets
- [ ] Configure database indexing
- [ ] Enable HTTP/2 support
- [ ] Set up load balancing (if needed)
- [ ] Configure async workers appropriately
- [ ] Enable request batching where applicable
- [ ] Set up monitoring and alerting

### Monitoring & Observability
- [ ] Set up Prometheus metrics collection
- [ ] Configure Grafana dashboards
- [ ] Set up error tracking (Sentry, etc.)
- [ ] Enable structured logging
- [ ] Configure health check endpoints
- [ ] Set up uptime monitoring
- [ ] Configure performance alerting
- [ ] Enable distributed tracing (if microservices)
- [ ] Set up log aggregation
- [ ] Configure backup and recovery procedures

### Environment Configuration
```env
# Production environment variables
ENVIRONMENT=production
API_VERSION=v1
DEBUG=false

# Security
SECRET_KEY=your-super-secret-key-here
API_KEYS=prod-key-1,prod-key-2
ALLOWED_ORIGINS=https://your-domain.com,https://api.your-domain.com

# Rate Limiting
REDIS_URL=redis://your-redis-server:6379
RATE_LIMIT_PER_MINUTE=60

# External APIs
POLYGON_API_KEY=your-polygon-api-key
OPENAI_API_KEY=your-openai-api-key

# Performance
MAX_CONCURRENT_REQUESTS=100
REQUEST_TIMEOUT_SECONDS=30
CACHE_TTL_MINUTES=30

# Monitoring
ENABLE_METRICS=true
LOG_LEVEL=INFO
SENTRY_DSN=your-sentry-dsn
```

This security and performance guide provides comprehensive protection and optimization strategies for your Market Parser API in production environments.