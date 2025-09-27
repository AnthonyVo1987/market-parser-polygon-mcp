"""
Secure Dynamic Prompt Manager

This module provides a secure implementation of the dynamic prompting system
that integrates all security features including rate limiting, input validation,
audit logging, and system resilience.

Author: AI Assistant
Date: September 27, 2025
"""

import logging
import time
from typing import Any, Dict, Optional

from .dynamic_prompts import DynamicPromptManager, UserPreferences
from .advanced_prompting_features import AdvancedPromptManager
from .security_features import SecurityManager, SecurityConfig, SecurityLevel, ThreatType

logger = logging.getLogger(__name__)


class SecureDynamicPromptManager(AdvancedPromptManager):
    """
    Secure implementation of the dynamic prompt manager.
    
    This class extends the AdvancedPromptManager with comprehensive
    security features including input validation, rate limiting,
    audit logging, and threat detection.
    """
    
    def __init__(self, base_template: str, config: Dict[str, Any], security_config: SecurityConfig = None):
        super().__init__(base_template, config)
        
        # Initialize security configuration
        if security_config is None:
            security_config = SecurityConfig()
        
        self.security_manager = SecurityManager(security_config)
        self.security_config = security_config
        
        logger.info("SecureDynamicPromptManager initialized with security features enabled")
    
    def generate_prompt(self, user_input: str, context: Dict[str, Any], 
                       user_id: str = "anonymous", ip_address: str = "127.0.0.1",
                       rule_name: str = 'default') -> Dict[str, Any]:
        """
        Generate a secure customized prompt with comprehensive validation.
        
        Args:
            user_input: The user's input message
            context: Additional context for prompt generation
            user_id: User identifier for security tracking
            ip_address: Client IP address for security validation
            rule_name: Rate limiting rule to apply
            
        Returns:
            Dictionary containing prompt and security information
        """
        start_time = time.time()
        
        # Initialize response structure
        response = {
            'success': False,
            'prompt': '',
            'security_info': {
                'validated': False,
                'sanitized': False,
                'threats_detected': [],
                'rate_limited': False
            },
            'errors': [],
            'metadata': {
                'user_id': user_id,
                'ip_address': ip_address,
                'timestamp': time.time(),
                'processing_time': 0.0
            }
        }
        
        try:
            # Step 1: Security validation
            is_valid, security_errors = self.security_manager.validate_request(
                user_input, user_id, ip_address, rule_name
            )
            
            if not is_valid:
                response['errors'] = security_errors
                response['security_info']['rate_limited'] = any('rate limit' in error.lower() for error in security_errors)
                response['security_info']['threats_detected'] = security_errors
                
                # Log security violation
                self.security_manager.audit_logger.log_security_event(
                    ThreatType.MALICIOUS_INPUT,
                    SecurityLevel.HIGH,
                    user_id,
                    ip_address,
                    f"Request blocked: {', '.join(security_errors)}",
                    blocked=True,
                    metadata={'user_input_length': len(user_input)}
                )
                
                return response
            
            response['security_info']['validated'] = True
            
            # Step 2: Input sanitization
            sanitized_input = self.security_manager.sanitize_input(user_input)
            response['security_info']['sanitized'] = sanitized_input != user_input
            
            # Step 3: Generate prompt using circuit breaker
            def generate_prompt_internal():
                # Parse user instructions from sanitized input
                preferences = self.parse_user_instructions(sanitized_input)
                
                # Validate preferences
                self.validator.validate_preferences(preferences)
                
                # Check for custom template
                custom_template = self._get_custom_template(sanitized_input, preferences)
                if custom_template:
                    template = custom_template
                else:
                    template = self.base_template
                
                # Apply customizations to template
                customized_prompt = self.template_engine.apply_preferences(
                    template, preferences, context
                )
                
                # Cache result for performance
                cache_key = self._generate_cache_key(sanitized_input, context)
                self.cache.store(cache_key, customized_prompt)
                
                return customized_prompt, preferences
            
            # Execute with circuit breaker protection
            prompt, preferences = self.security_manager.circuit_breaker.call(generate_prompt_internal)
            
            response['prompt'] = prompt
            response['success'] = True
            
            # Step 4: Record successful interaction
            processing_time = time.time() - start_time
            response['metadata']['processing_time'] = processing_time
            
            self.learning_system.record_user_interaction(
                user_id, preferences, processing_time, True
            )
            
            self.security_manager.audit_logger.log_user_interaction(
                user_id, ip_address, "generate_prompt", True, processing_time,
                metadata={
                    'input_length': len(user_input),
                    'sanitized': response['security_info']['sanitized'],
                    'preferences': preferences.__dict__ if preferences else {}
                }
            )
            
            logger.info(f"Successfully generated secure prompt for user {user_id}")
            
        except Exception as e:
            # Handle errors securely
            processing_time = time.time() - start_time
            error_message = f"Prompt generation failed: {str(e)}"
            
            response['errors'].append(error_message)
            response['metadata']['processing_time'] = processing_time
            
            # Log error
            self.security_manager.audit_logger.log_security_event(
                ThreatType.SUSPICIOUS_PATTERN,
                SecurityLevel.MEDIUM,
                user_id,
                ip_address,
                error_message,
                blocked=False,
                metadata={'exception_type': type(e).__name__}
            )
            
            self.learning_system.record_user_interaction(
                user_id, UserPreferences(), processing_time, False
            )
            
            logger.error(f"Error generating prompt for user {user_id}: {e}")
        
        return response
    
    def get_user_security_status(self, user_id: str, ip_address: str) -> Dict[str, Any]:
        """
        Get security status for a specific user.
        
        Args:
            user_id: User identifier
            ip_address: Client IP address
            
        Returns:
            Dictionary with user security information
        """
        remaining_requests = self.security_manager.rate_limiter.get_remaining_requests(
            user_id, ip_address
        )
        
        is_blocked = user_id in self.security_manager.rate_limiter.blocked_users
        block_expires = None
        if is_blocked:
            block_expires = self.security_manager.rate_limiter.blocked_users[user_id]
        
        return {
            'user_id': user_id,
            'ip_address': ip_address,
            'remaining_requests': remaining_requests,
            'is_blocked': is_blocked,
            'block_expires': block_expires.isoformat() if block_expires else None,
            'ip_whitelisted': self.security_manager.ip_whitelist.is_allowed(ip_address)
        }
    
    def get_system_security_status(self) -> Dict[str, Any]:
        """Get comprehensive system security status."""
        base_status = self.security_manager.get_security_status()
        
        # Add additional system information
        base_status.update({
            'total_users_tracked': len(self.learning_system.user_analytics),
            'circuit_breaker_failures': self.security_manager.circuit_breaker.failure_count,
            'security_config': {
                'rate_limiting_enabled': self.security_config.enable_rate_limiting,
                'input_validation_enabled': self.security_config.enable_input_validation,
                'audit_logging_enabled': self.security_config.enable_audit_logging,
                'circuit_breaker_enabled': self.security_config.enable_circuit_breaker,
                'max_input_length': self.security_config.max_input_length
            }
        })
        
        return base_status
    
    def reset_user_security(self, user_id: str, admin_user_id: str, reason: str = ""):
        """
        Reset security restrictions for a user (admin function).
        
        Args:
            user_id: User to reset restrictions for
            admin_user_id: Administrator performing the action
            reason: Reason for reset
        """
        self.security_manager.reset_user_security(user_id)
        
        # Log admin action
        self.security_manager.audit_logger.log_security_event(
            ThreatType.UNAUTHORIZED_ACCESS,  # Using as admin action type
            SecurityLevel.MEDIUM,
            admin_user_id,
            "admin",
            f"Admin {admin_user_id} reset security for user {user_id}. Reason: {reason}",
            blocked=False,
            metadata={'target_user': user_id, 'reason': reason}
        )
        
        logger.info(f"Admin {admin_user_id} reset security for user {user_id}")
    
    def update_security_config(self, new_config: SecurityConfig, admin_user_id: str):
        """
        Update security configuration (admin function).
        
        Args:
            new_config: New security configuration
            admin_user_id: Administrator performing the update
        """
        old_config = self.security_config
        self.security_config = new_config
        
        # Reinitialize security manager with new config
        self.security_manager = SecurityManager(new_config)
        
        # Log configuration change
        self.security_manager.audit_logger.log_security_event(
            ThreatType.UNAUTHORIZED_ACCESS,  # Using as admin action type
            SecurityLevel.MEDIUM,
            admin_user_id,
            "admin",
            f"Security configuration updated by admin {admin_user_id}",
            blocked=False,
            metadata={
                'old_config': old_config.__dict__,
                'new_config': new_config.__dict__
            }
        )
        
        logger.info(f"Security configuration updated by admin {admin_user_id}")
    
    def _generate_cache_key(self, user_input: str, context: Dict[str, Any]) -> str:
        """Generate a cache key for the given input and context."""
        import hashlib
        
        # Create a hash of the input and relevant context
        cache_data = {
            'input': user_input,
            'context_keys': sorted(context.keys()) if context else []
        }
        
        cache_string = str(cache_data)
        return hashlib.md5(cache_string.encode()).hexdigest()
    
    def get_security_recommendations(self) -> Dict[str, Any]:
        """Get security recommendations based on current system state."""
        security_summary = self.security_manager.audit_logger.get_security_summary()
        
        recommendations = []
        
        # Analyze security events
        if security_summary:
            total_events = security_summary.get('total_events', 0)
            blocked_actions = security_summary.get('blocked_actions', 0)
            
            if total_events > 100:
                recommendations.append("High security event volume detected. Consider reviewing rate limits.")
            
            if blocked_actions / max(total_events, 1) > 0.1:
                recommendations.append("High block rate detected. Review security policies.")
            
            events_by_severity = security_summary.get('events_by_severity', {})
            if events_by_severity.get('critical', 0) > 0:
                recommendations.append("Critical security events detected. Immediate review required.")
            
            if events_by_severity.get('high', 0) > 10:
                recommendations.append("Multiple high-severity events. Consider tightening security.")
        
        # Check circuit breaker state
        if self.security_manager.circuit_breaker.state == 'OPEN':
            recommendations.append("Circuit breaker is open. System may be experiencing issues.")
        
        # Check blocked users
        blocked_count = len(self.security_manager.rate_limiter.blocked_users)
        if blocked_count > 10:
            recommendations.append(f"{blocked_count} users currently blocked. Review rate limiting policies.")
        
        return {
            'recommendations': recommendations,
            'security_score': self._calculate_security_score(),
            'last_updated': time.time()
        }
    
    def _calculate_security_score(self) -> int:
        """Calculate a security score from 0-100 based on current system state."""
        score = 100
        
        # Deduct points for security issues
        security_summary = self.security_manager.audit_logger.get_security_summary()
        
        if security_summary:
            events_by_severity = security_summary.get('events_by_severity', {})
            
            # Deduct points for security events
            score -= events_by_severity.get('critical', 0) * 10
            score -= events_by_severity.get('high', 0) * 5
            score -= events_by_severity.get('medium', 0) * 2
            
            # Deduct points for high block rate
            total_events = security_summary.get('total_events', 0)
            blocked_actions = security_summary.get('blocked_actions', 0)
            if total_events > 0:
                block_rate = blocked_actions / total_events
                if block_rate > 0.2:
                    score -= 20
                elif block_rate > 0.1:
                    score -= 10
        
        # Deduct points for circuit breaker issues
        if self.security_manager.circuit_breaker.state == 'OPEN':
            score -= 30
        elif self.security_manager.circuit_breaker.state == 'HALF_OPEN':
            score -= 10
        
        # Deduct points for many blocked users
        blocked_count = len(self.security_manager.rate_limiter.blocked_users)
        if blocked_count > 20:
            score -= 20
        elif blocked_count > 10:
            score -= 10
        
        return max(0, min(100, score))