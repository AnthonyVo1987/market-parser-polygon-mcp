# Phase 4: Advanced Optimization & Production Hardening Implementation Plan

**Status**: Ready for Implementation
**Estimated Time**: 20-26 hours
**Expected Impact**: 300% performance potential, production-ready, enterprise-grade monitoring
**Risk Level**: MEDIUM-LOW (mostly additive features, minimal breaking changes)
**Prerequisites**: Phase 1, Phase 2, and Phase 3 completed (highly recommended)

---

## Overview

### Objectives

Transform Market Parser into a production-ready, enterprise-grade application with:

1. **Production Logging & Metrics**: Structured logging, correlation IDs, performance tracking
2. **Performance Dashboard**: Real-time monitoring with visualizations
3. **Cold Start Optimization**: HF Spaces-specific optimizations, keep-alive service
4. **Advanced Async Patterns**: Circuit breakers, retry logic, task prioritization
5. **Load Testing**: Automated performance benchmarking and regression tests
6. **Production Hardening**: Error tracking, rate limiting, graceful shutdown

### Scope

**In Scope:**
- Structured JSON logging with correlation IDs
- Custom performance dashboard (HTML + Chart.js)
- Resource monitoring (CPU, memory, disk)
- Cold start optimization for HF Spaces
- Circuit breaker and retry patterns
- Load testing with Locust
- Production hardening (timeouts, rate limiting, error tracking)
- Comprehensive documentation

**Out of Scope:**
- External monitoring services (Datadog, New Relic) - focus on self-hosted
- Complex distributed tracing (keep simple for single-server deployment)
- Kubernetes/container orchestration (HF Spaces handles this)
- Custom ML model optimization (out of scope for this phase)

### Expected Impact

**Performance:**
- **Sustained performance**: Handle 10-20 concurrent users without degradation
- **Zero cold starts**: During business hours (with keep-alive)
- **Sub-3s queries**: 95% of queries under 3 seconds (with all optimizations)
- **99.9% uptime**: With circuit breakers and graceful degradation

**Monitoring:**
- **Real-time visibility**: Dashboard shows performance metrics, errors, resource usage
- **Alerting**: Automatic alerts for high resource usage, error spikes
- **Historical data**: 30-day metrics history for trend analysis
- **Debugging**: Correlation IDs make request tracing easy

**Production Readiness:**
- **Error resilience**: Circuit breakers prevent cascading failures
- **Resource protection**: Rate limiting prevents abuse
- **Graceful degradation**: App continues functioning during partial failures
- **Documentation**: Complete playbooks for operations and troubleshooting

---

## Prerequisites

### Required Knowledge

- Python logging and monitoring
- Async programming patterns (asyncio)
- Load testing concepts
- System resource monitoring
- Web dashboard development (HTML, JavaScript)

### Required Tools

- Python 3.10+ with asyncio
- Chrome/Firefox for testing dashboard
- Locust for load testing (`pip install locust`)
- psutil for resource monitoring (`pip install psutil`)

### Dependencies to Install

```bash
# Add to requirements.txt or pyproject.toml:
psutil>=5.9.0           # Resource monitoring
locust>=2.15.0          # Load testing
prometheus-client>=0.17.0  # Optional: Prometheus metrics format
```

### Verification Commands

```bash
# Install dependencies
uv add psutil locust

# Verify installations
python -c "import psutil; print(f'psutil {psutil.__version__}')"
locust --version

# Check current resource usage
python -c "import psutil; print(f'CPU: {psutil.cpu_percent()}%, Memory: {psutil.virtual_memory().percent}%')"
```

---

## Task Breakdown

### Task 1: Production Logging & Metrics Collection (4-5 hours)

#### Overview

Implement structured JSON logging with correlation IDs for request tracing, and create a metrics collection system to track performance over time.

#### Step-by-Step Implementation

**Step 1.1: Create Structured Logging Module** (60 minutes)

Create `src/backend/services/logging_service.py`:

```python
"""
Production-grade structured logging with correlation IDs.
"""
import logging
import json
import sys
from datetime import datetime
from typing import Any, Dict, Optional
from contextvars import ContextVar

# Context variable for correlation ID (thread-safe)
correlation_id_ctx: ContextVar[Optional[str]] = ContextVar('correlation_id', default=None)


class JSONFormatter(logging.Formatter):
    """JSON formatter for structured logging."""

    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON."""
        log_data: Dict[str, Any] = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'level': record.levelname,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
        }

        # Add correlation ID if present
        correlation_id = correlation_id_ctx.get()
        if correlation_id:
            log_data['correlation_id'] = correlation_id

        # Add extra fields from record
        if hasattr(record, 'user_query'):
            log_data['user_query'] = record.user_query
        if hasattr(record, 'response_time'):
            log_data['response_time_ms'] = record.response_time
        if hasattr(record, 'error'):
            log_data['error'] = str(record.error)
            log_data['error_type'] = record.error.__class__.__name__

        # Add exception info if present
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)

        return json.dumps(log_data)


def setup_logging(log_level: str = "INFO") -> logging.Logger:
    """
    Set up production logging with JSON formatting.

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger("market_parser")
    logger.setLevel(getattr(logging, log_level.upper()))

    # Remove existing handlers
    logger.handlers.clear()

    # Console handler with JSON formatter
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(JSONFormatter())
    logger.addHandler(console_handler)

    # Prevent propagation to root logger
    logger.propagate = False

    return logger


def set_correlation_id(correlation_id: str) -> None:
    """Set correlation ID for current context."""
    correlation_id_ctx.set(correlation_id)


def get_correlation_id() -> Optional[str]:
    """Get correlation ID from current context."""
    return correlation_id_ctx.get()


# Global logger instance
logger = setup_logging()
```

**What this does:**
- **JSON logging**: All logs in structured JSON format for easy parsing
- **Correlation IDs**: Track requests across the entire system
- **Context variables**: Thread-safe correlation ID storage
- **Extra fields**: Attach custom data (query, response time, errors)
- **Exception tracking**: Automatic exception info in logs

**Step 1.2: Create Metrics Collection Module** (90 minutes)

Create `src/backend/services/metrics_service.py`:

```python
"""
In-memory metrics collection for performance monitoring.
"""
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections import deque
from typing import Dict, List, Optional
from threading import Lock


@dataclass
class MetricPoint:
    """Single metric data point."""
    timestamp: datetime
    value: float
    tags: Dict[str, str] = field(default_factory=dict)


class MetricsCollector:
    """Thread-safe in-memory metrics collector."""

    def __init__(self, retention_hours: int = 24):
        """
        Initialize metrics collector.

        Args:
            retention_hours: How long to keep metrics in memory
        """
        self.retention_hours = retention_hours
        self.retention_seconds = retention_hours * 3600

        # Counters (cumulative)
        self.counters: Dict[str, int] = {}

        # Gauges (current value)
        self.gauges: Dict[str, float] = {}

        # Histograms (time series data)
        self.histograms: Dict[str, deque] = {}

        # Thread safety
        self._lock = Lock()

        # Startup time
        self.start_time = time.time()

    def increment(self, metric_name: str, value: int = 1, tags: Optional[Dict[str, str]] = None) -> None:
        """Increment a counter metric."""
        with self._lock:
            if metric_name not in self.counters:
                self.counters[metric_name] = 0
            self.counters[metric_name] += value

    def gauge(self, metric_name: str, value: float, tags: Optional[Dict[str, str]] = None) -> None:
        """Set a gauge metric (current value)."""
        with self._lock:
            self.gauges[metric_name] = value

    def histogram(self, metric_name: str, value: float, tags: Optional[Dict[str, str]] = None) -> None:
        """Add a histogram data point (for percentiles, averages)."""
        with self._lock:
            if metric_name not in self.histograms:
                self.histograms[metric_name] = deque(maxlen=10000)  # Keep last 10k points

            self.histograms[metric_name].append(
                MetricPoint(
                    timestamp=datetime.utcnow(),
                    value=value,
                    tags=tags or {}
                )
            )

            # Prune old data
            self._prune_histogram(metric_name)

    def _prune_histogram(self, metric_name: str) -> None:
        """Remove data points older than retention period."""
        if metric_name not in self.histograms:
            return

        cutoff_time = datetime.utcnow() - timedelta(seconds=self.retention_seconds)
        histogram = self.histograms[metric_name]

        # Remove old points from left (oldest)
        while histogram and histogram[0].timestamp < cutoff_time:
            histogram.popleft()

    def get_counter(self, metric_name: str) -> int:
        """Get counter value."""
        with self._lock:
            return self.counters.get(metric_name, 0)

    def get_gauge(self, metric_name: str) -> Optional[float]:
        """Get gauge value."""
        with self._lock:
            return self.gauges.get(metric_name)

    def get_histogram_stats(self, metric_name: str, minutes: int = 5) -> Dict[str, float]:
        """
        Get histogram statistics for recent time window.

        Args:
            metric_name: Name of histogram metric
            minutes: Time window in minutes

        Returns:
            Dict with avg, min, max, p50, p95, p99, count
        """
        with self._lock:
            if metric_name not in self.histograms:
                return {}

            # Filter to time window
            cutoff_time = datetime.utcnow() - timedelta(minutes=minutes)
            values = [
                point.value
                for point in self.histograms[metric_name]
                if point.timestamp >= cutoff_time
            ]

            if not values:
                return {}

            # Sort for percentiles
            sorted_values = sorted(values)
            count = len(sorted_values)

            def percentile(p: float) -> float:
                """Calculate percentile."""
                k = (count - 1) * p
                f = int(k)
                c = f + 1 if c < count else f
                if f == c:
                    return sorted_values[f]
                return sorted_values[f] * (c - k) + sorted_values[c] * (k - f)

            return {
                'count': count,
                'avg': sum(values) / count,
                'min': min(values),
                'max': max(values),
                'p50': percentile(0.50),
                'p95': percentile(0.95),
                'p99': percentile(0.99),
            }

    def get_all_metrics(self) -> Dict:
        """Get all current metrics."""
        with self._lock:
            return {
                'counters': dict(self.counters),
                'gauges': dict(self.gauges),
                'histograms': {
                    name: self.get_histogram_stats(name)
                    for name in self.histograms.keys()
                },
                'uptime_seconds': time.time() - self.start_time,
            }

    def reset(self) -> None:
        """Reset all metrics (use with caution)."""
        with self._lock:
            self.counters.clear()
            self.gauges.clear()
            self.histograms.clear()


# Global metrics collector
metrics = MetricsCollector(retention_hours=24)
```

