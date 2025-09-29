"""Configuration management for the Market Parser application."""

import json
from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Consolidated application configuration with environment and JSON-based settings."""

    # API Keys (from environment)
    polygon_api_key: str
    openai_api_key: str

    # Server configuration
    fastapi_host: str = "127.0.0.1"
    fastapi_port: int = 8000

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

    # CORS configuration
    cors_origins: str = "http://localhost:3000,http://127.0.0.1:3000"

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

        # Load configuration from JSON file and override defaults
        config_path = Path(__file__).parent.parent.parent / "config" / "app.config.json"
        with open(config_path, encoding="utf-8") as f:
            config = json.load(f)

        # Extract backend and frontend configs
        backend_config = config["backend"]
        frontend_config = config["frontend"]

        # Override defaults with config file values
        self.fastapi_host = backend_config["server"]["host"]
        self.fastapi_port = backend_config["server"]["port"]
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

        # CORS configuration
        cors_origins_list = backend_config["security"]["cors"]["origins"]
        self.cors_origins = ",".join(cors_origins_list)

        # AI configuration
        ai_config = backend_config["ai"]
        self.default_active_model = ai_config["default_active_model"]
        self.available_models = ["gpt-5-nano"]  # Only GPT-5-Nano supported
        self.max_context_length = ai_config["maxContextLength"]
        self.ai_pricing = ai_config["pricing"]

        # Security configuration (rate limiting removed for maximum performance)
        # Only CORS configuration remains

        # Logging configuration
        self.log_mode = backend_config["logging"]["mode"]

        # Monitoring configuration
        monitoring_config = backend_config["monitoring"]
        self.enable_performance_monitoring = monitoring_config["enablePerformanceMonitoring"]
        self.enable_error_tracking = monitoring_config["enableErrorTracking"]
        self.enable_resource_monitoring = monitoring_config["enableResourceMonitoring"]
        self.monitoring_log_level = monitoring_config["logLevel"]
        self.metrics_retention_days = monitoring_config["metricsRetentionDays"]

        # Frontend configuration
        self.frontend_config = frontend_config


# Initialize settings instance
settings = Settings()
