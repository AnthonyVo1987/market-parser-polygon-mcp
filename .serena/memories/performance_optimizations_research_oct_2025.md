# Performance Optimizations Research - October 2025

## Overview
Comprehensive research on performance improvements for Market Parser Gradio PWA deployed on Hugging Face Spaces. Identifies 20+ optimizations across 6 categories with potential for 3x-5x faster responses and 10-20x more concurrent users.

**Full Documentation**: See `research_task_plan.md` for complete details.

---

## Quick Wins - Phase 1 (1-2 hours, 50-70% improvement)

### 1. Gradio Queue Configuration (10 min)
**File**: `app.py` line 17

**Current Code**:
```python
demo.launch(
    server_name="0.0.0.0",
    server_port=7860,
    share=False,
    show_error=True,
)
```

**Optimization**:
```python
demo.queue(
    default_concurrency_limit=10,  # default=1, increase to 10
    max_size=100,  # prevent runaway queue
).launch(
    server_name="0.0.0.0",
    server_port=7860,
    max_threads=80,  # increase from 40 to 80 (monitor memory)
    share=False,
    show_error=True,
)
```

**Parameters**:
- `default_concurrency_limit`: Linearly multiplies server capacity. Start with 10, increase to 20 if resources allow.
- `max_threads`: Total thread pool size (default 40). Increase to 60-80 for production.
- `max_size`: Queue max size. Set to 100-200 to prevent excess requests.

**Impact**: 10-20x concurrent user capacity
**Complexity**: Very Low (2 parameter additions)
**Risk**: Low (backwards compatible)

---

### 2. ❌ ABANDONED: API Response Caching (LRU) (30 min)

**STATUS:** NOT IMPLEMENTED - External caching removed (2025-10-19)

**Reason for Abandonment:**
- @lru_cache decorator is incompatible with async-first architecture
- App already uses OpenAI native prompt caching for efficiency
- External caching adds complexity without measurable benefit

**See:** `.serena/memories/lru_cache_removal_rationale_oct_2025.md`

---

#### Original Research (Historical Reference):

**File**: `src/backend/tools/*.py` (polygon_tools.py, tradier_tools.py)

**Option A - Simple In-Memory LRU Cache**:
```python
from functools import lru_cache
import time

@lru_cache(maxsize=1000)
def get_cached_stock_quote(symbol: str, timestamp_minute: int = None):
    """Cache stock quotes by 1-minute buckets"""
    if timestamp_minute is None:
        timestamp_minute = int(time.time() / 60)
    return get_stock_quote(symbol)  # existing function
```

**Option B - requests-cache (HTTP-level)**:
```python
import requests_cache

requests_cache.install_cache(
    'market_data_cache',
    expire_after=300,  # 5 minutes TTL
    backend='sqlite',  # or 'redis', 'memory'
)
```

**Caching Strategy by Data Type**:
- Stock prices (OHLC): 60-300 seconds (market hours volatility)
- Historical data: 24 hours (immutable)
- Options chains: 60 seconds (high volatility)
- Company info: 7 days (rarely changes)
- Market status: 60 seconds (changes at market open/close)

**Impact**: 50-80% API call reduction, 3-10x faster (cache hits)
**Complexity**: Low (decorator additions)
**Risk**: Low (in-memory, no persistence issues)

---

### 3. Connection Pooling (20 min)
**File**: `src/backend/tools/api_utils.py` or similar

**Current Pattern** (likely):
```python
import requests

def fetch_data(url):
    response = requests.get(url)  # New connection each time!
    return response.json()
```

**Optimized Pattern**:
```python
import aiohttp

class APIClient:
    def __init__(self):
        self.session = aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(
                limit=100,           # max 100 concurrent
                limit_per_host=10,   # max 10 per host
            )
        )

    async def fetch_data(self, url: str):
        async with self.session.get(url) as response:
            return await response.json()

    async def close(self):
        await self.session.close()

# Singleton pattern
_api_client = None

def get_api_client():
    global _api_client
    if _api_client is None:
        _api_client = APIClient()
    return _api_client
```

**Impact**: 30-50% faster repeated API calls (eliminate TCP handshake overhead)
**Complexity**: Low (requires aiohttp integration)
**Risk**: Low (transparent optimization)

---

## Phase 2 - API Optimization (Week 1, 8-12 hours)

### 4. aiohttp Integration (2-4 hours)
**Files**: `src/backend/tools/polygon_tools.py`, `tradier_tools.py`

Replace synchronous `requests` with async `aiohttp` for HTTP calls.

**Before**:
```python
import requests
response = requests.get(f"{POLYGON_API}/v2/snapshot/locale/us/markets/stocks/tickers/{symbol}")
```