**What this does:**
- **Three metric types**: Counters (cumulative), Gauges (current value), Histograms (time series)
- **Thread-safe**: Uses locks for concurrent access
- **Automatic retention**: Keeps 24 hours of data, auto-prunes old data
- **Percentile calculations**: P50, P95, P99 for response times
- **In-memory**: No database needed, fast access

**Step 1.3: Add Logging Middleware** (60 minutes)

Modify `app.py` to add logging middleware:

```python
# app.py
import uuid
from fastapi import FastAPI, Request
from fastapi.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware
import time

from src.backend.services.logging_service import logger, set_correlation_id, get_correlation_id
from src.backend.services.metrics_service import metrics


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for request/response logging and metrics."""

    async def dispatch(self, request: Request, call_next):
        # Generate correlation ID
        correlation_id = str(uuid.uuid4())
        set_correlation_id(correlation_id)

        # Log request
        logger.info(
            "Request started",
            extra={
                'correlation_id': correlation_id,
                'method': request.method,
                'path': request.url.path,
                'client_ip': request.client.host,
            }
        )

        # Track request
        metrics.increment('requests_total')
        metrics.increment(f'requests_by_path_{request.url.path.replace("/", "_")}')

        # Time request
        start_time = time.perf_counter()

        try:
            # Process request
            response = await call_next(request)

            # Calculate duration
            duration_ms = (time.perf_counter() - start_time) * 1000

            # Track metrics
            metrics.histogram('request_duration_ms', duration_ms)
            metrics.increment(f'requests_by_status_{response.status_code}')

            if response.status_code >= 200 and response.status_code < 300:
                metrics.increment('requests_successful')
            elif response.status_code >= 400:
                metrics.increment('requests_failed')

            # Log response
            logger.info(
                "Request completed",
                extra={
                    'correlation_id': correlation_id,
                    'status_code': response.status_code,
                    'duration_ms': duration_ms,
                }
            )

            # Add correlation ID to response headers
            response.headers['X-Correlation-ID'] = correlation_id

            return response

        except Exception as e:
            # Track error
            metrics.increment('requests_error')
            metrics.increment(f'errors_{e.__class__.__name__}')

            # Log error
            logger.error(
                "Request failed",
                extra={
                    'correlation_id': correlation_id,
                    'error': str(e),
                },
                exc_info=True
            )

            raise


# Apply middleware
if __name__ == "__main__":
    # Check if we need FastAPI wrapper for HF Spaces
    is_hf_spaces = os.getenv("SPACE_ID") is not None

    if is_hf_spaces:
        app = FastAPI()

        # Add logging middleware
        app.add_middleware(LoggingMiddleware)

        # Mount Gradio app
        app = gr.mount_gradio_app(app, demo, path="/")

        # Run with uvicorn (HF Spaces handles this)
    else:
        # Local development
        demo.queue(...).launch(...)
```

**What this does:**
- **Correlation IDs**: Every request gets unique ID for tracking
- **Request logging**: Log start and completion of every request
- **Performance tracking**: Measure and record request duration
- **Error tracking**: Log and count all errors
- **Response headers**: Include correlation ID in response for debugging

**Step 1.4: Integrate Logging in CLI** (60 minutes)

Modify `src/backend/cli.py` to add logging:

```python
# cli.py
from src.backend.services.logging_service import logger
from src.backend.services.metrics_service import metrics
import time


async def process_query_with_footer(agent: Agent, session: Session, user_input: str) -> str:
    """Process query with performance metrics and logging."""
    start_time = time.perf_counter()

    # Log query start
    logger.info(
        "Query processing started",
        extra={'user_query': user_input}
    )

    # Track query
    metrics.increment('queries_total')

    try:
        # Process query (existing code)
        result = await process_query(agent, session, user_input)

        # Calculate metrics
        elapsed_time = time.perf_counter() - start_time
        elapsed_ms = elapsed_time * 1000

        # Track metrics
        metrics.histogram('query_duration_ms', elapsed_ms)
        metrics.increment('queries_successful')

        # Track token usage (if available from result)
        if hasattr(result, 'usage'):
            metrics.histogram('tokens_used', result.usage.total_tokens)
            metrics.histogram('tokens_input', result.usage.input_tokens)
            metrics.histogram('tokens_output', result.usage.output_tokens)

        # Log success
        logger.info(
            "Query processing completed",
            extra={
                'user_query': user_input,
                'response_time_ms': elapsed_ms,
                'tokens_used': getattr(result.usage, 'total_tokens', None) if hasattr(result, 'usage') else None,
            }
        )

        # Return result with footer (existing code)
        return result + f"\n\nPerformance: {elapsed_time:.3f}s"

    except Exception as e:
        # Track error
        metrics.increment('queries_failed')
        metrics.increment(f'query_errors_{e.__class__.__name__}')

        # Log error
        logger.error(
            "Query processing failed",
            extra={
                'user_query': user_input,
                'error': str(e),
            },
            exc_info=True
        )

        raise
```

**What this does:**
- **Query logging**: Log every query with timing and results
- **Metric tracking**: Track query duration, token usage, success/failure
- **Error logging**: Detailed error logs with stack traces
- **Performance footer**: Already implemented, now also logged

#### Success Criteria

- ✅ Structured JSON logs in console/stdout
- ✅ Correlation IDs present in all logs
- ✅ Request/response logging working
- ✅ Metrics collecting (counters, gauges, histograms)
- ✅ Error tracking with stack traces
- ✅ No performance degradation (< 5ms overhead)

#### Testing

1. **Test logging**:

   ```bash
   # Start app
   uv run python app.py

   # Submit query
   # Check logs in console (should see JSON format)

   # Verify correlation ID in logs
   grep "correlation_id" <log_output>
   ```

2. **Test metrics**:

   ```python
   # In Python console or script:
   from src.backend.services.metrics_service import metrics

   # Check counters
   print(metrics.get_counter('requests_total'))

   # Check histogram stats
   print(metrics.get_histogram_stats('request_duration_ms'))
   ```

3. **Test error logging**:

   ```bash
   # Trigger an error (e.g., invalid query)
   # Check logs for error with stack trace
   # Verify error counter incremented
   ```

#### Rollback Plan

If logging breaks the app:

1. **Disable middleware**:
   - Comment out `app.add_middleware(LoggingMiddleware)`

2. **Revert to basic logging**:
   - Remove JSON formatter
   - Use standard `logging.basicConfig()`

3. **Test without metrics**:
   - Comment out all `metrics.` calls
   - Verify app works normally

---

### Task 2: Performance Dashboard & Monitoring (5-6 hours)

#### Overview

Create a real-time performance dashboard with visualizations for metrics, resource usage, and system health. Includes `/metrics`, `/status`, and `/dashboard` endpoints.

#### Step-by-Step Implementation

**Step 2.1: Create Metrics API Endpoint** (60 minutes)

Modify `app.py` to add metrics endpoint:

