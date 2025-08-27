import pandas as pd

SEASON_INFO_COL_MAP = {
    'url': 'url',
    'season_year': 'season_year',
    'sb_champ': 'sb_champ',
    'mvp_id': 'mvp_id',
    'mvp_name': 'mvp_name',
    'opoy_id': 'opoy_id',
    'opoy_name': 'opoy_name',
    'dpoy_id': 'dpoy_id',
    'dpoy_name': 'dpoy_name',
    'oroy_id': 'oroy_id',
    'oroy_name': 'oroy_name',
    'droy_id': 'droy_id',
    'droy_name': 'droy_name',
    'passing_leader_id': 'passing_leader_id',
    'passing_leader_name': 'passing_leader_name',
    'rushing_leader_id': 'rushing_leader_id',
    'rushing_leader_name': 'rushing_leader_name',
    'receiving_leader_id': 'receiving_leader_id',
    'receiving_leader_name': 'receiving_leader_name',
}
        
def transform_season_info_df(game_info_df) -> pd.DataFrame:
    game_info_df = _normalize_df(game_info_df, SEASON_INFO_COL_MAP)
    return game_info_df

    
def _normalize_df(df, col_map: dict) -> pd.DataFrame:
    
    for original_col, new_col in col_map.items():
        if original_col not in df.columns:
            df[original_col] = pd.NA

    df = df.rename(columns=col_map)
    df = df[list(col_map.values())]
    return df
    
