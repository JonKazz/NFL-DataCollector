# NFL Data Collector

A comprehensive Python web scraper for collecting NFL data from Pro Football Reference and storing it in a local PostgreSQL database. This library provides extensive coverage of NFL statistics and information.

## What It Does

The NFL Data Collector scrapes and stores:

- **Season Data** - Complete season schedules, standings, and outcomes
- **Team Season Statistics** - Comprehensive team performance metrics, records, and rankings
- **Game Statistics** - Detailed game-by-game statistics for both teams
- **Player Statistics** - Individual player performance data for each game with up to 100 metrics
- **Player Profiles** - Player biographical information, physical attributes, and career details

## Data Sources

All data is scraped from [Pro Football Reference](https://www.pro-football-reference.com/), a comprehensive and reliable source for NFL statistics and historical data.

## Configuration Setup

The application uses a flexible configuration system with the following priority order:

1. **Local Config File** (`local_config.txt`) - Highest priority
2. **Interactive Input** - Prompts user for database credentials

### Option 1: Local Config File (Recommended)

Create a `local_config.txt` file in the project root with the following format:

```
localhost
nfl_database
your_username
your_password
5432
```

**File format (one value per line):**
- Line 1: DB_HOSTNAME
- Line 2: DB_DATABASE  
- Line 3: DB_USERNAME
- Line 4: DB_PASSWORD
- Line 5: DB_PORT

### Option 2: Interactive Setup

If no `local_config.txt` file exists, the application will prompt you for each database setting:

```
Database Configuration Setup
==============================
Enter DB_HOSTNAME (default: localhost): 
Enter DB_DATABASE (default: postgres): 
Enter DB_USERNAME (default: postgres): 
Enter DB_PASSWORD: 
Enter DB_PORT (default: 5432): 
```

The application will ask if you want to save this configuration to `local_config.txt` for future use.

## Running the Application

```bash
python main.py
```

The application will automatically detect your configuration method and proceed accordingly.

## Database Schema

The library creates and manages several PostgreSQL tables:
- `game_info` - Game metadata and results
- `game_stats` - Team statistics for each game
- `game_player_stats` - Individual player statistics for each game
- `player_profiles` - Player biographical information
- `season_team_info` - Team season summaries and records
