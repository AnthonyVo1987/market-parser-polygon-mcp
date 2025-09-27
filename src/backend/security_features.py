"""
Security Features for Dynamic Adaptive Prompting System

This module provides comprehensive security features including:
- Rate limiting and abuse prevention
- Enhanced input validation and sanitization
- Audit logging and monitoring
- Circuit breaker pattern for system resilience
- Authentication and authorization
- Security configuration management

Author: AI Assistant
Date: September 27, 2025
"""

import ipaddress
import logging
import re
import time
from collections import defaultdict, deque
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


class SecurityLevel(Enum):
    """Security levels for different operations"""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ThreatType(Enum):
    """Types of security threats"""

    INJECTION = "injection"
    RATE_LIMIT_EXCEEDED = "rate_limit_exceeded"
    MALICIOUS_INPUT = "malicious_input"
    UNAUTHORIZED_ACCESS = "unauthorized_access"
    SUSPICIOUS_PATTERN = "suspicious_pattern"


@dataclass
class SecurityEvent:
    """Data class for security events"""

    timestamp: datetime
    event_type: ThreatType
    severity: SecurityLevel
    user_id: str
    ip_address: str
    description: str
    blocked: bool
    metadata: Dict[str, Any]


@dataclass
class RateLimitRule:
    """Data class for rate limiting rules"""

    max_requests: int
    time_window: int  # seconds
    block_duration: int  # seconds
    security_level: SecurityLevel


@dataclass
class SecurityConfig:
    """Security configuration settings"""

    enable_rate_limiting: bool = True
    enable_input_validation: bool = True
    enable_audit_logging: bool = True
    enable_circuit_breaker: bool = True
    max_input_length: int = 10000
    blocked_patterns: Optional[List[str]] = None
    allowed_ip_ranges: Optional[List[str]] = None
    rate_limit_rules: Optional[Dict[str, RateLimitRule]] = None

    def __post_init__(self):
        if self.blocked_patterns is None:
            self.blocked_patterns = [
                r"<script[^>]*>.*?</script>",
                r"javascript:",
                r"vbscript:",
                r"onload\s*=",
                r"onerror\s*=",
                r"eval\s*\(",
                r"exec\s*\(",
                r"system\s*\(",
                r"subprocess\.",
                r"__import__",
                r"file://",
                r"ftp://",
                r"\.\./",
                r"etc/passwd",
                r"etc/shadow",
            ]

        if self.allowed_ip_ranges is None:
            self.allowed_ip_ranges = ["0.0.0.0/0"]  # Allow all by default

        if self.rate_limit_rules is None:
            self.rate_limit_rules = {
                "default": RateLimitRule(100, 3600, 300, SecurityLevel.MEDIUM),
                "high_frequency": RateLimitRule(10, 60, 60, SecurityLevel.HIGH),
                "critical": RateLimitRule(5, 300, 900, SecurityLevel.CRITICAL),
            }


