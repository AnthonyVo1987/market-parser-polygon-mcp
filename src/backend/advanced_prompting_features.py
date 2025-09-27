"""
Advanced Prompting Features for Dynamic Adaptive Prompting System

This module provides advanced features for the dynamic prompting system including:
- Custom template management
- Learning system for user preferences
- Advanced analytics and insights
- Performance optimization
- Template versioning and rollback

Author: AI Assistant
Date: September 26, 2025
"""

import json
import logging
import time
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

from .dynamic_prompts import DynamicPromptManager, UserPreferences

logger = logging.getLogger(__name__)


@dataclass
class TemplateVersion:
    """Data class for template versioning"""

    version: str
    content: str
    created_at: datetime
    description: str
    is_active: bool = False


@dataclass
class UserAnalytics:
    """Data class for user analytics"""

    user_id: str
    total_requests: int
    preferred_verbosity: str
    preferred_format: str
    preferred_style: str
    most_used_tools: List[str]
    average_response_time: float
    last_activity: datetime


@dataclass
class PerformanceMetrics:
    """Data class for performance metrics"""

    timestamp: datetime
    response_time: float
    cache_hit_rate: float
    memory_usage: float
    cpu_usage: float
    error_rate: float


class CustomTemplateManager:
    """
    Manages custom user-defined prompt templates.

    This class allows users to create, store, and manage their own
    prompt templates with versioning and rollback capabilities.
    """

    def __init__(self, templates_dir: str = "templates"):
        self.templates_dir = Path(templates_dir)
        self.templates_dir.mkdir(exist_ok=True)
        self.templates: Dict[str, List[TemplateVersion]] = defaultdict(list)
        self.active_templates: Dict[str, str] = {}
        self._load_templates()

    def create_template(self, name: str, content: str, description: str = "") -> str:
        """
        Create a new custom template.

        Args:
            name: Template name
            content: Template content
            description: Template description

        Returns:
            Version ID of the created template
        """
        version_id = f"v{len(self.templates[name]) + 1}"
        version = TemplateVersion(
            version=version_id,
            content=content,
            created_at=datetime.now(),
            description=description,
            is_active=True,
        )

        # Deactivate previous versions
        for prev_version in self.templates[name]:
            prev_version.is_active = False

        self.templates[name].append(version)
        self.active_templates[name] = version_id
        self._save_templates()

        logger.info(f"Created template '{name}' version {version_id}")
        return version_id

    def get_template(self, name: str, version: Optional[str] = None) -> Optional[str]:
        """
        Get a template by name and version.

        Args:
            name: Template name
            version: Version ID (defaults to active version)

        Returns:
            Template content or None if not found
        """
        if name not in self.templates:
            return None

        if version is None:
            version = self.active_templates.get(name)

        for template_version in self.templates[name]:
            if template_version.version == version:
                return template_version.content

        return None

    def list_templates(self) -> List[Dict[str, Any]]:
        """List all available templates with their versions."""
        result = []
        for name, versions in self.templates.items():
            active_version = self.active_templates.get(name)
            result.append(
                {
                    "name": name,
                    "versions": [asdict(v) for v in versions],
                    "active_version": active_version,
                    "total_versions": len(versions),
                }
            )
        return result

    def rollback_template(self, name: str, version: str) -> bool:
        """
        Rollback a template to a previous version.

        Args:
            name: Template name
            version: Version to rollback to

        Returns:
            True if rollback successful, False otherwise
        """
        if name not in self.templates:
            return False

        # Find the target version
        target_version = None
        for template_version in self.templates[name]:
            if template_version.version == version:
                target_version = template_version
                break

        if target_version is None:
            return False

        # Deactivate all versions
        for template_version in self.templates[name]:
            template_version.is_active = False

        # Activate target version
        target_version.is_active = True
        self.active_templates[name] = version
        self._save_templates()

        logger.info(f"Rolled back template '{name}' to version {version}")
        return True

    def delete_template(self, name: str, version: Optional[str] = None) -> bool:
        """
        Delete a template or specific version.

        Args:
            name: Template name
            version: Version to delete (defaults to all versions)

        Returns:
            True if deletion successful, False otherwise
        """
        if name not in self.templates:
            return False

        if version is None:
            # Delete all versions
            del self.templates[name]
            if name in self.active_templates:
                del self.active_templates[name]
        else:
            # Delete specific version
            self.templates[name] = [v for v in self.templates[name] if v.version != version]
            if not self.templates[name]:
                del self.templates[name]
                if name in self.active_templates:
                    del self.active_templates[name]
            elif self.active_templates.get(name) == version:
                # If deleting active version, activate the latest remaining version
                if self.templates[name]:
                    latest_version = max(self.templates[name], key=lambda v: v.created_at)
                    latest_version.is_active = True
                    self.active_templates[name] = latest_version.version

        self._save_templates()
        logger.info(f"Deleted template '{name}' version {version or 'all'}")
        return True

    def _load_templates(self):
        """Load templates from disk."""
        templates_file = self.templates_dir / "templates.json"
        if templates_file.exists():
            try:
                with open(templates_file, "r") as f:
                    data = json.load(f)

                for name, versions_data in data.get("templates", {}).items():
                    for version_data in versions_data:
                        version = TemplateVersion(
                            version=version_data["version"],
                            content=version_data["content"],
                            created_at=datetime.fromisoformat(version_data["created_at"]),
                            description=version_data["description"],
                            is_active=version_data["is_active"],
                        )
                        self.templates[name].append(version)

                self.active_templates = data.get("active_templates", {})
                logger.info(f"Loaded {len(self.templates)} templates")
            except Exception as e:
                logger.error(f"Error loading templates: {e}")

    def _save_templates(self):
        """Save templates to disk."""
        templates_file = self.templates_dir / "templates.json"
        try:
            data = {"templates": {}, "active_templates": self.active_templates}

            for name, versions in self.templates.items():
                data["templates"][name] = [asdict(v) for v in versions]

            with open(templates_file, "w") as f:
                json.dump(data, f, indent=2, default=str)

            logger.debug(f"Saved {len(self.templates)} templates")
        except Exception as e:
            logger.error(f"Error saving templates: {e}")


