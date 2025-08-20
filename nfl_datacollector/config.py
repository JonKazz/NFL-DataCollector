"""Configuration management for NFL Data Collector."""

import os
from dataclasses import dataclass


@dataclass
class DatabaseConfig:
    """Database configuration settings."""
    
    hostname: str
    database: str
    username: str
    password: str
    port: int
    
    @classmethod
    def from_env(cls):
        """Create configuration from environment variables."""
        return cls(
            hostname=os.getenv("DB_HOSTNAME", "localhost"),
            database=os.getenv("DB_DATABASE", "postgres"),
            username=os.getenv("DB_USERNAME", "postgres"),
            password=os.getenv("DB_PASSWORD", ""),
            port=int(os.getenv("DB_PORT", "1234")),
        )
    
    def get_connection_string(self) -> str:
        """Get SQLAlchemy connection string."""
        return f"postgresql+psycopg2://{self.username}:{self.password}@{self.hostname}:{self.port}/{self.database}" 