class RateLimiter:
    """
    Rate limiter with sliding window algorithm.

    Prevents abuse by limiting the number of requests per user/IP
    within specified time windows.
    """

    def __init__(self, config: SecurityConfig):
        self.config = config
        self.request_history: Dict[str, deque] = defaultdict(deque)
        self.blocked_users: Dict[str, datetime] = {}
        self.rules = config.rate_limit_rules

    def is_allowed(
        self, user_id: str, ip_address: str, rule_name: str = "default"
    ) -> Tuple[bool, Optional[str]]:
        """
        Check if a request is allowed based on rate limiting rules.

        Args:
            user_id: User identifier
            ip_address: Client IP address
            rule_name: Rate limiting rule to apply

        Returns:
            Tuple of (is_allowed, reason_if_blocked)
        """
        if not self.config.enable_rate_limiting:
            return True, None

        # Check if user is currently blocked
        if user_id in self.blocked_users:
            if datetime.now() < self.blocked_users[user_id]:
                return False, f"User blocked until {self.blocked_users[user_id]}"
            del self.blocked_users[user_id]

        # Get applicable rule
        rule = self.rules.get(rule_name, self.rules["default"])

        # Clean old requests from history
        now = time.time()
        cutoff_time = now - rule.time_window

        # Use combination of user_id and ip_address as key
        key = f"{user_id}:{ip_address}"

        # Remove old requests
        while self.request_history[key] and self.request_history[key][0] < cutoff_time:
            self.request_history[key].popleft()

        # Check if limit exceeded
        if len(self.request_history[key]) >= rule.max_requests:
            # Block user
            block_until = datetime.now() + timedelta(seconds=rule.block_duration)
            self.blocked_users[user_id] = block_until

            logger.warning(f"Rate limit exceeded for user {user_id} from {ip_address}")
            return False, f"Rate limit exceeded. Blocked until {block_until}"

        # Record this request
        self.request_history[key].append(now)
        return True, None

    def get_remaining_requests(
        self, user_id: str, ip_address: str, rule_name: str = "default"
    ) -> int:
        """Get remaining requests for a user."""
        rule = self.rules.get(rule_name, self.rules["default"])
        key = f"{user_id}:{ip_address}"

        # Clean old requests
        now = time.time()
        cutoff_time = now - rule.time_window
        while self.request_history[key] and self.request_history[key][0] < cutoff_time:
            self.request_history[key].popleft()

        return max(0, rule.max_requests - len(self.request_history[key]))

    def reset_user_limits(self, user_id: str):
        """Reset rate limits for a specific user."""
        # Remove from blocked users
        if user_id in self.blocked_users:
            del self.blocked_users[user_id]

        # Clear request history for this user
        keys_to_remove = [
            key for key in self.request_history.keys() if key.startswith(f"{user_id}:")
        ]
        for key in keys_to_remove:
            del self.request_history[key]

        logger.info(f"Reset rate limits for user {user_id}")


