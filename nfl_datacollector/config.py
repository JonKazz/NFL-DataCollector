"""Configuration management for NFL Data Collector."""

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass
class DatabaseConfig:
    """Database configuration settings."""
    
    hostname: str
    database: str
    username: str
    password: str
    port: int
    
    @classmethod
    def from_local_file(cls):
        """Create configuration from local_config.txt file."""
        config_file = Path("local_config.txt")
        
        if not config_file.exists():
            return None
            
        try:
            with open(config_file, 'r') as f:
                lines = f.readlines()
                
            if len(lines) >= 5:
                return cls(
                    hostname=lines[0].strip(),
                    database=lines[1].strip(),
                    username=lines[2].strip(),
                    password=lines[3].strip(),
                    port=int(lines[4].strip())
                )
        except (ValueError, IndexError, FileNotFoundError):
            print("Error reading local_config.txt file. Please check the format.")
            
        return None
    
    @classmethod
    def from_interactive(cls):
        """Create configuration by prompting user interactively."""
        print("Database Configuration Setup")
        print("=" * 30)
        
        hostname = input("Enter DB_HOSTNAME (default: localhost): ").strip() or "localhost"
        database = input("Enter DB_DATABASE (default: postgres): ").strip() or "postgres"
        username = input("Enter DB_USERNAME (default: postgres): ").strip() or "postgres"
        password = input("Enter DB_PASSWORD: ").strip()
        
        while True:
            try:
                port_input = input("Enter DB_PORT (default: 5432): ").strip() or "5432"
                port = int(port_input)
                break
            except ValueError:
                print("Please enter a valid port number.")
        
        return cls(
            hostname=hostname,
            database=database,
            username=username,
            password=password,
            port=port
        )
    
    
    @classmethod
    def load(cls):
        """Load configuration with priority: local file > interactive > environment variables."""
        # First try local config file
        config = cls.from_local_file()
        if config:
            print("Configuration loaded from local_config.txt")
            return config
        
        # If no local file, prompt user interactively
        print("No local_config.txt found. Please provide database configuration:")
        config = cls.from_interactive()
        
        # Ask if user wants to save this config
        save_config = input("\nWould you like to save this configuration to local_config.txt? (y/n): ").strip().lower()
        if save_config in ['y', 'yes']:
            cls.save_to_file(config)
            print("Configuration saved to local_config.txt")
        
        return config
    
    @classmethod
    def save_to_file(cls, config, filename="local_config.txt"):
        """Save configuration to a text file."""
        try:
            with open(filename, 'w') as f:
                f.write(f"{config.hostname}\n")
                f.write(f"{config.database}\n")
                f.write(f"{config.username}\n")
                f.write(f"{config.password}\n")
                f.write(f"{config.port}\n")
            print(f"Configuration saved to {filename}")
        except Exception as e:
            print(f"Error saving configuration: {e}")
    
    def get_connection_string(self) -> str:
        """Get SQLAlchemy connection string."""
        return f"postgresql+psycopg2://{self.username}:{self.password}@{self.hostname}:{self.port}/{self.database}" 