```python
# app.py (in FastAPI section)
from src.backend.services.metrics_service import metrics
from src.backend.services.logging_service import logger
import psutil
import os


@app.get("/metrics")
async def get_metrics():
    """
    Get current metrics in JSON format.

    Returns:
        JSON with all current metrics
    """
    try:
        all_metrics = metrics.get_all_metrics()

        return {
            'status': 'success',
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'metrics': all_metrics,
        }
    except Exception as e:
        logger.error("Failed to fetch metrics", exc_info=True)
        return {
            'status': 'error',
            'error': str(e),
        }


@app.get("/status")
async def get_status():
    """
    Get system status and resource usage.

    Returns:
        JSON with system status, resource usage, and health checks
    """
    try:
        # Get process info
        process = psutil.Process(os.getpid())

        # Resource usage
        cpu_percent = process.cpu_percent(interval=0.1)
        memory_info = process.memory_info()
        memory_mb = memory_info.rss / 1024 / 1024

        # System info
        system_memory = psutil.virtual_memory()
        disk_usage = psutil.disk_usage('/')

        # Uptime
        uptime_seconds = time.time() - metrics.start_time

        return {
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'uptime_seconds': uptime_seconds,
            'uptime_human': str(timedelta(seconds=int(uptime_seconds))),
            'process': {
                'pid': os.getpid(),
                'cpu_percent': cpu_percent,
                'memory_mb': memory_mb,
                'memory_percent': process.memory_percent(),
                'num_threads': process.num_threads(),
                'num_connections': len(process.connections()),
            },
            'system': {
                'cpu_count': psutil.cpu_count(),
                'memory_total_gb': system_memory.total / 1024 / 1024 / 1024,
                'memory_available_gb': system_memory.available / 1024 / 1024 / 1024,
                'memory_percent': system_memory.percent,
                'disk_total_gb': disk_usage.total / 1024 / 1024 / 1024,
                'disk_used_gb': disk_usage.used / 1024 / 1024 / 1024,
                'disk_free_gb': disk_usage.free / 1024 / 1024 / 1024,
                'disk_percent': disk_usage.percent,
            },
            'metrics_summary': {
                'total_requests': metrics.get_counter('requests_total'),
                'successful_requests': metrics.get_counter('requests_successful'),
                'failed_requests': metrics.get_counter('requests_failed'),
                'total_queries': metrics.get_counter('queries_total'),
                'successful_queries': metrics.get_counter('queries_successful'),
                'failed_queries': metrics.get_counter('queries_failed'),
            },
        }
    except Exception as e:
        logger.error("Failed to fetch status", exc_info=True)
        return {
            'status': 'error',
            'error': str(e),
        }


@app.get("/health")
async def health_check():
    """
    Simple health check endpoint for keep-alive services.

    Returns:
        JSON with health status
    """
    return {
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'uptime_seconds': time.time() - metrics.start_time,
    }
```

**What this does:**
- **/metrics**: Returns all collected metrics (for monitoring tools)
- **/status**: Returns system resource usage and health
- **/health**: Simple endpoint for keep-alive pings
- **Error handling**: Graceful errors if metrics fail

**Step 2.2: Create Dashboard HTML** (180 minutes)

Create `static/dashboard.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Market Parser - Performance Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: #0f172a;
            color: #e2e8f0;
            padding: 20px;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
        }

        header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 2px solid #334155;
        }

        h1 {
            font-size: 2em;
            color: #fff;
        }

        .status-badge {
            padding: 8px 16px;
            border-radius: 20px;
            font-weight: 600;
            font-size: 0.9em;
        }

        .status-healthy {
            background: #10b981;
            color: #fff;
        }

        .status-warning {
            background: #f59e0b;
            color: #fff;
        }

        .status-error {
            background: #ef4444;
            color: #fff;
        }

        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }

        .card {
            background: #1e293b;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        }

        .card h3 {
            font-size: 0.9em;
            color: #94a3b8;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .card .value {
            font-size: 2.5em;
            font-weight: 700;
            color: #fff;
            margin-bottom: 5px;
        }

        .card .label {
            font-size: 0.85em;
            color: #64748b;
        }

        .chart-container {
            background: #1e293b;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        }

        .chart-container h2 {
            font-size: 1.2em;
            color: #fff;
            margin-bottom: 20px;
        }

        .refresh-indicator {
            font-size: 0.8em;
            color: #64748b;
        }

        .refresh-indicator.active {
            color: #10b981;
        }

        @media (max-width: 768px) {
            .grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📊 Performance Dashboard</h1>
            <div>
                <span class="status-badge status-healthy" id="statusBadge">Healthy</span>
                <span class="refresh-indicator" id="refreshIndicator">Auto-refresh: 10s</span>
            </div>
        </header>

        <!-- Real-time Stats -->
        <div class="grid">
            <div class="card">
                <h3>Uptime</h3>
                <div class="value" id="uptime">--</div>
                <div class="label">Hours</div>
            </div>
            <div class="card">
                <h3>Total Requests</h3>
                <div class="value" id="totalRequests">--</div>
                <div class="label">Since startup</div>
            </div>
            <div class="card">
                <h3>Success Rate</h3>
                <div class="value" id="successRate">--</div>
                <div class="label">Percentage</div>
            </div>
            <div class="card">
                <h3>Avg Response Time</h3>
                <div class="value" id="avgResponseTime">--</div>
                <div class="label">Milliseconds (5min)</div>
            </div>
            <div class="card">
                <h3>CPU Usage</h3>
                <div class="value" id="cpuUsage">--</div>
                <div class="label">Percentage</div>
            </div>
            <div class="card">
                <h3>Memory Usage</h3>
                <div class="value" id="memoryUsage">--</div>
                <div class="label">MB</div>
            </div>
        </div>

        <!-- Response Time Chart -->
        <div class="chart-container">
            <h2>Response Time (Last 5 Minutes)</h2>
            <canvas id="responseTimeChart"></canvas>
        </div>

        <!-- Cache Hit Rate Chart -->
        <div class="chart-container">
            <h2>Cache Hit Rate</h2>
            <canvas id="cacheHitChart"></canvas>
        </div>
    </div>

    <script>
        // Chart.js configuration
        const chartConfig = {
            responsive: true,
            maintainAspectRatio: true,
            aspectRatio: 3,
            plugins: {
                legend: {
                    labels: {
                        color: '#e2e8f0'
                    }
                }
            },
            scales: {
                y: {
                    ticks: { color: '#94a3b8' },
                    grid: { color: '#334155' }
                },
                x: {
                    ticks: { color: '#94a3b8' },
                    grid: { color: '#334155' }
                }
            }
        };

        // Response Time Chart
        const responseTimeCtx = document.getElementById('responseTimeChart').getContext('2d');
        const responseTimeChart = new Chart(responseTimeCtx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: 'Avg Response Time (ms)',
                    data: [],
                    borderColor: '#3b82f6',
                    backgroundColor: 'rgba(59, 130, 246, 0.1)',
                    tension: 0.4
                }, {
                    label: 'P95 Response Time (ms)',
                    data: [],
                    borderColor: '#f59e0b',
                    backgroundColor: 'rgba(245, 158, 11, 0.1)',
                    tension: 0.4
                }]
            },
            options: chartConfig
        });

        // Cache Hit Chart
        const cacheHitCtx = document.getElementById('cacheHitChart').getContext('2d');
        const cacheHitChart = new Chart(cacheHitCtx, {
            type: 'doughnut',
            data: {
                labels: ['Cache Hits', 'Cache Misses'],
                datasets: [{
                    data: [70, 30],
                    backgroundColor: ['#10b981', '#ef4444']
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        labels: {
                            color: '#e2e8f0'
                        }
                    }
                }
            }
        });

        // Data history (last 20 points)
        const dataHistory = {
            timestamps: [],
            avgResponseTimes: [],
            p95ResponseTimes: [],
            maxPoints: 20
        };

        // Fetch and update data
        async function updateDashboard() {
            const refreshIndicator = document.getElementById('refreshIndicator');
            refreshIndicator.classList.add('active');

            try {
                // Fetch metrics and status
                const [metricsRes, statusRes] = await Promise.all([
                    fetch('/metrics'),
                    fetch('/status')
                ]);

                const metrics = await metricsRes.json();
                const status = await statusRes.json();

                // Update status badge
                const statusBadge = document.getElementById('statusBadge');
                statusBadge.textContent = status.status === 'healthy' ? 'Healthy' : 'Degraded';
                statusBadge.className = `status-badge status-${status.status === 'healthy' ? 'healthy' : 'warning'}`;

                // Update stats
                document.getElementById('uptime').textContent = (status.uptime_seconds / 3600).toFixed(1);
                document.getElementById('totalRequests').textContent = metrics.metrics.counters.requests_total || 0;

                // Success rate
                const total = metrics.metrics.counters.requests_total || 0;
                const successful = metrics.metrics.counters.requests_successful || 0;
                const successRate = total > 0 ? ((successful / total) * 100).toFixed(1) : '--';
                document.getElementById('successRate').textContent = total > 0 ? `${successRate}%` : '--';

                // Response time
                const requestStats = metrics.metrics.histograms.request_duration_ms || {};
                const avgResponseTime = requestStats.avg ? requestStats.avg.toFixed(0) : '--';
                document.getElementById('avgResponseTime').textContent = avgResponseTime;

                // Resource usage
                document.getElementById('cpuUsage').textContent = `${status.process.cpu_percent.toFixed(1)}%`;
                document.getElementById('memoryUsage').textContent = status.process.memory_mb.toFixed(0);

                // Update charts
                const now = new Date().toLocaleTimeString();

                dataHistory.timestamps.push(now);
                dataHistory.avgResponseTimes.push(requestStats.avg || 0);
                dataHistory.p95ResponseTimes.push(requestStats.p95 || 0);

                // Keep only last N points
                if (dataHistory.timestamps.length > dataHistory.maxPoints) {
                    dataHistory.timestamps.shift();
                    dataHistory.avgResponseTimes.shift();
                    dataHistory.p95ResponseTimes.shift();
                }

                // Update response time chart
                responseTimeChart.data.labels = dataHistory.timestamps;
                responseTimeChart.data.datasets[0].data = dataHistory.avgResponseTimes;
                responseTimeChart.data.datasets[1].data = dataHistory.p95ResponseTimes;
                responseTimeChart.update();

                // Update cache hit chart (placeholder - implement when cache metrics available)
                // cacheHitChart.data.datasets[0].data = [cacheHits, cacheMisses];
                // cacheHitChart.update();

            } catch (error) {
                console.error('Failed to fetch dashboard data:', error);
                document.getElementById('statusBadge').textContent = 'Error';
                document.getElementById('statusBadge').className = 'status-badge status-error';
            }

            refreshIndicator.classList.remove('active');
        }

        // Auto-refresh every 10 seconds
        updateDashboard();
        setInterval(updateDashboard, 10000);
    </script>
</body>
</html>
```

