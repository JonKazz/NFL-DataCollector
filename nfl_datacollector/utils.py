import time
import random
import pandas as pd

pd.set_option("display.max_columns", None)

def polite_sleep(min_seconds: float = 6.0, max_seconds: float = 8.0) -> None:
    sleep_time = random.uniform(min_seconds, max_seconds)
    time.sleep(sleep_time)


TEAM_ID_TO_TEAM_NAME_MAP = {
    'crd': 'Arizona Cardinals', 'atl': 'Atlanta Falcons', 'rav': 'Baltimore Ravens', 'buf': 'Buffalo Bills',
    'car': 'Carolina Panthers', 'chi': 'Chicago Bears', 'cin': 'Cincinnati Bengals', 'cle': 'Cleveland Browns',
    'dal': 'Dallas Cowboys', 'den': 'Denver Broncos', 'det': 'Detroit Lions', 'gnb': 'Green Bay Packers',
    'htx': 'Houston Texans', 'clt': 'Indianapolis Colts', 'jax': 'Jacksonville Jaguars', 'kan': 'Kansas City Chiefs',
    'sdg': 'Los Angeles Chargers', 'ram': 'Los Angeles Rams', 'rai': 'Las Vegas Raiders', 'mia': 'Miami Dolphins',
    'min': 'Minnesota Vikings', 'nwe': 'New England Patriots', 'nor': 'New Orleans Saints', 'nyg': 'New York Giants',
    'nyj': 'New York Jets', 'phi': 'Philadelphia Eagles', 'pit': 'Pittsburgh Steelers', 'sea': 'Seattle Seahawks',
    'sfo': 'San Francisco 49ers', 'tam': 'Tampa Bay Buccaneers', 'oti': 'Tennessee Titans', 'was': 'Washington Commanders'
}

TEAM_ID_TO_CITY_MAP = {
    'crd': 'Arizona', 'atl': 'Atlanta', 'rav': 'Baltimore', 'buf': 'Buffalo', 'car': 'Carolina',
    'chi': 'Chicago', 'cin': 'Cincinnati', 'cle': 'Cleveland', 'dal': 'Dallas', 'den': 'Denver',
    'det': 'Detroit', 'gnb': 'Green Bay', 'htx': 'Houston', 'clt': 'Indianapolis', 'jax': 'Jacksonville',
    'kan': 'Kansas City', 'sdg': 'Los Angeles', 'ram': 'Los Angeles', 'rai': 'Las Vegas',
    'mia': 'Miami', 'min': 'Minnesota', 'nwe': 'New England', 'nor': 'New Orleans', 'nyg': 'New York',
    'nyj': 'New York', 'phi': 'Philadelphia', 'pit': 'Pittsburgh', 'sea': 'Seattle',
    'sfo': 'San Francisco', 'tam': 'Tampa Bay', 'oti': 'Tennessee', 'was': 'Washington'
}

TEAM_ABR_TO_TEAM_ID_MAP = {
    "ARI": "crd", "ATL": "atl", "BAL": "rav", "BUF": "buf", "CAR": "car", "CHI": "chi", "CIN": "cin",
    "CLE": "cle", "DAL": "dal", "DEN": "den", "DET": "det", "GNB": "gnb", "HOU": "htx", "IND": "clt",
    "JAX": "jax", "KAN": "kan", "LAC": "sdg", "LAR": "ram", "LVR": "rai", "MIA": "mia", "MIN": "min",
    "NWE": "nwe", "NOR": "nor", "NYG": "nyg", "NYJ": "nyj", "PHI": "phi", "PIT": "pit", "SEA": "sea",
    "SFO": "sfo", "TAM": "tam", "TEN": "oti",
} 


ALL_SEASONS = [2024, 2023, 2022, 2021, 2020, 2019, 2018, 2017, 2016, 2015]