**After**:
```python
import aiohttp
async with aiohttp.ClientSession() as session:
    async with session.get(f"{POLYGON_API}/v2/snapshot/locale/us/markets/stocks/tickers/{symbol}") as response:
        return await response.json()
```

**Impact**: 3x faster HTTP requests, handles thousands of simultaneous connections
**Complexity**: Medium (requires async refactoring)
**Risk**: Medium (code changes in tools/)

---

### 5. Intelligent Caching Strategy (2-3 hours)
**Options**:

**Option A - Redis (Distributed)**:
```python
import redis
import json

redis_client = redis.Redis(host='localhost', port=6379, db=0)

async def get_cached_data(key: str, ttl: int = 300):
    cached = redis_client.get(key)
    if cached:
        return json.loads(cached)
    
    data = await fetch_from_api(key)
    redis_client.setex(key, ttl, json.dumps(data))
    return data
```

**Option B - SQLite (Persistent)**:
```python
import requests_cache

requests_cache.install_cache(
    'market_data_cache',
    backend='sqlite',
    expire_after=300,
)
```

**Impact**: 80% cost savings, 50-80% API reduction
**Complexity**: Medium (requires Redis/SQLite setup)
**Risk**: Medium (Redis requires external server)

---

### 6. Request Batching (1-2 hours)
**File**: `src/backend/cli.py` or agent service

**Pattern - Use asyncio.gather() for parallel requests**:
```python
import asyncio

async def get_multiple_stock_prices(*symbols):
    """Fetch multiple stock prices in parallel"""
    tasks = [get_stock_quote(symbol) for symbol in symbols]
    results = await asyncio.gather(*tasks)
    return results

# Usage: 3 stocks in parallel instead of sequential
prices = await get_multiple_stock_prices("AAPL", "GOOGL", "MSFT")
```

**Impact**: 3-10x faster multi-stock queries
**Complexity**: Low (add asyncio.gather calls)
**Risk**: Low (non-blocking parallelization)

---

### 7. Rate Limit Protection (1 hour)
**Install**: `pip install ratelimit` or `requests-ratelimiter`

```python
from ratelimit import limits, sleep_and_retry

@sleep_and_retry
@limits(calls=100, period=1)  # 100 calls per second
async def fetch_polygon_data(endpoint: str):
    return await api_client.get(endpoint)
```

**Impact**: 100% rate limit compliance
**Complexity**: Low (decorator addition)
**Risk**: Low

---

## Phase 3 - PWA Features (Week 2, 8-16 hours)

### 8. Service Worker + Caching Strategies (4-8 hours)
**Files**: New `public/service-worker.js`, update `app.py`

**Caching Strategies**:

1. **Cache-First** (Static Assets):
   - CSS, JS, images, fonts
   - Serve cached, fallback to network
   - Instant loading

2. **Network-First** (API Responses):
   - Real-time stock prices
   - Market data
   - Always try network first, fallback to cache

3. **Stale-While-Revalidate** (Mixed Content):
   - Historical data
   - Company info
   - Return cached immediately, update background

**Implementation**: Use Workbox for simplified management

**Impact**: Instant UI loading, offline functionality, 50-90% faster perceived performance
**Complexity**: High (requires JavaScript service worker)
**Risk**: Medium (can break app if misconfigured)

---

### 9. Background Sync (2-4 hours)
Allow users to submit queries while offline, process when online.

**Impact**: Offline query queuing
**Complexity**: High
**Risk**: Medium (complex error handling)

---

## Phase 4 - Advanced Optimization (Week 3-4, 16-24 hours)

### 10. Complete Async Refactor (8-16 hours)
Ensure all I/O operations use async/await throughout codebase.

**Impact**: 300% performance potential
**Complexity**: Very High
**Risk**: High (major code changes)

---

### 11. Task Prioritization (1-2 hours)
Use `asyncio.create_task()` for high-priority operations.

```python
async def process_urgent_query(query: str):
    task = asyncio.create_task(fetch_critical_data())
    other_data = await fetch_supplementary_data()
    critical_data = await task
    return combine_results(critical_data, other_data)
```

**Impact**: 30% improvement in critical operation response times
**Complexity**: Low
**Risk**: Low

---

### 12. Cold Start Optimization (varies)
**Lazy Loading**:
```python
def get_polygon_client():
    global _polygon_client
    if _polygon_client is None:
        from polygon import RESTClient
        _polygon_client = RESTClient(api_key=POLYGON_API_KEY)
    return _polygon_client
```

**Impact**: 30-50% faster cold starts
**Complexity**: Low
**Risk**: Low

---

### 13. Performance Monitoring Dashboard (4-6 hours)
Add metrics tracking:
- Response times
- Cache hit rates
- Concurrent users
- API call counts
- Error rates

---