**What this does:**
- **Real-time stats**: Uptime, requests, success rate, response time, CPU, memory
- **Live charts**: Response time trends (avg and P95), cache hit rate
- **Auto-refresh**: Updates every 10 seconds
- **Professional UI**: Dark theme, responsive design
- **Chart.js**: Industry-standard charting library

**Step 2.3: Serve Dashboard** (30 minutes)

Modify `app.py` to serve dashboard:

```python
# app.py
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles


# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/dashboard")
async def serve_dashboard():
    """Serve performance dashboard HTML."""
    return FileResponse("static/dashboard.html")
```

**What this does:**
- Serves dashboard at `/dashboard` endpoint
- Serves static files (HTML, CSS, JS)

#### Success Criteria

- ✅ `/metrics` endpoint returns JSON metrics
- ✅ `/status` endpoint returns system status
- ✅ `/health` endpoint responds quickly (< 50ms)
- ✅ `/dashboard` loads and displays charts
- ✅ Dashboard auto-refreshes every 10 seconds
- ✅ Charts update with real data
- ✅ Resource usage accurate (matches system monitor)

#### Testing

1. **Test endpoints**:

   ```bash
   # Start app
   uv run python app.py

   # Test metrics endpoint
   curl http://127.0.0.1:7860/metrics | jq

   # Test status endpoint
   curl http://127.0.0.1:7860/status | jq

   # Test health endpoint
   curl http://127.0.0.1:7860/health | jq
   ```

2. **Test dashboard**:

   ```bash
   # Open in browser
   open http://127.0.0.1:7860/dashboard

   # Verify:
   # - Stats display current values
   # - Charts render correctly
   # - Auto-refresh works (watch for updates)
   # - No console errors
   ```

3. **Load test dashboard**:

   ```bash
   # Generate some load
   for i in {1..50}; do
     curl -X POST http://127.0.0.1:7860/api/query \
       -H "Content-Type: application/json" \
       -d '{"query": "Tesla stock price"}' &
   done

   # Watch dashboard update with new metrics
   ```

#### Rollback Plan

If dashboard breaks:

1. **Disable dashboard endpoint**:
   - Comment out `/dashboard` route

2. **Keep metrics endpoints**:
   - `/metrics` and `/status` are still useful without dashboard

3. **Use command-line monitoring**:
   ```bash
   watch -n 10 'curl -s http://127.0.0.1:7860/status | jq'
   ```

---

### Task 3: Cold Start & Resource Optimization (2-3 hours)

#### Overview

Optimize HF Spaces cold starts with lazy loading and keep-alive service. Reduce startup time by 30-50%.

#### Step-by-Step Implementation

**Step 3.1: Implement Lazy Loading** (60 minutes)

Create `src/backend/services/lazy_loader.py`:

```python
"""
Lazy loading for heavy dependencies to reduce cold start time.
"""
from typing import Any, Optional, Callable
from functools import wraps


class LazyLoader:
    """Lazy loader for heavy dependencies."""

    def __init__(self, import_func: Callable):
        """
        Initialize lazy loader.

        Args:
            import_func: Function that imports and returns the dependency
        """
        self.import_func = import_func
        self._cached_import: Optional[Any] = None

    def __call__(self) -> Any:
        """Get the loaded dependency (load if not cached)."""
        if self._cached_import is None:
            self._cached_import = self.import_func()
        return self._cached_import


# Lazy loaders for heavy dependencies
_polygon_client = None
_tradier_client = None


def get_polygon_client():
    """Get Polygon client (lazy initialized)."""
    global _polygon_client
    if _polygon_client is None:
        from polygon import RESTClient
        import os
        _polygon_client = RESTClient(api_key=os.getenv("POLYGON_API_KEY"))
    return _polygon_client


def get_tradier_client():
    """Get Tradier client (lazy initialized)."""
    global _tradier_client
    if _tradier_client is None:
        # Import and initialize Tradier client
        # (Adjust based on actual Tradier client implementation)
        import os
        _tradier_client = {
            'api_key': os.getenv("TRADIER_API_KEY"),
            'base_url': os.getenv("TRADIER_API_URL", "https://api.tradier.com"),
        }
    return _tradier_client
```

**What this does:**
- **Lazy loading**: Only import when first used
- **Singleton pattern**: Import once, reuse everywhere
- **Faster startup**: Heavy imports delayed until needed

**Step 3.2: Refactor Tools to Use Lazy Loading** (90 minutes)

Modify `src/backend/tools/polygon_tools.py`:

```python
# polygon_tools.py
from src.backend.services.lazy_loader import get_polygon_client

# Remove top-level imports:
# from polygon import RESTClient  # DON'T DO THIS
# client = RESTClient(...)         # DON'T DO THIS


@function_tool
def get_stock_price_history(symbol: str, from_date: str, to_date: str):
    """Get stock price history."""
    # Get client lazily
    client = get_polygon_client()

    # Rest of function...
    return client.get_aggregate_bars(symbol, from_date, to_date)
```

**Do the same for**:
- `src/backend/tools/tradier_tools.py`
- Any other modules with heavy imports

**Step 3.3: Create Keep-Alive GitHub Action** (60 minutes)

Create `.github/workflows/keep-alive.yml`:

```yaml
name: Keep Alive HF Space

on:
  schedule:
    # Run every 5 minutes during business hours (9 AM - 5 PM EST, Mon-Fri)
    # Cron: min hour day month weekday
    - cron: '*/5 13-21 * * 1-5'  # 9 AM - 5 PM EST = 1 PM - 9 PM UTC

jobs:
  ping:
    runs-on: ubuntu-latest

    steps:
      - name: Ping HF Space
        run: |
          # Replace with your actual HF Spaces URL
          URL="https://your-username-market-parser.hf.space/health"

          echo "Pinging $URL at $(date)"

          RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" "$URL")

          if [ "$RESPONSE" -eq 200 ]; then
            echo "✅ Health check passed (HTTP $RESPONSE)"
          else
            echo "❌ Health check failed (HTTP $RESPONSE)"
            exit 1
          fi
```

**What this does:**
- **GitHub Actions**: Free cron job service
- **Business hours only**: Saves resources, prevents spam
- **5-minute interval**: Keeps HF Space awake
- **Health endpoint**: Quick, lightweight check

**Alternative: UptimeRobot** (if you prefer external service):

1. Sign up at uptimerobot.com (free tier)
2. Create HTTP monitor:
   - URL: `https://your-username-market-parser.hf.space/health`
   - Monitoring Interval: 5 minutes
   - Monitor Type: HTTP(s)
3. No code needed, works immediately

#### Success Criteria

- ✅ Cold start time reduced by 30-50% (measure with `time python app.py`)
- ✅ Lazy loading works (imports only when tools called)
- ✅ GitHub Action runs successfully every 5 minutes
- ✅ Health endpoint responds < 50ms
- ✅ No errors from lazy loading

#### Testing

1. **Measure cold start improvement**:

   ```bash
   # Before lazy loading
   time python -c "from src.backend.cli import initialize_persistent_agent; initialize_persistent_agent()"

   # After lazy loading (should be 30-50% faster)
   time python -c "from src.backend.cli import initialize_persistent_agent; initialize_persistent_agent()"
   ```

2. **Test lazy loading**:

   ```python
   # Should not import until first call
   from src.backend.tools.polygon_tools import get_stock_price_history

   # First call triggers import (slower)
   result1 = get_stock_price_history("TSLA", "2024-01-01", "2024-01-31")

   # Second call uses cached client (faster)
   result2 = get_stock_price_history("AAPL", "2024-01-01", "2024-01-31")
   ```

3. **Test GitHub Action** (manually):

   ```bash
   # Trigger workflow manually in GitHub Actions UI
   # Or wait for scheduled run
   # Check workflow logs for success
   ```

#### Rollback Plan

If lazy loading breaks:

1. **Revert to eager loading**:
   - Remove `get_polygon_client()` calls
   - Use top-level imports again

2. **Disable GitHub Action**:
   - Delete `.github/workflows/keep-alive.yml`
   - Or disable in GitHub Actions settings

---

### Task 4: Advanced Async & Error Handling (4-5 hours)

#### Overview

Implement production-grade async patterns: circuit breakers, retry logic, task prioritization, and rate limiting.

#### Step-by-Step Implementation

**Step 4.1: Circuit Breaker Pattern** (120 minutes)

Create `src/backend/services/circuit_breaker.py`:

