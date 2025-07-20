import logging
import logging.handlers
import os
import platform
import sys
from pathlib import Path
from typing import Optional

from settings import AgentSettings


def get_default_log_dir() -> Path:
    """Get the default log directory based on OS standards"""
    system = platform.system().lower()

    if system == "darwin":  # macOS
        return Path.home() / "Library" / "Logs" / "agentic-classifier"
    elif system == "linux":
        if os.geteuid() == 0:
            return Path("/var/log/agentic-classifier")
        else:
            return Path.home() / ".local" / "state" / "agentic-classifier" / "logs"
    elif system == "windows":
        return Path.home() / "AppData" / "Local" / "agentic-classifier" / "logs"
    else:
        return Path.home() / ".agentic-classifier" / "logs"


def setup_logging(agent_config: Optional[AgentSettings] = None) -> None:
    """Configure logging for the mcp-simple-server MCP server"""
    # Get log level from server config, environment, or default to INFO
    log_level = "INFO"
    if agent_config and hasattr(agent_config, "log_level"):
        log_level = agent_config.log_level.upper()
    elif os.getenv("LOG_LEVEL"):
        log_level = os.getenv("LOG_LEVEL").upper()

    valid_levels = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
    }
    effective_level = valid_levels.get(log_level, logging.INFO)

    # Configure basic logging first
    logging.basicConfig(
        level=effective_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[],  # We'll add handlers explicitly
    )

    # Get all relevant loggers
    project_logger = logging.getLogger("agentic_classifier")
    root_logger = logging.getLogger()

    # Remove any existing handlers to avoid duplicates
    for logger in [
        project_logger,
        root_logger,
    ]:
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)

    # Create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Add stderr handler
    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setLevel(effective_level)
    stderr_handler.setFormatter(formatter)
    root_logger.addHandler(stderr_handler)

    # Set up file logging
    log_path = get_default_log_dir()
    log_path.mkdir(parents=True, exist_ok=True)
    log_file = log_path / "agentic_classifier.log"

    # Add rotating file handler (10MB files, keep 5 backups)
    file_handler = logging.handlers.RotatingFileHandler(
        log_file, maxBytes=10_000_000, backupCount=5, encoding="utf-8"
    )
    file_handler.setLevel(effective_level)
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)

    # Set levels for all loggers
    for logger in [
        project_logger,
    ]:
        logger.setLevel(effective_level)
        # Ensure propagation is enabled
        logger.propagate = True

    # Log startup information
    project_logger.info(f"Log File: {log_file}")
    project_logger.info("Logging Enabled for:")
    project_logger.info(f"- {project_logger.name} (Project Logger)")
    project_logger.info(f"Log Level: {log_level}")


# Export the logger for use in other modules
logger = logging.getLogger("agentic_classifier")