### 14. Resource Monitoring (1-2 hours)
```python
import psutil
import os

def log_resource_usage():
    process = psutil.Process(os.getpid())
    memory_mb = process.memory_info().rss / 1024 / 1024
    cpu_percent = process.cpu_percent()
    print(f"Memory: {memory_mb:.2f} MB, CPU: {cpu_percent:.2f}%")
```

**Impact**: Identify bottlenecks
**Complexity**: Low
**Risk**: Low

---

## Performance Impact Summary

### Response Time Improvements
- **Cached responses**: 5-10s → 0.5-2s (5-10x faster)
- **Uncached responses**: 5-10s → 3-7s (30-50% faster with aiohttp + batching)

### Concurrent Capacity
- **Current**: 1-2 concurrent (Gradio default)
- **Optimized**: 10-20 concurrent users (Gradio queue configuration)

### API Cost Reduction
- **Current**: 100% API calls
- **Optimized**: 20-50% API calls (50-80% reduction)

### User Experience
- Instant UI loading (Gradio 5 SSR + PWA caching)
- Offline functionality (service worker)
- Faster perceived performance (stale-while-revalidate)

---

## Recommended Implementation Order

**Priority 1 (Start Here)**:
1. Gradio Queue Configuration (10 min)
2. API Response Caching LRU (30 min)
3. Connection Pooling (20 min)

**Priority 2 (Next Week)**:
4. aiohttp Integration (2-4 hours)
5. Intelligent Caching (2-3 hours)
6. Request Batching (1-2 hours)

**Priority 3 (Later)**:
7. Service Worker / PWA (4-8 hours)
8. Performance Monitoring (varies)

---

## Tool Architecture Notes

**Important**: App uses **direct Python function tools** (NOT MCP tools)
- Tools already in memory: `get_stock_quote`, `get_options_expiration_dates`, `get_stock_price_history`, `get_market_status_and_date_time`, `get_ta_indicators`, `get_call_options_chain`, `get_put_options_chain`
- Zero tool discovery overhead
- Focus optimizations on: API response caching, HTTP connection pooling, request batching

---

## Files to Modify

**Quick Wins Phase 1**:
- `app.py` - Add queue configuration
- `src/backend/tools/polygon_tools.py` - Add @lru_cache decorators
- `src/backend/tools/tradier_tools.py` - Add @lru_cache decorators
- `src/backend/tools/api_utils.py` - Add connection pooling

**Phase 2**:
- `src/backend/tools/polygon_tools.py` - aiohttp integration
- `src/backend/tools/tradier_tools.py` - aiohttp integration
- `src/backend/services/agent_service.py` - Rate limiting, request batching

**Phase 3**:
- `public/service-worker.js` - New service worker
- `app.py` - Service worker registration
- `src/backend/config.py` - PWA configuration

---

## Testing Strategy

**Load Testing**:
```bash
pip install locust
locust -f locustfile.py --host=https://your-space.hf.space
```

**Cache Monitoring**:
```python
# Track cache hit rates
cache_stats = {"hits": 0, "misses": 0}
hit_rate = cache_stats["hits"] / (cache_stats["hits"] + cache_stats["misses"]) * 100
```

**Performance Benchmarking**:
```python
import time

def benchmark_query(query: str, iterations: int = 10):
    times = []
    for _ in range(iterations):
        start = time.perf_counter()
        result = process_query(query)
        times.append(time.perf_counter() - start)
    
    print(f"Avg: {sum(times)/len(times):.3f}s")
    print(f"Min: {min(times):.3f}s")
    print(f"Max: {max(times):.3f}s")
```

**Lighthouse PWA Audit**:
```bash
npm install -g lighthouse
lighthouse https://your-space.hf.space --view --preset=desktop
```

**Target Scores**: 90+ (Performance, PWA, Accessibility, Best Practices)

---

## Success Criteria

**Performance Targets**:
- Average response time < 3s (uncached), < 1s (cached)
- Concurrent capacity: 10+ users
- Cache hit rate: > 60%
- API call reduction: > 50%

**Reliability Targets**:
- 100% rate limit compliance
- < 1% error rate
- Offline functionality working

**User Experience Targets**:
- Lighthouse Performance Score: 90+
- Lighthouse PWA Score: 90+
- First Contentful Paint: < 1.5s
- Time to Interactive: < 3s

---

## Reference Documentation

- Full research: `research_task_plan.md`
- Gradio docs: https://www.gradio.app/guides/setting-up-a-demo-for-maximum-performance
- Python asyncio: https://docs.python.org/3/library/asyncio.html
- aiohttp: https://docs.aiohttp.org/
- Workbox: https://developer.chrome.com/docs/workbox/
- Polygon.io: https://polygon.io/knowledge-base/categories/rest

---

**Created**: 2025-10-19
**Status**: Ready for implementation
**Pick & Choose**: Use this as a menu of optimizations to implement as needed