```python
"""
Circuit breaker pattern for API resilience.
"""
import time
from enum import Enum
from typing import Callable, Any, Optional
from functools import wraps


class CircuitState(Enum):
    """Circuit breaker states."""
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Failing, rejecting requests
    HALF_OPEN = "half_open"  # Testing if service recovered


class CircuitBreakerOpenError(Exception):
    """Raised when circuit breaker is open."""
    pass


class CircuitBreaker:
    """
    Circuit breaker to prevent cascading failures.

    Usage:
        breaker = CircuitBreaker(failure_threshold=5, timeout=60)

        @breaker
        async def call_api():
            return await api.fetch()
    """

    def __init__(
        self,
        failure_threshold: int = 5,
        timeout: int = 60,
        expected_exception: type = Exception,
    ):
        """
        Initialize circuit breaker.

        Args:
            failure_threshold: Number of failures before opening circuit
            timeout: Seconds to wait before trying half-open
            expected_exception: Exception type to count as failure
        """
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.expected_exception = expected_exception

        # State
        self.failure_count = 0
        self.last_failure_time: Optional[float] = None
        self.state = CircuitState.CLOSED

    def __call__(self, func: Callable) -> Callable:
        """Decorator to wrap function with circuit breaker."""

        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            # Check circuit state
            if self.state == CircuitState.OPEN:
                if time.time() - self.last_failure_time >= self.timeout:
                    # Try half-open
                    self.state = CircuitState.HALF_OPEN
                    print(f"[CircuitBreaker] {func.__name__} entering HALF_OPEN state")
                else:
                    # Still open, reject request
                    raise CircuitBreakerOpenError(
                        f"Circuit breaker is OPEN for {func.__name__}"
                    )

            try:
                # Call function
                result = await func(*args, **kwargs)

                # Success - reset if in half-open
                if self.state == CircuitState.HALF_OPEN:
                    self.on_success()

                return result

            except self.expected_exception as e:
                # Failure - record and potentially open circuit
                self.on_failure()
                raise

        return wrapper

    def on_success(self) -> None:
        """Handle successful call."""
        self.failure_count = 0
        self.state = CircuitState.CLOSED
        print("[CircuitBreaker] Reset to CLOSED state")

    def on_failure(self) -> None:
        """Handle failed call."""
        self.failure_count += 1
        self.last_failure_time = time.time()

        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN
            print(
                f"[CircuitBreaker] Opened circuit after {self.failure_count} failures"
            )
```

**Usage in tools**:

```python
# In polygon_tools.py or tradier_tools.py
from src.backend.services.circuit_breaker import CircuitBreaker

# Create circuit breaker for API calls
polygon_breaker = CircuitBreaker(failure_threshold=5, timeout=60)


@polygon_breaker
async def fetch_polygon_data(endpoint: str):
    """Fetch data from Polygon with circuit breaker protection."""
    client = get_polygon_client()
    return await client.get(endpoint)
```

**What this does:**
- **Prevents cascading failures**: If API fails repeatedly, stop calling it
- **Automatic recovery**: After timeout, try half-open to test recovery
- **Failure threshold**: Configurable number of failures before opening
- **Timeout**: Configurable wait time before retrying

**Step 4.2: Retry with Exponential Backoff** (90 minutes)

Create `src/backend/services/retry.py`:

```python
"""
Retry logic with exponential backoff.
"""
import asyncio
from typing import Callable, Any, Optional, Type, Tuple
from functools import wraps


async def retry_with_backoff(
    func: Callable,
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    exponential_base: float = 2.0,
    exceptions: Tuple[Type[Exception], ...] = (Exception,),
) -> Any:
    """
    Retry async function with exponential backoff.

    Args:
        func: Async function to retry
        max_retries: Maximum number of retry attempts
        base_delay: Initial delay in seconds
        max_delay: Maximum delay in seconds
        exponential_base: Base for exponential backoff (default: 2.0)
        exceptions: Tuple of exception types to catch and retry

    Returns:
        Result from successful function call

    Raises:
        Last exception if all retries exhausted
    """
    last_exception = None

    for attempt in range(max_retries + 1):
        try:
            return await func()
        except exceptions as e:
            last_exception = e

            if attempt == max_retries:
                # Final attempt failed
                raise

            # Calculate delay with exponential backoff
            delay = min(base_delay * (exponential_base ** attempt), max_delay)

            print(
                f"[Retry] Attempt {attempt + 1}/{max_retries + 1} failed: {e}. "
                f"Retrying in {delay:.1f}s..."
            )

            await asyncio.sleep(delay)

    # Should never reach here, but satisfy type checker
    raise last_exception


def with_retry(
    max_retries: int = 3,
    base_delay: float = 1.0,
    exceptions: Tuple[Type[Exception], ...] = (Exception,),
):
    """
    Decorator to add retry logic with exponential backoff.

    Usage:
        @with_retry(max_retries=3, base_delay=1.0)
        async def fetch_data():
            return await api.get()
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            return await retry_with_backoff(
                lambda: func(*args, **kwargs),
                max_retries=max_retries,
                base_delay=base_delay,
                exceptions=exceptions,
            )
        return wrapper
    return decorator
```

**Usage in tools**:

```python
from src.backend.services.retry import with_retry

@with_retry(max_retries=3, base_delay=1.0)
async def fetch_stock_price(symbol: str):
    """Fetch stock price with automatic retry."""
    client = get_polygon_client()
    return await client.get_last_trade(symbol)
```

**What this does:**
- **Exponential backoff**: Delay increases exponentially (1s, 2s, 4s, 8s...)
- **Configurable**: Max retries, base delay, exceptions to catch
- **Decorator pattern**: Easy to apply to any async function

**Step 4.3: Request Rate Limiting** (60 minutes)

Create `src/backend/services/rate_limiter.py`:

```python
"""
Request rate limiting for API protection.
"""
import time
from collections import deque
from typing import Optional
from functools import wraps


class RateLimiter:
    """
    Token bucket rate limiter.

    Usage:
        limiter = RateLimiter(max_requests=100, time_window=60)

        @limiter
        async def api_call():
            return await fetch()
    """

    def __init__(self, max_requests: int, time_window: int):
        """
        Initialize rate limiter.

        Args:
            max_requests: Maximum requests allowed in time window
            time_window: Time window in seconds
        """
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests: deque = deque()

    def __call__(self, func):
        """Decorator to add rate limiting."""

        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Remove expired requests
            now = time.time()
            while self.requests and self.requests[0] < now - self.time_window:
                self.requests.popleft()

            # Check if rate limit exceeded
            if len(self.requests) >= self.max_requests:
                # Calculate wait time
                oldest_request = self.requests[0]
                wait_time = (oldest_request + self.time_window) - now

                raise RateLimitExceededError(
                    f"Rate limit exceeded. Retry after {wait_time:.1f}s"
                )

            # Record request
            self.requests.append(now)

            # Execute function
            return await func(*args, **kwargs)

        return wrapper


class RateLimitExceededError(Exception):
    """Raised when rate limit is exceeded."""
    pass
```

**Usage**:

```python
from src.backend.services.rate_limiter import RateLimiter

# Polygon rate limit: 100 req/s
polygon_limiter = RateLimiter(max_requests=100, time_window=1)

@polygon_limiter
async def fetch_polygon_data(endpoint: str):
    """Fetch with rate limiting."""
    client = get_polygon_client()
    return await client.get(endpoint)
```

#### Success Criteria

- ✅ Circuit breaker opens after threshold failures
- ✅ Circuit breaker automatically tries half-open after timeout
- ✅ Retry logic with exponential backoff works
- ✅ Rate limiting prevents exceeding limits
- ✅ All patterns work together without conflicts

#### Testing

1. **Test circuit breaker**:

   ```python
   # Simulate API failures
   async def failing_api():
       raise Exception("API error")

   breaker = CircuitBreaker(failure_threshold=3, timeout=5)

   # Call 5 times (should open circuit after 3)
   for i in range(5):
       try:
           await breaker(failing_api)()
       except Exception as e:
           print(f"Attempt {i+1}: {e}")

   # Should raise CircuitBreakerOpenError after 3 failures
   ```

2. **Test retry logic**:

   ```python
   attempts = 0

   @with_retry(max_retries=3, base_delay=1.0)
   async def flaky_api():
       nonlocal attempts
       attempts += 1
       if attempts < 3:
           raise Exception("Temporary failure")
       return "Success"

   result = await flaky_api()
   print(f"Success after {attempts} attempts")
   ```

3. **Test rate limiting**:

   ```python
   limiter = RateLimiter(max_requests=10, time_window=1)

   @limiter
   async def api_call():
       return "OK"

   # Call 15 times quickly (should fail after 10)
   for i in range(15):
       try:
           await api_call()
           print(f"Request {i+1}: OK")
       except RateLimitExceededError as e:
           print(f"Request {i+1}: {e}")
   ```

#### Rollback Plan

If advanced patterns break:

1. **Disable decorators**:
   - Remove `@breaker`, `@with_retry`, `@limiter` decorators
   - Keep underlying functions

2. **Use simple try/except**:
   ```python
   try:
       result = await api_call()
   except Exception as e:
       logger.error("API call failed", exc_info=True)
   ```

---

### Task 5: Load Testing & Validation (2-3 hours)

#### Overview

Create automated load testing with Locust and performance benchmarking scripts. Document improvements.

#### Step-by-Step Implementation

**Step 5.1: Create Locust Load Test** (90 minutes)

Create `locustfile.py` in project root:

