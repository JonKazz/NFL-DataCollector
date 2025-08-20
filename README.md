# NFL Data Collector

A Python application for collecting and storing NFL game data, player statistics, and team information.

## Configuration Setup

The application uses a flexible configuration system with the following priority order:

1. **Local Config File** (`local_config.txt`) - Highest priority
2. **Interactive Input** - Prompts user for database credentials
3. **Environment Variables** - Fallback option

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

### Option 3: Environment Variables

Set these environment variables as a fallback:

```bash
export DB_HOSTNAME=localhost
export DB_DATABASE=nfl_database
export DB_USERNAME=your_username
export DB_PASSWORD=your_password
export DB_PORT=5432
```

## Security Notes

- `local_config.txt` is automatically added to `.gitignore` to prevent accidentally committing credentials
- Never commit real database credentials to version control
- Use the example file `local_config.txt.example` as a template

## Running the Application

```bash
python main.py
```

The application will automatically detect your configuration method and proceed accordingly.