class LearningSystem:
    """
    Learning system that adapts to user preferences over time.

    This class analyzes user behavior and automatically suggests
    improvements to prompt templates and user preferences.
    """

    def __init__(self, analytics_file: str = "analytics.json"):
        self.analytics_file = Path(analytics_file)
        self.user_analytics: Dict[str, UserAnalytics] = {}
        self.performance_metrics: List[PerformanceMetrics] = []
        self.preference_patterns: Dict[str, Counter] = defaultdict(Counter)
        self._load_analytics()

    def record_user_interaction(
        self, user_id: str, preferences: UserPreferences, response_time: float, success: bool
    ):
        """
        Record a user interaction for learning.

        Args:
            user_id: User identifier
            preferences: User preferences used
            response_time: Response time in seconds
            success: Whether the interaction was successful
        """
        # Update user analytics
        if user_id not in self.user_analytics:
            self.user_analytics[user_id] = UserAnalytics(
                user_id=user_id,
                total_requests=0,
                preferred_verbosity="standard",
                preferred_format="structured",
                preferred_style="professional",
                most_used_tools=[],
                average_response_time=0.0,
                last_activity=datetime.now(),
            )

        analytics = self.user_analytics[user_id]
        analytics.total_requests += 1
        analytics.last_activity = datetime.now()

        # Update average response time
        if analytics.average_response_time == 0.0:
            analytics.average_response_time = response_time
        else:
            analytics.average_response_time = (analytics.average_response_time + response_time) / 2

        # Update preference patterns
        if preferences.verbosity:
            self.preference_patterns[user_id]["verbosity"][preferences.verbosity] += 1
        if preferences.output_format:
            self.preference_patterns[user_id]["format"][preferences.output_format] += 1
        if preferences.response_style:
            self.preference_patterns[user_id]["style"][preferences.response_style] += 1

        # Update most common preferences
        self._update_user_preferences(user_id)

        # Record performance metrics
        self.performance_metrics.append(
            PerformanceMetrics(
                timestamp=datetime.now(),
                response_time=response_time,
                cache_hit_rate=0.0,  # Will be updated by cache system
                memory_usage=0.0,  # Will be updated by monitoring system
                cpu_usage=0.0,  # Will be updated by monitoring system
                error_rate=0.0 if success else 1.0,
            )
        )

        # Keep only last 1000 metrics to prevent memory growth
        if len(self.performance_metrics) > 1000:
            self.performance_metrics = self.performance_metrics[-1000:]

        self._save_analytics()

    def get_user_recommendations(self, user_id: str) -> Dict[str, Any]:
        """
        Get personalized recommendations for a user.

        Args:
            user_id: User identifier

        Returns:
            Dictionary with recommendations
        """
        if user_id not in self.user_analytics:
            return {}

        analytics = self.user_analytics[user_id]
        patterns = self.preference_patterns[user_id]

        recommendations = {
            "user_id": user_id,
            "total_requests": analytics.total_requests,
            "preferred_verbosity": analytics.preferred_verbosity,
            "preferred_format": analytics.preferred_format,
            "preferred_style": analytics.preferred_style,
            "average_response_time": analytics.average_response_time,
            "suggestions": [],
        }

        # Generate suggestions based on patterns
        if analytics.total_requests > 10:
            # Suggest most used preferences
            if patterns["verbosity"]:
                most_used_verbosity = patterns["verbosity"].most_common(1)[0][0]
                if most_used_verbosity != analytics.preferred_verbosity:
                    recommendations["suggestions"].append(
                        f"Consider using [{most_used_verbosity}] for verbosity based on your usage patterns"
                    )

            if patterns["format"]:
                most_used_format = patterns["format"].most_common(1)[0][0]
                if most_used_format != analytics.preferred_format:
                    recommendations["suggestions"].append(
                        f"Consider using [{most_used_format}] for output format based on your usage patterns"
                    )

            if patterns["style"]:
                most_used_style = patterns["style"].most_common(1)[0][0]
                if most_used_style != analytics.preferred_style:
                    recommendations["suggestions"].append(
                        f"Consider using [{most_used_style}] for response style based on your usage patterns"
                    )

        return recommendations

    def get_system_insights(self) -> Dict[str, Any]:
        """Get system-wide insights and analytics."""
        if not self.performance_metrics:
            return {}

        recent_metrics = [
            m
            for m in self.performance_metrics
            if m.timestamp > datetime.now() - timedelta(hours=24)
        ]

        if not recent_metrics:
            return {}

        avg_response_time = sum(m.response_time for m in recent_metrics) / len(recent_metrics)
        avg_error_rate = sum(m.error_rate for m in recent_metrics) / len(recent_metrics)

        # User activity insights
        active_users = len(
            [
                u
                for u in self.user_analytics.values()
                if u.last_activity > datetime.now() - timedelta(hours=24)
            ]
        )

        # Most popular preferences
        all_verbosity = Counter()
        all_format = Counter()
        all_style = Counter()

        for patterns in self.preference_patterns.values():
            all_verbosity.update(patterns["verbosity"])
            all_format.update(patterns["format"])
            all_style.update(patterns["style"])

        return {
            "total_users": len(self.user_analytics),
            "active_users_24h": active_users,
            "total_requests_24h": len(recent_metrics),
            "average_response_time": avg_response_time,
            "error_rate": avg_error_rate,
            "most_popular_verbosity": all_verbosity.most_common(1)[0] if all_verbosity else None,
            "most_popular_format": all_format.most_common(1)[0] if all_format else None,
            "most_popular_style": all_style.most_common(1)[0] if all_style else None,
            "performance_trend": self._calculate_performance_trend(),
        }

    def _update_user_preferences(self, user_id: str):
        """Update user's most common preferences."""
        if user_id not in self.user_analytics:
            return

        analytics = self.user_analytics[user_id]
        patterns = self.preference_patterns[user_id]

        if patterns["verbosity"]:
            analytics.preferred_verbosity = patterns["verbosity"].most_common(1)[0][0]
        if patterns["format"]:
            analytics.preferred_format = patterns["format"].most_common(1)[0][0]
        if patterns["style"]:
            analytics.preferred_style = patterns["style"].most_common(1)[0][0]

    def _calculate_performance_trend(self) -> str:
        """Calculate performance trend over time."""
        if len(self.performance_metrics) < 10:
            return "insufficient_data"

        recent_metrics = self.performance_metrics[-10:]
        older_metrics = (
            self.performance_metrics[-20:-10] if len(self.performance_metrics) >= 20 else []
        )

        if not older_metrics:
            return "insufficient_data"

        recent_avg = sum(m.response_time for m in recent_metrics) / len(recent_metrics)
        older_avg = sum(m.response_time for m in older_metrics) / len(older_metrics)

        if recent_avg < older_avg * 0.9:
            return "improving"
        elif recent_avg > older_avg * 1.1:
            return "degrading"
        else:
            return "stable"

    def _load_analytics(self):
        """Load analytics data from disk."""
        if self.analytics_file.exists():
            try:
                with open(self.analytics_file, "r") as f:
                    data = json.load(f)

                # Load user analytics
                for user_id, user_data in data.get("user_analytics", {}).items():
                    self.user_analytics[user_id] = UserAnalytics(
                        user_id=user_data["user_id"],
                        total_requests=user_data["total_requests"],
                        preferred_verbosity=user_data["preferred_verbosity"],
                        preferred_format=user_data["preferred_format"],
                        preferred_style=user_data["preferred_style"],
                        most_used_tools=user_data["most_used_tools"],
                        average_response_time=user_data["average_response_time"],
                        last_activity=datetime.fromisoformat(user_data["last_activity"]),
                    )

                # Load preference patterns
                for user_id, patterns_data in data.get("preference_patterns", {}).items():
                    for pref_type, counts in patterns_data.items():
                        self.preference_patterns[user_id][pref_type] = Counter(counts)

                logger.info(f"Loaded analytics for {len(self.user_analytics)} users")
            except Exception as e:
                logger.error(f"Error loading analytics: {e}")

    def _save_analytics(self):
        """Save analytics data to disk."""
        try:
            data = {
                "user_analytics": {
                    uid: asdict(analytics) for uid, analytics in self.user_analytics.items()
                },
                "preference_patterns": {
                    uid: {pref_type: dict(counts) for pref_type, counts in patterns.items()}
                    for uid, patterns in self.preference_patterns.items()
                },
            }

            with open(self.analytics_file, "w") as f:
                json.dump(data, f, indent=2, default=str)

            logger.debug("Saved analytics data")
        except Exception as e:
            logger.error(f"Error saving analytics: {e}")


