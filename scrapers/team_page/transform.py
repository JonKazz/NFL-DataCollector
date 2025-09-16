import pandas as pd
import re
from nfl_datacollector.utils import TEAM_ID_TO_TEAM_NAME_MAP, TEAM_ID_TO_CITY_MAP

def transform_season_team_info_df(df):
    df = parse_playoffs_column(df)
    df = parse_record_column(df)
    df = parse_conference_column(df)
    
    df['id'] = df['team_id'] + '_' + df['year']
    df['name'] = df['team_id'].map(TEAM_ID_TO_TEAM_NAME_MAP)
    df['city'] = df['team_id'].map(TEAM_ID_TO_CITY_MAP)
    df['coach'] = df['Coach'].str.replace(r'\s*\(\d+-\d+-\d+\)', '', regex=True)
    df['points_for'] = df['Points For'].str.split(' ').str[0]
    df['points_against'] = df['Points Against'].str.split(' ').str[0]
    df = column_mapping(df)
    
    return df

    
def column_mapping(df):
    col_map = {
        'id': 'id',
        'team_id': 'team_id',
        'year': 'year',
        'name': 'name',
        'city': 'city',
        'Stadium': 'stadium',
        'wins': 'wins',
        'losses': 'losses',
        'ties': 'ties',
        'conference': 'conference',
        'division': 'division',
        'division_rank': 'division_rank',
        'playoffs': 'playoffs',
        'points_for': 'points_for',
        'points_against': 'points_against',
        'coach': 'coach',
        'Offensive Coordinator': 'off_coordinator',
        'Defensive Coordinator': 'def_coordinator',
        'Offensive Scheme': 'off_scheme',
        'Defensive Alignment': 'def_alignment',
        'logo': 'logo',
        
        'total_yards_for': 'total_yards_for',
        'total_yards_against': 'total_yards_against',
        'turnovers': 'turnovers',           
        'forced_turnovers': 'forced_turnovers', 
        'pass_yards_for': 'pass_yards_for',
        'pass_yards_against': 'pass_yards_against',
        'pass_td_for': 'pass_td_for',
        'pass_td_against': 'pass_td_against',
        'pass_ints_thrown': 'pass_ints_thrown',           
        'pass_ints': 'pass_ints',
        'rush_yards_for': 'rush_yards_for',
        'rush_yards_against': 'rush_yards_against',
        'rush_td_for': 'rush_td_for',
        'rush_td_against': 'rush_td_against',
        'penalties_for': 'penalties_for',
    }
    df = df.rename(columns=col_map)
    df = df[list(col_map.values())]
    return df
    

def parse_playoffs_column(df):
    def classify_playoffs(playoff_text):
        if pd.isna(playoff_text):
            return 'Missed Playoffs'
        elif 'Won Super Bowl' in playoff_text:
            return 'Won Super Bowl'
        elif 'Lost Super Bowl' in playoff_text:
            return 'Lost Super Bowl'
        elif 'Lost Conference Championship' in playoff_text:
            return 'Lost Conference Championship'
        elif 'Lost Divisional' in playoff_text:
            return 'Lost Divisional'
        elif 'Lost Wild Card' in playoff_text:
            return 'Lost Wild Card'
        else:
            return 'Unknown'

    df['playoffs'] = df['Playoffs'].apply(classify_playoffs)
    return df


def parse_record_column(df):
    def extract_all_parts(record):
        if pd.isna(record):
            return pd.Series([None, None, None, None, None])

        match = re.search(r'(\d+)-(\d+)-(\d+),\s*(\d+)(?:st|nd|rd|th)\s+in\s*([A-Z]+ [A-Za-z]+)', record)
        if match:
            wins = int(match.group(1))
            losses = int(match.group(2))
            ties = int(match.group(3))
            division_rank = int(match.group(4))
            division = match.group(5)
            return pd.Series([wins, losses, ties, division_rank, division])
        else:
            return pd.Series([None, None, None, None, None])

    df[['wins', 'losses', 'ties', 'division_rank', 'division']] = df['Record'].apply(extract_all_parts)
    return df

def parse_conference_column(df):
    # first word of the division string, e.g., "AFC West" -> "AFC"
    df['conference'] = df['division'].str.strip().str.split(n=1).str[0].str.lower()
    return df