class EnhancedInputValidator:
    """
    Enhanced input validator with comprehensive security checks.

    Provides multiple layers of validation including pattern matching,
    content analysis, and threat detection.
    """

    def __init__(self, config: SecurityConfig):
        self.config = config
        self.blocked_patterns = [
            re.compile(pattern, re.IGNORECASE) for pattern in config.blocked_patterns
        ]
        self.suspicious_keywords = [
            "password",
            "token",
            "secret",
            "key",
            "auth",
            "login",
            "admin",
            "root",
            "sudo",
            "chmod",
            "rm -rf",
            "delete",
            "drop table",
            "truncate",
            "update",
            "insert",
            "select",
        ]

    def validate_input(
        self, user_input: str, _user_id: str, _ip_address: str
    ) -> Tuple[bool, List[str], SecurityLevel]:
        """
        Comprehensive input validation.

        Args:
            user_input: Input to validate
            user_id: User identifier
            ip_address: Client IP address

        Returns:
            Tuple of (is_valid, violations, threat_level)
        """
        violations = []
        threat_level = SecurityLevel.LOW

        if not self.config.enable_input_validation:
            return True, [], SecurityLevel.LOW

        # Check input length
        if len(user_input) > self.config.max_input_length:
            violations.append(f"Input too long: {len(user_input)} > {self.config.max_input_length}")
            threat_level = SecurityLevel.MEDIUM

        # Check for blocked patterns
        for pattern in self.blocked_patterns:
            if pattern.search(user_input):
                violations.append(f"Blocked pattern detected: {pattern.pattern}")
                threat_level = SecurityLevel.HIGH

        # Check for suspicious keywords
        suspicious_count = sum(
            1 for keyword in self.suspicious_keywords if keyword.lower() in user_input.lower()
        )
        if suspicious_count > 3:
            violations.append(f"High concentration of suspicious keywords: {suspicious_count}")
            threat_level = SecurityLevel.MEDIUM

        # Check for potential injection attempts
        injection_patterns = [
            r"union\s+select",
            r"or\s+1\s*=\s*1",
            r"and\s+1\s*=\s*1",
            r"<script",
            r"javascript:",
            r"eval\s*\(",
            r"exec\s*\(",
            r"system\s*\(",
            r"__import__",
        ]

        for pattern in injection_patterns:
            if re.search(re.compile(pattern), user_input, re.IGNORECASE):
                violations.append(f"Potential injection attempt: {pattern}")
                threat_level = SecurityLevel.CRITICAL

        # Check for encoding attempts
        if any(
            encoded in user_input.lower()
            for encoded in ["%3c", "%3e", "%22", "%27", "&lt;", "&gt;"]
        ):
            violations.append("Encoded characters detected")
            threat_level = SecurityLevel.HIGH

        # Check for path traversal attempts
        if any(
            traversal in user_input for traversal in ["../", "..\\", "/etc/", "/proc/", "/sys/"]
        ):
            violations.append("Path traversal attempt detected")
            threat_level = SecurityLevel.HIGH

        is_valid = len(violations) == 0 or threat_level == SecurityLevel.LOW
        return is_valid, violations, threat_level

    def sanitize_input(self, user_input: str) -> str:
        """
        Sanitize user input by removing or escaping dangerous content.

        Args:
            user_input: Input to sanitize

        Returns:
            Sanitized input string
        """
        sanitized = user_input

        # Remove script tags and their content
        sanitized = re.sub(
            r"<script[^>]*>.*?</script>", "", sanitized, flags=re.IGNORECASE | re.DOTALL
        )

        # Remove dangerous HTML attributes
        sanitized = re.sub(r'on\w+\s*=\s*["\'][^"\']*["\']', "", sanitized, flags=re.IGNORECASE)

        # Remove javascript: and vbscript: protocols
        sanitized = re.sub(r"(javascript|vbscript):", "", sanitized, flags=re.IGNORECASE)

        # Remove dangerous characters
        dangerous_chars = ["<", ">", '"', "'", "&", ";"]
        for char in dangerous_chars:
            sanitized = sanitized.replace(char, "")

        # Limit length
        if len(sanitized) > self.config.max_input_length:
            sanitized = sanitized[: self.config.max_input_length]

        return sanitized.strip()