class AdvancedPromptManager(DynamicPromptManager):
    """
    Advanced prompt manager with learning and analytics capabilities.

    This class extends the base DynamicPromptManager with advanced features
    including custom templates, learning system, and analytics.
    """

    def __init__(self, base_template: str, config: Dict[str, Any]):
        super().__init__(base_template, config)
        self.template_manager = CustomTemplateManager()
        self.learning_system = LearningSystem()
        self.performance_monitor = PerformanceMonitor()

    def generate_prompt(
        self, user_input: str, context: Dict[str, Any], user_id: str = "anonymous"
    ) -> str:
        """
        Generate a customized prompt with advanced features.

        Args:
            user_input: The user's input message
            context: Additional context for prompt generation
            user_id: User identifier for analytics

        Returns:
            Customized prompt string
        """
        start_time = time.time()

        try:
            # Parse user instructions
            preferences = self.parse_user_instructions(user_input)

            # Validate preferences
            self.validator.validate_preferences(preferences)

            # Check for custom template
            custom_template = self._get_custom_template(user_input, preferences)
            if custom_template:
                template = custom_template
            else:
                template = self.base_template

            # Apply customizations to template
            customized_prompt = self.template_engine.apply_preferences(
                template, preferences, context
            )

            # Cache result for performance
            self.cache.store(user_input, customized_prompt)

            # Record interaction for learning
            response_time = time.time() - start_time
            self.learning_system.record_user_interaction(user_id, preferences, response_time, True)

            return customized_prompt

        except Exception as e:
            response_time = time.time() - start_time
            self.learning_system.record_user_interaction(
                user_id, UserPreferences(), response_time, False
            )
            return self._handle_general_error(e, user_input)

    def _get_custom_template(self, user_input: str, preferences: UserPreferences) -> Optional[str]:
        """Get custom template if applicable."""
        # Simple heuristic: check if user input contains template reference
        if "[template:" in user_input:
            # Extract template name from input
            import re

            match = re.search(r"\[template:([^\]]+)\]", user_input)
            if match:
                template_name = match.group(1)
                return self.template_manager.get_template(template_name)
        return None

    def get_user_recommendations(self, user_id: str) -> Dict[str, Any]:
        """Get personalized recommendations for a user."""
        return self.learning_system.get_user_recommendations(user_id)

    def get_system_insights(self) -> Dict[str, Any]:
        """Get system-wide insights and analytics."""
        return self.learning_system.get_system_insights()

    def create_custom_template(self, name: str, content: str, description: str = "") -> str:
        """Create a custom template."""
        return self.template_manager.create_template(name, content, description)

    def list_custom_templates(self) -> List[Dict[str, Any]]:
        """List all custom templates."""
        return self.template_manager.list_templates()


