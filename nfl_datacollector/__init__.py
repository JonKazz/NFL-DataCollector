"""NFL Data Collector package."""

__version__ = "0.1.0"

from .config import DatabaseConfig
from .utils import polite_sleep

__all__ = ["DatabaseConfig", "polite_sleep"] 