```python
"""
Locust load testing for Market Parser.

Usage:
    locust -f locustfile.py --host=http://127.0.0.1:7860
    locust -f locustfile.py --host=https://your-space.hf.space
"""
from locust import HttpUser, task, between, events
import json
import time


class MarketParserUser(HttpUser):
    """Simulated user for load testing."""

    # Wait 1-3 seconds between tasks
    wait_time = between(1, 3)

    def on_start(self):
        """Called when user starts (setup)."""
        print("User started")

    @task(5)  # Weight: 5 (most common)
    def query_stock_price(self):
        """Query stock price."""
        queries = [
            "What is Tesla stock price?",
            "Show me AAPL current price",
            "NVDA stock quote",
            "Microsoft stock price today",
        ]

        query = self.environment.parsed_options.get_random_query(queries)

        with self.client.post(
            "/api/query",
            json={"query": query},
            catch_response=True,
            name="/api/query [stock_price]"
        ) as response:
            if response.status_code == 200:
                # Verify response contains expected data
                if "price" in response.text.lower():
                    response.success()
                else:
                    response.failure("No price in response")
            else:
                response.failure(f"HTTP {response.status_code}")

    @task(3)  # Weight: 3
    def query_options_chain(self):
        """Query options chain."""
        queries = [
            "Show NVDA call options",
            "TSLA put options expiring next week",
            "AMD options chain",
        ]

        query = self.environment.parsed_options.get_random_query(queries)

        with self.client.post(
            "/api/query",
            json={"query": query},
            catch_response=True,
            name="/api/query [options]"
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"HTTP {response.status_code}")

    @task(2)  # Weight: 2
    def query_technical_analysis(self):
        """Query technical analysis."""
        queries = [
            "AMD technical analysis",
            "Show TSLA support and resistance levels",
            "AAPL RSI indicator",
        ]

        query = self.environment.parsed_options.get_random_query(queries)

        with self.client.post(
            "/api/query",
            json={"query": query},
            catch_response=True,
            name="/api/query [technical_analysis]"
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"HTTP {response.status_code}")

    @task(1)  # Weight: 1 (least common)
    def check_health(self):
        """Check health endpoint."""
        with self.client.get("/health", catch_response=True, name="/health") as response:
            if response.status_code == 200 and response.json().get("status") == "healthy":
                response.success()
            else:
                response.failure("Health check failed")


# Helper function
def get_random_query(queries):
    """Get random query from list."""
    import random
    return random.choice(queries)


# Make it accessible from parsed_options
setattr(events.init, 'get_random_query', staticmethod(get_random_query))
```

**Run load test**:

```bash
# Local testing (10 users, ramp up 2/sec, 2 minutes)
locust -f locustfile.py --host=http://127.0.0.1:7860 \
  --users 10 --spawn-rate 2 --run-time 2m --headless

# Production testing (100 users, ramp up 10/sec, 5 minutes)
locust -f locustfile.py --host=https://your-space.hf.space \
  --users 100 --spawn-rate 10 --run-time 5m --headless

# Interactive UI mode
locust -f locustfile.py --host=http://127.0.0.1:7860
# Open http://localhost:8089
```

**What this does:**
- **Simulated users**: Mimics real user behavior
- **Weighted tasks**: Common queries more frequent
- **Validation**: Checks response content, not just HTTP 200
- **Metrics**: RPS, response times, failures

**Step 5.2: Create Benchmarking Script** (60 minutes)

Create `scripts/benchmark.py`:

```python
"""
Performance benchmarking script.

Usage:
    python scripts/benchmark.py --baseline
    python scripts/benchmark.py --optimized
    python scripts/benchmark.py --compare
"""
import asyncio
import argparse
import time
import statistics
import json
from datetime import datetime
from pathlib import Path


# Benchmark queries
BENCHMARK_QUERIES = [
    "What is Tesla stock price?",
    "Show NVDA call options",
    "AMD technical analysis",
    "AAPL volume trends this week",
    "Microsoft support and resistance levels",
]


async def benchmark_query(query: str, iterations: int = 10):
    """
    Benchmark a single query.

    Args:
        query: Query string
        iterations: Number of iterations

    Returns:
        Dict with statistics
    """
    # Import here to use current implementation
    from src.backend.cli import initialize_persistent_agent, process_query

    agent, session = initialize_persistent_agent()

    times = []
    for i in range(iterations):
        print(f"  Iteration {i+1}/{iterations}...")

        start = time.perf_counter()
        try:
            result = await process_query(agent, session, query)
            elapsed = time.perf_counter() - start
            times.append(elapsed)
        except Exception as e:
            print(f"    Error: {e}")
            continue

    if not times:
        return None

    return {
        'query': query,
        'iterations': len(times),
        'avg': statistics.mean(times),
        'median': statistics.median(times),
        'min': min(times),
        'max': max(times),
        'stdev': statistics.stdev(times) if len(times) > 1 else 0,
    }


async def run_benchmark(label: str = "benchmark"):
    """Run full benchmark suite."""
    print(f"\n{'='*60}")
    print(f"Running Benchmark: {label}")
    print(f"{'='*60}\n")

    results = []

    for query in BENCHMARK_QUERIES:
        print(f"Benchmarking: {query}")
        result = await benchmark_query(query, iterations=10)

        if result:
            results.append(result)
            print(f"  Avg: {result['avg']:.3f}s, Median: {result['median']:.3f}s\n")

    # Overall stats
    all_times = [r['avg'] for r in results]
    overall = {
        'label': label,
        'timestamp': datetime.utcnow().isoformat(),
        'queries_tested': len(results),
        'overall_avg': statistics.mean(all_times),
        'overall_median': statistics.median(all_times),
        'overall_min': min(all_times),
        'overall_max': max(all_times),
        'results': results,
    }

    # Save results
    output_dir = Path("benchmark_results")
    output_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = output_dir / f"{label}_{timestamp}.json"

    with open(output_file, 'w') as f:
        json.dump(overall, f, indent=2)

    print(f"\n{'='*60}")
    print("Benchmark Complete")
    print(f"{'='*60}")
    print(f"Overall Average: {overall['overall_avg']:.3f}s")
    print(f"Overall Median: {overall['overall_median']:.3f}s")
    print(f"Results saved to: {output_file}")

    return overall


def compare_benchmarks(baseline_file: str, optimized_file: str):
    """Compare two benchmark results."""
    with open(baseline_file) as f:
        baseline = json.load(f)

    with open(optimized_file) as f:
        optimized = json.load(f)

    print(f"\n{'='*60}")
    print("Benchmark Comparison")
    print(f"{'='*60}\n")

    print(f"Baseline:  {baseline['label']} ({baseline['timestamp']})")
    print(f"Optimized: {optimized['label']} ({optimized['timestamp']})\n")

    # Overall comparison
    baseline_avg = baseline['overall_avg']
    optimized_avg = optimized['overall_avg']
    improvement = ((baseline_avg - optimized_avg) / baseline_avg) * 100

    print(f"Overall Average:")
    print(f"  Baseline:  {baseline_avg:.3f}s")
    print(f"  Optimized: {optimized_avg:.3f}s")
    print(f"  Improvement: {improvement:+.1f}%\n")

    # Per-query comparison
    print("Per-Query Comparison:")
    print(f"{'Query':<40} {'Baseline':<10} {'Optimized':<10} {'Change':<10}")
    print("-" * 70)

    for b_result, o_result in zip(baseline['results'], optimized['results']):
        query = b_result['query'][:37] + "..." if len(b_result['query']) > 40 else b_result['query']
        b_avg = b_result['avg']
        o_avg = o_result['avg']
        change = ((b_avg - o_avg) / b_avg) * 100

        print(f"{query:<40} {b_avg:>8.3f}s {o_avg:>8.3f}s {change:>8.1f}%")

    print()


def main():
    parser = argparse.ArgumentParser(description="Performance benchmarking")
    parser.add_argument("--baseline", action="store_true", help="Run baseline benchmark")
    parser.add_argument("--optimized", action="store_true", help="Run optimized benchmark")
    parser.add_argument("--compare", nargs=2, metavar=("BASELINE", "OPTIMIZED"),
                        help="Compare two benchmark results")

    args = parser.parse_args()

    if args.baseline:
        asyncio.run(run_benchmark("baseline"))
    elif args.optimized:
        asyncio.run(run_benchmark("optimized"))
    elif args.compare:
        compare_benchmarks(args.compare[0], args.compare[1])
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
```

**Usage**:

```bash
# Run baseline (before optimizations)
python scripts/benchmark.py --baseline

# Apply optimizations (Phases 1-3)...

# Run optimized benchmark
python scripts/benchmark.py --optimized

# Compare results
python scripts/benchmark.py --compare \
  benchmark_results/baseline_20250119_120000.json \
  benchmark_results/optimized_20250119_130000.json
```

#### Success Criteria

- ✅ Locust load test runs successfully
- ✅ Can handle 10+ concurrent users without errors
- ✅ Benchmark script measures performance accurately
- ✅ Comparison shows improvement from optimizations
- ✅ Results saved for historical tracking

#### Testing

1. **Run Locust load test** (local):

   ```bash
   locust -f locustfile.py --host=http://127.0.0.1:7860 \
     --users 10 --spawn-rate 2 --run-time 1m --headless

   # Expected:
   # - 100% success rate (or close)
   # - Avg response time < 5s
   # - No failures or errors
   ```

2. **Run benchmark**:

   ```bash
   # Baseline
   python scripts/benchmark.py --baseline

   # Check output file
   cat benchmark_results/baseline_*.json
   ```

