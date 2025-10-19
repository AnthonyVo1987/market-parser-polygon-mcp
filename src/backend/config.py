"""Configuration management for the Market Parser application."""

import json
import os
from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Consolidated application configuration with environment and JSON-based settings."""

    # API Keys (from environment)
    polygon_api_key: str
    openai_api_key: str
    tradier_api_key: str

    # MCP configuration
    mcp_timeout_seconds: float = 30.0
    polygon_mcp_version: str = "0.4.1"

    # Agent configuration
    agent_session_name: str = "financial_analysis_session"
    reports_directory: str = "reports"
    cli_session_name: str = "cli_financial_analysis_session"
    session_timeout_minutes: int = 30
    session_cleanup_interval_minutes: int = 5
    max_session_size: int = 1000
    enable_session_persistence: bool = True

    # AI configuration
    default_active_model: str = "gpt-5-nano"
    available_models: list = ["gpt-5-nano"]
    max_context_length: int = 400000
    ai_pricing: dict = {}

    # Logging configuration
    log_mode: str = "info"

    # Monitoring configuration
    enable_performance_monitoring: bool = True
    enable_error_tracking: bool = True
    enable_resource_monitoring: bool = True
    monitoring_log_level: str = "info"
    metrics_retention_days: int = 7

    # Frontend configuration
    frontend_config: dict = {}

    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"

    def __init__(self):
        super().__init__()

        # Set environment variables for OpenAI SDK (required for openai-agents SDK)
        # Pydantic loads .env into settings, but OpenAI SDK reads from os.environ
        os.environ["OPENAI_API_KEY"] = self.openai_api_key
        os.environ["POLYGON_API_KEY"] = self.polygon_api_key
        os.environ["TRADIER_API_KEY"] = self.tradier_api_key

        # Load configuration from JSON file and override defaults (if file exists)
        # This is optional for cloud deployments (HF Spaces) where config file may not be present
        config_path = Path(__file__).parent.parent.parent / "config" / "app.config.json"

        if config_path.exists():
            try:
                with open(config_path, encoding="utf-8") as f:
                    config = json.load(f)

                # Extract backend config
                backend_config = config["backend"]

                # Override defaults with config file values
                self.mcp_timeout_seconds = backend_config["mcp"]["timeoutSeconds"]
                self.polygon_mcp_version = backend_config["mcp"]["version"]

                # Agent configuration
                agent_config = backend_config["agent"]
                self.agent_session_name = agent_config["sessionName"]
                self.reports_directory = agent_config["reportsDirectory"]
                self.cli_session_name = agent_config["cliSessionName"]
                self.session_timeout_minutes = agent_config["sessionTimeoutMinutes"]
                self.session_cleanup_interval_minutes = agent_config["sessionCleanupIntervalMinutes"]
                self.max_session_size = agent_config["maxSessionSize"]
                self.enable_session_persistence = agent_config["enableSessionPersistence"]

                # AI configuration
                ai_config = backend_config["ai"]
                self.default_active_model = ai_config["default_active_model"]
                self.available_models = ["gpt-5-nano"]  # Only GPT-5-Nano supported
                self.max_context_length = ai_config["maxContextLength"]
                self.ai_pricing = ai_config["pricing"]

                # Logging configuration
                self.log_mode = backend_config["logging"]["mode"]

                # Monitoring configuration
                monitoring_config = backend_config["monitoring"]
                self.enable_performance_monitoring = monitoring_config["enablePerformanceMonitoring"]
                self.enable_error_tracking = monitoring_config["enableErrorTracking"]
                self.enable_resource_monitoring = monitoring_config["enableResourceMonitoring"]
                self.monitoring_log_level = monitoring_config["logLevel"]
                self.metrics_retention_days = monitoring_config["metricsRetentionDays"]
            except (json.JSONDecodeError, KeyError) as e:
                # Log error but continue with defaults
                print(f"Warning: Failed to load config from {config_path}: {e}")
                print("Continuing with default configuration values")
        else:
            # Config file not present (expected in cloud deployments like HF Spaces)
            # Use default values already set in class definition
            print(f"Info: Config file not found at {config_path}")
            print("Using default configuration values (expected for cloud deployments)")


# Initialize settings instance
settings = Settings()