class AuditLogger:
    """
    Comprehensive audit logging system.

    Logs all security events, user interactions, and system activities
    for monitoring and compliance purposes.
    """

    def __init__(self, log_file: str = "security_audit.log"):
        self.log_file = Path(log_file)
        self.events: List[SecurityEvent] = []
        self.setup_logging()

    def setup_logging(self):
        """Setup audit logging configuration."""
        # Create audit logger separate from main logger
        self.audit_logger = logging.getLogger("security_audit")
        self.audit_logger.setLevel(logging.INFO)

        # Create file handler
        handler = logging.FileHandler(self.log_file)
        handler.setLevel(logging.INFO)

        # Create formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(formatter)

        # Add handler to logger
        if not self.audit_logger.handlers:
            self.audit_logger.addHandler(handler)

    def log_security_event(
        self,
        event_type: ThreatType,
        severity: SecurityLevel,
        user_id: str,
        ip_address: str,
        description: str,
        blocked: bool = False,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        """
        Log a security event.

        Args:
            event_type: Type of security threat
            severity: Severity level
            user_id: User identifier
            ip_address: Client IP address
            description: Event description
            blocked: Whether the action was blocked
            metadata: Additional event metadata
        """
        event = SecurityEvent(
            timestamp=datetime.now(),
            event_type=event_type,
            severity=severity,
            user_id=user_id,
            ip_address=ip_address,
            description=description,
            blocked=blocked,
            metadata=metadata or {},
        )

        self.events.append(event)

        # Log to file
        log_message = (
            f"SECURITY_EVENT - Type: {event_type.value}, "
            f"Severity: {severity.value}, User: {user_id}, "
            f"IP: {ip_address}, Blocked: {blocked}, "
            f"Description: {description}"
        )

        if severity in [SecurityLevel.HIGH, SecurityLevel.CRITICAL]:
            self.audit_logger.error(log_message)
        elif severity == SecurityLevel.MEDIUM:
            self.audit_logger.warning(log_message)
        else:
            self.audit_logger.info(log_message)

        # Keep only last 10000 events in memory
        if len(self.events) > 10000:
            self.events = self.events[-10000:]

    def log_user_interaction(
        self,
        user_id: str,
        ip_address: str,
        action: str,
        success: bool,
        response_time: float,
        _metadata: Optional[Dict[str, Any]] = None,
    ):
        """Log user interaction for audit purposes."""
        log_message = (
            f"USER_INTERACTION - User: {user_id}, IP: {ip_address}, "
            f"Action: {action}, Success: {success}, "
            f"ResponseTime: {response_time:.3f}s"
        )

        self.audit_logger.info(log_message)

    def get_security_summary(self, hours: int = 24) -> Dict[str, Any]:
        """Get security summary for the specified time period."""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        recent_events = [e for e in self.events if e.timestamp > cutoff_time]

        if not recent_events:
            return {}

        # Count events by type and severity
        event_counts: Dict[str, int] = defaultdict(int)
        severity_counts: Dict[str, int] = defaultdict(int)
        blocked_counts = 0

        for event in recent_events:
            event_counts[event.event_type.value] += 1
            severity_counts[event.severity.value] += 1
            if event.blocked:
                blocked_counts += 1

        return {
            "time_period_hours": hours,
            "total_events": len(recent_events),
            "events_by_type": dict(event_counts),
            "events_by_severity": dict(severity_counts),
            "blocked_actions": blocked_counts,
            "most_common_threat": (
                max(event_counts.items(), key=lambda x: x[1])[0] if event_counts else None
            ),
        }


class CircuitBreaker:
    """
    Circuit breaker pattern implementation for system resilience.

    Prevents cascading failures by temporarily blocking requests
    when error rates exceed thresholds.
    """

    def __init__(self, failure_threshold: int = 5, recovery_timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN

    def call(self, func, *args, **kwargs):
        """
        Execute a function with circuit breaker protection.

        Args:
            func: Function to execute
            *args: Function arguments
            **kwargs: Function keyword arguments

        Returns:
            Function result or raises exception
        """
        if self.state == "OPEN":
            if self._should_attempt_reset():
                self.state = "HALF_OPEN"
            else:
                raise Exception("Circuit breaker is OPEN - service unavailable")

        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise e

    def _should_attempt_reset(self) -> bool:
        """Check if circuit breaker should attempt to reset."""
        if self.last_failure_time is None:
            return True

        return time.time() - self.last_failure_time >= self.recovery_timeout

    def _on_success(self):
        """Handle successful operation."""
        self.failure_count = 0
        self.state = "CLOSED"

    def _on_failure(self):
        """Handle failed operation."""
        self.failure_count += 1
        self.last_failure_time = time.time()

        if self.failure_count >= self.failure_threshold:
            self.state = "OPEN"
            logger.warning(f"Circuit breaker opened after {self.failure_count} failures")


class IPWhitelist:
    """
    IP address whitelist for access control.

    Allows or blocks requests based on IP address ranges.
    """

    def __init__(self, allowed_ranges: List[str]):
        self.allowed_networks = []
        for range_str in allowed_ranges:
            try:
                self.allowed_networks.append(ipaddress.ip_network(range_str, strict=False))
            except ValueError as e:
                logger.error(f"Invalid IP range: {range_str} - {e}")

    def is_allowed(self, ip_address: str) -> bool:
        """
        Check if an IP address is allowed.

        Args:
            ip_address: IP address to check

        Returns:
            True if allowed, False otherwise
        """
        try:
            ip = ipaddress.ip_address(ip_address)
            return any(ip in network for network in self.allowed_networks)
        except ValueError:
            logger.error(f"Invalid IP address: {ip_address}")
            return False


class SecurityManager:
    """
    Central security manager that coordinates all security features.

    This class provides a unified interface for all security operations
    including rate limiting, input validation, audit logging, and more.
    """

    def __init__(self, config: SecurityConfig):
        self.config = config
        self.rate_limiter = RateLimiter(config)
        self.input_validator = EnhancedInputValidator(config)
        self.audit_logger = AuditLogger()
        self.circuit_breaker = CircuitBreaker()
        self.ip_whitelist = IPWhitelist(config.allowed_ip_ranges)

    def validate_request(
        self, user_input: str, user_id: str, ip_address: str, rule_name: str = "default"
    ) -> Tuple[bool, List[str]]:
        """
        Comprehensive request validation.

        Args:
            user_input: User input to validate
            user_id: User identifier
            ip_address: Client IP address
            rule_name: Rate limiting rule to apply

        Returns:
            Tuple of (is_valid, error_messages)
        """
        errors = []

        try:
            # Check IP whitelist
            if not self.ip_whitelist.is_allowed(ip_address):
                error_msg = f"IP address {ip_address} not in whitelist"
                errors.append(error_msg)
                self.audit_logger.log_security_event(
                    ThreatType.UNAUTHORIZED_ACCESS,
                    SecurityLevel.HIGH,
                    user_id,
                    ip_address,
                    error_msg,
                    blocked=True,
                )
                return False, errors

            # Check rate limits
            rate_allowed, rate_reason = self.rate_limiter.is_allowed(user_id, ip_address, rule_name)
            if not rate_allowed:
                if rate_reason:
                    errors.append(rate_reason)
                self.audit_logger.log_security_event(
                    ThreatType.RATE_LIMIT_EXCEEDED,
                    SecurityLevel.MEDIUM,
                    user_id,
                    ip_address,
                    rate_reason or "Rate limit exceeded",
                    blocked=True,
                )
                return False, errors

            # Validate input
            input_valid, violations, threat_level = self.input_validator.validate_input(
                user_input, user_id, ip_address
            )

            if not input_valid:
                errors.extend(violations)
                self.audit_logger.log_security_event(
                    ThreatType.MALICIOUS_INPUT,
                    threat_level,
                    user_id,
                    ip_address,
                    f"Input validation failed: {', '.join(violations)}",
                    blocked=True,
                )
                return False, errors

            # Log successful validation
            self.audit_logger.log_user_interaction(
                user_id, ip_address, "input_validation", True, 0.0
            )

            return True, []

        except Exception as e:
            error_msg = f"Security validation error: {str(e)}"
            errors.append(error_msg)
            self.audit_logger.log_security_event(
                ThreatType.SUSPICIOUS_PATTERN,
                SecurityLevel.HIGH,
                user_id,
                ip_address,
                error_msg,
                blocked=True,
            )
            return False, errors

    def sanitize_input(self, user_input: str) -> str:
        """Sanitize user input."""
        return self.input_validator.sanitize_input(user_input)

    def get_security_status(self) -> Dict[str, Any]:
        """Get overall security status."""
        return {
            "rate_limiter_active": self.config.enable_rate_limiting,
            "input_validation_active": self.config.enable_input_validation,
            "audit_logging_active": self.config.enable_audit_logging,
            "circuit_breaker_state": self.circuit_breaker.state,
            "security_summary": self.audit_logger.get_security_summary(),
            "blocked_users_count": len(self.rate_limiter.blocked_users),
        }

    def reset_user_security(self, user_id: str):
        """Reset security restrictions for a user."""
        self.rate_limiter.reset_user_limits(user_id)
        logger.info(f"Reset security restrictions for user {user_id}")