3. **Compare benchmarks** (after implementing Phases 1-3):

   ```bash
   python scripts/benchmark.py --compare \
     benchmark_results/baseline_*.json \
     benchmark_results/optimized_*.json

   # Expected:
   # - 50-80% improvement in avg response time
   # - All queries faster
   ```

#### Rollback Plan

If load testing causes issues:

1. **Stop load test**:
   - Ctrl+C to stop Locust

2. **Reduce load**:
   - Use fewer users (--users 5)
   - Reduce spawn rate (--spawn-rate 1)

3. **Use benchmark script only**:
   - Less aggressive than Locust
   - Sequential queries, not concurrent

---

### Task 6: Production Hardening & Documentation (3-4 hours)

#### Overview

Final production hardening: timeout configuration, graceful shutdown, comprehensive documentation.

#### Step-by-Step Implementation

**Step 6.1: Timeout Configuration** (45 minutes)

Modify `app.py` and `cli.py` to add timeouts:

```python
# cli.py
import asyncio


async def process_query_with_timeout(
    agent: Agent,
    session: Session,
    user_input: str,
    timeout: float = 30.0
):
    """
    Process query with timeout.

    Args:
        agent: Agent instance
        session: Session instance
        user_input: User query
        timeout: Timeout in seconds (default: 30)

    Returns:
        Query result

    Raises:
        asyncio.TimeoutError: If query exceeds timeout
    """
    try:
        result = await asyncio.wait_for(
            process_query(agent, session, user_input),
            timeout=timeout
        )
        return result
    except asyncio.TimeoutError:
        logger.error(
            "Query timeout",
            extra={'user_query': user_input, 'timeout': timeout}
        )
        metrics.increment('queries_timeout')
        raise
```

**What this does:**
- **Query timeout**: Prevents hanging queries
- **Configurable**: Easy to adjust timeout value
- **Logging**: Track timeout events

**Step 6.2: Graceful Shutdown** (60 minutes)

Modify `app.py` to add graceful shutdown:

```python
# app.py
import signal
import sys


def graceful_shutdown(signum, frame):
    """Handle graceful shutdown on SIGTERM/SIGINT."""
    logger.info("Received shutdown signal, cleaning up...")

    # Close database connections, file handles, etc.
    # (Add your cleanup code here)

    # Log final metrics
    final_metrics = metrics.get_all_metrics()
    logger.info("Final metrics", extra={'metrics': final_metrics})

    logger.info("Shutdown complete")
    sys.exit(0)


# Register signal handlers
signal.signal(signal.SIGTERM, graceful_shutdown)
signal.signal(signal.SIGINT, graceful_shutdown)


if __name__ == "__main__":
    logger.info("Market Parser starting...")

    # Start app
    demo.queue(...).launch(...)
```

**What this does:**
- **Clean shutdown**: Responds to SIGTERM/SIGINT
- **Cleanup**: Close resources properly
- **Logging**: Final metrics before exit

**Step 6.3: Create Performance Tuning Guide** (90 minutes)

Create `docs/performance_tuning_guide.md`:

```markdown
# Performance Tuning Guide

## Overview

This guide documents all performance optimizations implemented in Market Parser and provides tuning recommendations for different deployment scenarios.

## Optimization Phases

### Phase 1: Quick Wins (50-70% improvement)
- Gradio queue configuration
- LRU caching for API responses
- Connection pooling

### Phase 2: API Optimization (3-5x faster)
- aiohttp async HTTP
- Request batching
- Rate limiting
- Persistent caching (SQLite/Redis)

### Phase 3: PWA Features (instant UI)
- Service worker caching
- Workbox strategies
- Offline support

### Phase 4: Production Hardening (enterprise-grade)
- Structured logging and monitoring
- Performance dashboard
- Cold start optimization
- Circuit breakers and retry logic
- Load testing and validation

## Configuration Parameters

### Gradio Queue

```python
demo.queue(
    default_concurrency_limit=10,  # Concurrent requests (1-20)
    max_size=100,                  # Queue size (50-200)
).launch(
    max_threads=80,                # Thread pool (40-120)
)
```

**Tuning:**
- **Light load** (< 10 users): concurrency_limit=5, max_threads=40
- **Medium load** (10-50 users): concurrency_limit=10, max_threads=80
- **Heavy load** (50+ users): concurrency_limit=20, max_threads=120

### API Caching

```python
# LRU Cache (in-memory)
@lru_cache(maxsize=1000)  # 500-2000

# Persistent Cache (SQLite/Redis)
cache_ttl = {
    'realtime_price': 60,      # 10-300 seconds
    'historical': 86400,       # 1-7 days
    'options_chain': 30,       # 10-60 seconds
    'company_info': 604800,    # 7-30 days
}
```

**Tuning:**
- **Real-time priority**: Low TTL (10-60s), smaller cache
- **Cost optimization**: High TTL (5-10 min), larger cache
- **Balanced**: Medium TTL (1-3 min), moderate cache

### Rate Limiting

```python
# Polygon: 100 req/s (paid), 5 req/min (free)
polygon_limiter = RateLimiter(max_requests=90, time_window=1)

# Tradier: 120 req/min (default)
tradier_limiter = RateLimiter(max_requests=110, time_window=60)
```

**Tuning:**
- Stay 10-20% below API limits
- Monitor rate limit errors
- Adjust based on usage patterns

### Circuit Breaker

```python
breaker = CircuitBreaker(
    failure_threshold=5,  # 3-10 failures
    timeout=60,           # 30-120 seconds
)
```

**Tuning:**
- **Sensitive**: threshold=3, timeout=30 (fast recovery, more opens)
- **Tolerant**: threshold=10, timeout=120 (slower recovery, fewer opens)
- **Balanced**: threshold=5, timeout=60

## Monitoring

### Key Metrics

- **Response time**: < 3s avg (cached), < 10s (uncached)
- **Success rate**: > 95%
- **Cache hit rate**: > 60%
- **CPU usage**: < 80%
- **Memory usage**: < 500 MB

### Dashboard

Access at `/dashboard`:
- Real-time stats
- Response time trends
- Resource usage
- Error rates

### Alerts

Set alerts for:
- Response time > 10s sustained
- Success rate < 90%
- CPU > 85% sustained
- Memory > 90%

## Troubleshooting

### Slow Queries

1. Check cache hit rate (should be > 60%)
2. Verify API response times (Polygon, Tradier)
3. Check for rate limiting errors
4. Review circuit breaker state

### High Memory Usage

1. Reduce cache size (maxsize in LRU cache)
2. Lower cache TTL (expire data sooner)
3. Check for memory leaks (use /status endpoint)

### High Error Rate

1. Check circuit breaker (may be open)
2. Verify API keys valid
3. Review rate limiting (may be exceeded)
4. Check logs for error patterns

## Load Testing

Run regular load tests:

```bash
# Weekly load test
locust -f locustfile.py --host=https://your-space.hf.space \
  --users 50 --spawn-rate 5 --run-time 10m --headless
```

**Target:**
- RPS: 5-10 requests/sec
- Success rate: > 95%
- P95 response time: < 5s

## Deployment

### HF Spaces

**Free Tier Limits:**
- CPU: 2-core, 16 GB RAM
- Sleeps after inactivity
- No GPU

**Optimizations:**
- Enable keep-alive (GitHub Action)
- Lazy load dependencies
- Optimize cold start (< 10s)

**Upgrade Recommendations:**
- > 50 concurrent users: Upgrade to CPU Upgrade tier
- Real-time quotes needed: Consider dedicated hosting

## Benchmarking

Run benchmarks before/after changes:

```bash
python scripts/benchmark.py --baseline
# Apply changes...
python scripts/benchmark.py --optimized
python scripts/benchmark.py --compare baseline.json optimized.json
```

## Best Practices

1. **Cache aggressively**: Most queries repeat
2. **Monitor constantly**: Dashboard + logs
3. **Test regularly**: Weekly load tests
4. **Tune incrementally**: Small changes, measure impact
5. **Document changes**: Update this guide

## References

- Gradio Performance Guide
- Python asyncio Best Practices
- Polygon API Documentation
- HF Spaces Documentation
```

**Step 6.4: Create Monitoring Playbook** (60 minutes)

Create `docs/monitoring_playbook.md`:

