"""UTF-8 logging configuration for the S-Art backend."""

from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent.parent
LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"


def get_logging_config() -> dict:
    """Return a uvicorn-compatible logging config with explicit UTF-8 files."""
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": LOG_FORMAT,
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            "access": {
                "format": (
                    "%(asctime)s | %(levelname)s | %(name)s | "
                    '%(client_addr)s | "%(request_line)s" | %(status_code)s'
                ),
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
                "stream": "ext://sys.stdout",
            },
            "backend_file": {
                "class": "logging.FileHandler",
                "formatter": "default",
                "filename": str(PROJECT_DIR / "backend.out.log"),
                "encoding": "utf-8",
                "mode": "a",
            },
            "error_file": {
                "class": "logging.FileHandler",
                "formatter": "default",
                "filename": str(PROJECT_DIR / "backend.err.log"),
                "encoding": "utf-8",
                "mode": "a",
                "level": "ERROR",
            },
            "access_file": {
                "class": "logging.FileHandler",
                "formatter": "access",
                "filename": str(PROJECT_DIR / "backend.out.log"),
                "encoding": "utf-8",
                "mode": "a",
            },
        },
        "loggers": {
            "uvicorn": {
                "handlers": ["console", "backend_file", "error_file"],
                "level": "INFO",
                "propagate": False,
            },
            "uvicorn.error": {
                "handlers": ["console", "backend_file", "error_file"],
                "level": "INFO",
                "propagate": False,
            },
            "uvicorn.access": {
                "handlers": ["console", "access_file", "error_file"],
                "level": "INFO",
                "propagate": False,
            },
        },
        "root": {
            "handlers": ["console", "backend_file", "error_file"],
            "level": "INFO",
        },
    }