class PerformanceMonitor:
    """
    Performance monitoring for the dynamic prompting system.

    This class monitors system performance and provides insights
    for optimization.
    """

    def __init__(self):
        self.metrics: List[PerformanceMetrics] = []
        self.start_time = time.time()

    def record_metrics(
        self,
        response_time: float,
        cache_hit_rate: float,
        memory_usage: float,
        cpu_usage: float,
        error_rate: float,
    ):
        """Record performance metrics."""
        self.metrics.append(
            PerformanceMetrics(
                timestamp=datetime.now(),
                response_time=response_time,
                cache_hit_rate=cache_hit_rate,
                memory_usage=memory_usage,
                cpu_usage=cpu_usage,
                error_rate=error_rate,
            )
        )

        # Keep only last 1000 metrics
        if len(self.metrics) > 1000:
            self.metrics = self.metrics[-1000:]

    def get_performance_summary(self) -> Dict[str, Any]:
        """Get performance summary."""
        if not self.metrics:
            return {}

        recent_metrics = [
            m for m in self.metrics if m.timestamp > datetime.now() - timedelta(hours=1)
        ]

        if not recent_metrics:
            return {}

        return {
            "uptime_hours": (time.time() - self.start_time) / 3600,
            "total_requests": len(self.metrics),
            "requests_last_hour": len(recent_metrics),
            "average_response_time": sum(m.response_time for m in recent_metrics)
            / len(recent_metrics),
            "average_cache_hit_rate": sum(m.cache_hit_rate for m in recent_metrics)
            / len(recent_metrics),
            "average_memory_usage": sum(m.memory_usage for m in recent_metrics)
            / len(recent_metrics),
            "average_cpu_usage": sum(m.cpu_usage for m in recent_metrics) / len(recent_metrics),
            "error_rate": sum(m.error_rate for m in recent_metrics) / len(recent_metrics),
        }