```markdown
# Monitoring Playbook

## Overview

Operational playbook for monitoring and responding to Market Parser issues.

## Monitoring Endpoints

### /health
**Purpose**: Keep-alive and basic health check
**Response**: `{"status": "healthy"}`
**When to use**: External monitors (UptimeRobot, GitHub Actions)

### /status
**Purpose**: Detailed system status and resources
**Response**: Process info, system resources, metrics summary
**When to use**: Troubleshooting, capacity planning

### /metrics
**Purpose**: Full performance metrics
**Response**: Counters, gauges, histograms
**When to use**: Performance analysis, dashboards

### /dashboard
**Purpose**: Visual monitoring interface
**Response**: HTML dashboard with live charts
**When to use**: Real-time monitoring, demos

## Alert Scenarios

### High Response Time

**Trigger**: Avg response time > 10s for 5 minutes

**Symptoms:**
- Dashboard shows increasing response times
- Users reporting slow queries
- `/status` shows high CPU or memory

**Investigation:**
1. Check cache hit rate (< 60% is low)
2. Review recent queries (any new patterns?)
3. Check API response times (Polygon, Tradier down?)
4. Verify rate limiting not exceeded

**Resolution:**
- Clear cache if stale: `metrics.reset()`
- Restart if needed: HF Spaces will auto-restart
- Check API status pages
- Increase cache TTL if appropriate

### High Error Rate

**Trigger**: Error rate > 10% for 5 minutes

**Symptoms:**
- Dashboard shows increasing errors
- Logs show repeated exceptions
- `/status` shows high failed_queries count

**Investigation:**
1. Check logs for error patterns
2. Verify circuit breaker state (may be open)
3. Check API keys valid
4. Review rate limiting

**Resolution:**
- If circuit breaker open: Wait for timeout, may recover automatically
- If API key invalid: Update environment variable, restart
- If rate limit exceeded: Reduce query frequency or upgrade API tier

### High CPU Usage

**Trigger**: CPU > 85% sustained for 10 minutes

**Symptoms:**
- Dashboard shows high CPU %
- App feels sluggish
- `/status` shows cpu_percent > 85

**Investigation:**
1. Check concurrent request count
2. Review recent load (traffic spike?)
3. Check for infinite loops (logs show repeated errors?)

**Resolution:**
- Reduce `concurrency_limit` temporarily
- Restart if CPU doesn't recover
- Scale up to CPU Upgrade tier if sustained

### High Memory Usage

**Trigger**: Memory > 90%

**Symptoms:**
- Dashboard shows high memory MB
- App may crash with OOM
- `/status` shows memory_percent > 90

**Investigation:**
1. Check cache size (`metrics.get_all_metrics()`)
2. Review memory leaks (memory increasing over time?)
3. Check for large query results

**Resolution:**
- Reduce cache size (maxsize)
- Restart to clear memory
- Investigate memory leaks if recurring

### Service Unavailable

**Trigger**: /health returns non-200 or timeout

**Symptoms:**
- App not responding
- HF Space shows error
- Keep-alive pings failing

**Investigation:**
1. Check HF Spaces status
2. Review recent deployments (new code?)
3. Check logs for startup errors

**Resolution:**
- HF Spaces will auto-restart (wait 2-3 minutes)
- If persists, check build logs
- Revert deployment if needed

## Daily Monitoring

### Morning Check (5 minutes)

1. Open `/dashboard`
2. Verify status is "Healthy"
3. Check uptime (should be > 23 hours if keep-alive working)
4. Review success rate (should be > 95%)
5. Check response times (< 5s avg)

### Weekly Review (30 minutes)

1. Run load test: `locust ...`
2. Review week's metrics (trends, patterns)
3. Check for errors (any new error types?)
4. Review cache hit rate (> 60%?)
5. Update tuning if needed

## Escalation

### User Reports Issue

1. Acknowledge receipt
2. Check `/status` and `/dashboard`
3. Review logs for user's correlation_id
4. Investigate and resolve
5. Follow up with user

### Critical Issue (App Down)

1. Check HF Spaces status
2. Review build/deployment logs
3. Restart if needed (HF auto-restarts)
4. Notify users if downtime > 5 minutes
5. Post-mortem after resolution

## Tools

- **Dashboard**: http://your-space.hf.space/dashboard
- **Logs**: HF Spaces logs viewer
- **Load Test**: `locust -f locustfile.py`
- **Benchmark**: `python scripts/benchmark.py`

## Contacts

- **HF Spaces Support**: https://huggingface.co/support
- **Polygon Support**: https://polygon.io/support
- **Tradier Support**: https://tradier.com/support

## Changelog

Track all monitoring-related changes here:
- 2025-01-19: Initial playbook created
```

#### Success Criteria

- ✅ Timeout configuration working (queries timeout after 30s)
- ✅ Graceful shutdown working (SIGTERM handled)
- ✅ Performance tuning guide complete
- ✅ Monitoring playbook complete
- ✅ All documentation up-to-date

#### Testing

1. **Test timeout**:

   ```python
   import asyncio

   # Query that takes too long
   result = await process_query_with_timeout(agent, session, "complex query", timeout=5)
   # Should timeout after 5 seconds
   ```

2. **Test graceful shutdown**:

   ```bash
   # Start app
   python app.py &
   PID=$!

   # Send SIGTERM
   kill -TERM $PID

   # Check logs for "Shutdown complete"
   ```

3. **Verify documentation**:
   - Read performance_tuning_guide.md
   - Read monitoring_playbook.md
   - Check for clarity and completeness

#### Rollback Plan

If production hardening causes issues:

1. **Remove timeouts**:
   - Use original `process_query` without timeout wrapper

2. **Remove shutdown handler**:
   - Comment out signal handlers

3. **Documentation**:
   - Keep documentation even if code rolled back

---

## Final Testing and Validation

### Pre-Deployment Checklist

- [ ] All 6 tasks completed
- [ ] Structured logging working (JSON format, correlation IDs)
- [ ] Metrics collecting (counters, gauges, histograms)
- [ ] Dashboard accessible at `/dashboard`
- [ ] `/metrics`, `/status`, `/health` endpoints working
- [ ] Cold start optimized (30-50% faster)
- [ ] Keep-alive service running (GitHub Action)
- [ ] Circuit breakers working
- [ ] Retry logic working
- [ ] Rate limiting working
- [ ] Load test passes (95%+ success rate)
- [ ] Benchmark shows improvement
- [ ] Timeout configuration working
- [ ] Graceful shutdown working
- [ ] Documentation complete

### Deployment Steps

1. **Commit all changes**:

   ```bash
   git add .
   git commit -m "[PHASE 4] Production hardening: Logging, monitoring, dashboard, load testing"
   git push
   ```

2. **Monitor HF Spaces build**

3. **Verify deployment**:

   ```bash
   # Check health
   curl https://your-space.hf.space/health

   # Check status
   curl https://your-space.hf.space/status | jq

   # Open dashboard
   open https://your-space.hf.space/dashboard
   ```

4. **Run load test**:

   ```bash
   locust -f locustfile.py --host=https://your-space.hf.space \
     --users 20 --spawn-rate 5 --run-time 5m --headless
   ```

5. **Monitor for 24 hours**:
   - Check dashboard regularly
   - Review logs for errors
   - Verify keep-alive working

### Post-Deployment Validation

1. **Run benchmark comparison**:

   ```bash
   python scripts/benchmark.py --compare \
     benchmark_results/baseline_*.json \
     benchmark_results/phase4_*.json
   ```

2. **Verify metrics**:
   - Uptime > 24 hours (with keep-alive)
   - Success rate > 95%
   - Avg response time < 3s (cached)
   - CPU < 50%
   - Memory < 300 MB

---

## Success Metrics

### Quantitative Metrics

**Performance:**
- [ ] Sustained 10-20 concurrent users
- [ ] 95% of queries < 3s (with caching)
- [ ] 99% of queries < 10s (uncached)
- [ ] Zero cold starts during business hours

**Monitoring:**
- [ ] Dashboard updates every 10s
- [ ] All metrics accurate
- [ ] Logs structured and searchable
- [ ] Correlation IDs in all requests

**Reliability:**
- [ ] 99.9% uptime (with circuit breakers)
- [ ] < 5% error rate
- [ ] Automatic recovery from API failures
- [ ] Graceful degradation under load

**Production Readiness:**
- [ ] Load test passes (100 users, 95% success)
- [ ] Documentation complete
- [ ] Monitoring playbook ready
- [ ] Performance tuning guide ready

### Qualitative Metrics

**Developer Experience:**
- [ ] Easy to debug (correlation IDs, structured logs)
- [ ] Easy to monitor (dashboard, endpoints)
- [ ] Easy to tune (documented parameters)
- [ ] Easy to operate (playbook, guides)

**User Experience:**
- [ ] Fast responses (< 3s perceived)
- [ ] High reliability (> 95% success)
- [ ] Transparent status (dashboard visible)
- [ ] Consistent performance

---

## Conclusion

Phase 4 completes the transformation of Market Parser into a production-ready, enterprise-grade application with:

- ✅ **Production Logging**: Structured JSON logging with correlation IDs
- ✅ **Performance Dashboard**: Real-time monitoring with live charts
- ✅ **Cold Start Optimization**: Zero cold starts during business hours
- ✅ **Advanced Async Patterns**: Circuit breakers, retry logic, rate limiting
- ✅ **Load Testing**: Automated performance validation
- ✅ **Production Hardening**: Timeouts, graceful shutdown, comprehensive docs

**Cumulative Impact (All 4 Phases):**
- **10-20x capacity**: Concurrent user handling
- **5-10x faster**: Response times (with caching)
- **50-80% cost reduction**: API call reduction
- **99.9% uptime**: With all resilience patterns
- **Enterprise-grade**: Monitoring, logging, documentation

**Next Steps:**
- Implement Phase 4 tasks sequentially
- Test thoroughly after each task
- Monitor dashboard and metrics
- Update documentation as needed
- Collect user feedback and iterate

---

**Phase 4 Plan Created**: 2025-10-19
**Status**: Ready for implementation
**Prerequisites**: Phase 1, Phase 2, Phase 3 completed (highly recommended)
**Risk Level**: MEDIUM-LOW (mostly additive, minimal breaking changes)
**Support**: Reference this document during implementation
