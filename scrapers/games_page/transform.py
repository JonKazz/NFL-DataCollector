import numpy as np
import pandas as pd
from nfl_datacollector.utils import TEAM_ABR_TO_TEAM_ID_MAP

GAME_INFO_COL_MAP = {
    'game_id': 'game_id',
    'url': 'url',
    'Won Toss': 'won_toss',
    'Roof': 'roof_type',
    'Surface': 'surface_type',
    'Duration': 'game_duration',
    'Attendance': 'attendance',
    'Weather': 'weather',
    'Vegas Line': 'vegas_line',
    'Over/Under': 'over_under',
    'date': 'date',
    'start_time': 'start_time',
    'stadium': 'stadium',
    'overtime': 'overtime',
    'home_team_id': 'home_team_id',
    'away_team_id': 'away_team_id',
    'winning_team_id': 'winning_team_id',
    'home_team_record': 'home_team_record',
    'away_team_record': 'away_team_record',
    'home_points': 'home_points',
    'away_points': 'away_points',
    'season_week': 'season_week',
    'season_year': 'season_year'
}

GAME_STATS_COL_MAP = {
    'game_id': 'game_id',
    'team_id': 'team_id',
    'Rush-Yds-TDs': 'rush_stats_combined',
    'Cmp-Att-Yd-TD-INT': 'passing_stats_combined',
    'Sacked-Yards': 'sack_stats_combined',
    'Fumbles-Lost': 'fumble_stats_combined',
    'Penalties-Yards': 'penalty_stats_combined',
    'Third Down Conv.': 'third_down_stats_combined',
    'Fourth Down Conv.': 'fourth_down_stats_combined',
    'First Downs': 'first_downs_total',
    'Net Pass Yards': 'net_passing_yards',
    'Total Yards': 'total_yards',
    'Turnovers': 'turnovers',
    'Time of Possession': 'time_of_possession',
    'points_q1': 'points_q1',
    'points_q2': 'points_q2',
    'points_q3': 'points_q3',
    'points_q4': 'points_q4',
    'points_overtime': 'points_overtime',
    'points_total': 'points_total',
    'rushing_attempts': 'rushing_attempts',
    'rushing_yards': 'rushing_yards',
    'rushing_touchdowns': 'rushing_touchdowns',
    'passing_attempts': 'passing_attempts',
    'passing_completions': 'passing_completions',
    'passing_yards': 'passing_yards',
    'passing_touchdowns': 'passing_touchdowns',
    'passing_interceptions': 'passing_interceptions',
    'sacks_total': 'sacks_total',
    'sack_yards': 'sack_yards',
    'fumbles_total': 'fumbles_total',
    'fumbles_lost': 'fumbles_lost',
    'penalties_total': 'penalties_total',
    'penalty_yards': 'penalty_yards',
    'third_down_conversions': 'third_down_conversions',
    'third_down_attempts': 'third_down_attempts',
    'fourth_down_conversions': 'fourth_down_conversions',
    'fourth_down_attempts': 'fourth_down_attempts'
}



PLAYER_STATS_COL_MAP = {
    # Identifiers
    'id': 'id',
    'game_id': 'game_id',
    'player_id': 'player_id',
    'team': 'team_id',
    'player_name': 'player_name',
    'pos': 'position',

    # Passing Stats
    'pass_cmp': 'pass_completions',
    'pass_att': 'pass_attempts',
    'pass_yds': 'pass_yards',
    'pass_td': 'pass_touchdowns',
    'pass_int': 'pass_interceptions',
    'pass_sacked': 'pass_sacked',
    'pass_sacked_yds': 'pass_sacked_yards',
    'pass_long': 'pass_long',
    'pass_rating': 'pass_rating',
    'pass_first_down': 'pass_first_downs',
    'pass_first_down_pct': 'pass_first_down_percentage',
    'pass_target_yds': 'pass_target_yds',
    'pass_tgt_yds_per_att': 'pass_target_yards_per_attempt',
    'pass_air_yds': 'pass_air_yards',
    'pass_air_yds_per_cmp': 'pass_air_yards_per_completion',
    'pass_air_yds_per_att': 'pass_air_yds_per_att',
    'pass_yac': 'pass_yards_after_catch',
    'pass_yac_per_cmp': 'pass_yards_after_catch_per_completion',
    'pass_drops': 'pass_drops',
    'pass_drop_pct': 'pass_drop_percentage',
    'pass_poor_throws': 'pass_poor_throws',
    'pass_poor_throw_pct': 'pass_poor_throw_percentage',
    'pass_blitzed': 'pass_blitzed',
    'pass_hurried': 'pass_hurried',
    'pass_hits': 'pass_hits',
    'pass_pressured': 'pass_pressured',
    'pass_pressured_pct': 'pass_pressured_percentage',

    # Rushing Stats
    'rush_att': 'rush_attempts',
    'rush_yds': 'rush_yards',
    'rush_td': 'rush_touchdowns',
    'rush_long': 'rush_long',
    'rush_scrambles': 'rush_scrambles',
    'rush_scrambles_yds_per_att': 'rush_scrambles_yards_per_attempt',
    'rush_first_down': 'rush_first_downs',
    'rush_yds_before_contact': 'rush_yards_before_contact',
    'rush_yds_bc_per_rush': 'rush_yards_before_contact_per_rush',
    'rush_yac': 'rush_yards_after_catch',
    'rush_yac_per_rush': 'rush_yards_after_catch_per_rush',
    'rush_broken_tackles': 'rush_broken_tackles',
    'rush_broken_tackles_per_rush': 'rush_broken_tackles_per_rush',

    # Receiving Stats
    'targets': 'receiving_targets',
    'rec': 'receiving_receptions',
    'rec_yds': 'receiving_yards',
    'rec_td': 'receiving_touchdowns',
    'rec_long': 'receiving_long',
    'rec_first_down': 'receiving_first_downs',
    'rec_air_yds': 'receiving_air_yards',
    'rec_air_yds_per_rec': 'receiving_air_yards_per_reception',
    'rec_yac': 'receiving_yards_after_catch',
    'rec_yac_per_rec': 'receiving_yards_after_catch_per_reception',
    'rec_adot': 'receiving_average_depth_of_target',
    'rec_broken_tackles': 'receiving_broken_tackles',
    'rec_broken_tackles_per_rec': 'receiving_broken_tackles_per_reception',
    'rec_drops': 'receiving_drops',
    'rec_drop_pct': 'receiving_drop_percentage',
    'rec_target_int': 'receiving_target_interceptions',
    'rec_pass_rating': 'receiving_passer_rating',

    # Fumbles
    'fumbles': 'fumbles_total',
    'fumbles_lost': 'fumbles_lost',
    'fumbles_rec': 'fumbles_recovered',
    'fumbles_rec_yds': 'fumbles_recovered_yards',
    'fumbles_rec_td': 'fumbles_recovered_touchdowns',
    'fumbles_forced': 'fumbles_forced',

    # Defense
    'def_int': 'defensive_interceptions',
    'def_int_yds': 'defensive_interception_yards',
    'def_int_td': 'defensive_interception_touchdowns',
    'def_int_long': 'defensive_interception_long',
    'pass_defended': 'defensive_passes_defended',
    'sacks': 'defensive_sacks',
    'tackles_combined': 'defensive_tackles_combined',
    'tackles_solo': 'defensive_tackles_solo',
    'tackles_assists': 'defensive_tackles_assists',
    'tackles_loss': 'defensive_tackles_loss',
    'qb_hits': 'defensive_qb_hits',
    'def_targets': 'defensive_targets',
    'def_cmp': 'defensive_completions',
    'def_cmp_perc': 'defensive_completion_percentage',
    'def_cmp_yds': 'defensive_completion_yards',
    'def_yds_per_cmp': 'defensive_completion_yards_per_completion',
    'def_yds_per_target': 'defensive_completion_yards_per_target',
    'def_cmp_td': 'defensive_completion_touchdowns',
    'def_pass_rating': 'defensive_pass_rating',
    'def_tgt_yds_per_att': 'defensive_target_yards_per_attempt',
    'def_air_yds': 'defensive_air_yds',
    'def_yac': 'defensive_yards_after_catch',
    'blitzes': 'defensive_blitzes',
    'qb_hurry': 'defensive_qb_hurries',
    'qb_knockdown': 'defensive_qb_knockdowns',
    'pressures': 'defensive_pressures',
    'tackles_missed': 'defensive_tackles_missed',
    'tackles_missed_pct': 'defensive_tackles_missed_percentage',

    # Kicking & Punting
    'xpm': 'extra_points_made',
    'xpa': 'extra_points_attempted',
    'fgm': 'field_goals_made',
    'fga': 'field_goals_attempted',
    'punt': 'punts',
    'punt_yds': 'punt_yards',
    'punt_yds_per_punt': 'punt_yards_per_punt',
    'punt_long': 'punt_long',

    # Kick & Punt Returns
    'kick_ret': 'kick_returns',
    'kick_ret_yds': 'kick_return_yards',
    'kick_ret_yds_per_ret': 'kick_return_yards_per_return',
    'kick_ret_td': 'kick_return_touchdowns',
    'kick_ret_long': 'kick_return_long',
    'punt_ret': 'punt_returns',
    'punt_ret_yds': 'punt_return_yards',
    'punt_ret_yds_per_ret': 'punt_return_yards_per_return',
    'punt_ret_td': 'punt_return_touchdowns',
    'punt_ret_long': 'punt_return_long',

    # Snap Counts
    'offense': 'snapcounts_offense',
    'off_pct': 'snapcounts_offense_percentage',
    'defense': 'snapcounts_defense',
    'def_pct': 'snapcounts_defense_percentage',
    'special_teams': 'snapcounts_special_teams',
    'st_pct': 'snapcounts_special_teams_percentage',
}

class GamePageTransformer():
    def __init__(self, game_info_df, game_stats_df, player_stats_df):
        self.game_info_df = game_info_df
        self.game_stats_df = game_stats_df
        self.player_stats_df = player_stats_df
    
    
    def transform_game_info_df(self) -> pd.DataFrame:
        self._normalize_df('game_info_df', GAME_INFO_COL_MAP)
        self._modify_game_info_features()
        return self.game_info_df
    
    
    def transform_game_stats_df(self) -> pd.DataFrame:
        self._normalize_df('game_stats_df', GAME_STATS_COL_MAP)
        self._modify_game_stats_features()
        return self.game_stats_df


    def transform_player_stats_df(self) -> pd.DataFrame:
        self._normalize_df('player_stats_df', PLAYER_STATS_COL_MAP)
        self._modify_player_stats_features()
        return self.player_stats_df
    
    
    def _normalize_df(self, df_attr: str, col_map: dict) -> None:
        df = getattr(self, df_attr)
        
        for original_col, new_col in col_map.items():
            if original_col not in df.columns:
                df[original_col] = pd.NA

        df = df.rename(columns=col_map)
        df = df[list(col_map.values())]
        
        setattr(self, df_attr, df)


    def _modify_game_info_features(self) -> None:
        attendance_value = self.game_info_df['attendance'].iloc[0]
        
        # --- Attendance Cleaning ---
        if pd.notna(attendance_value):
            # Process the single value
            processed_value = str(attendance_value).replace(',', '')
            if processed_value:
                try:
                    self.game_info_df.loc[0, 'attendance'] = int(float(processed_value))
                except (ValueError, TypeError):
                    self.game_info_df.loc[0, 'attendance'] = None
            else:
                self.game_info_df.loc[0, 'attendance'] = None

        # --- Playoff Game Label ---
        season_year = self.game_info_df['season_year'].iloc[0]
        season_week = self.game_info_df['season_week'].iloc[0]

        playoff_mapping_post2020 = {
            19: 'Wild Card',
            20: 'Divisional',
            21: 'Conference Championship',
            22: 'Superbowl'
        }

        playoff_mapping_pre2021 = {
            18: 'Wild Card',
            19: 'Divisional',
            20: 'Conference Championship',
            21: 'Superbowl'
        }

        playoff_game = None
        if season_year > 2020:
            playoff_game = playoff_mapping_post2020.get(season_week, None)
        else:
            playoff_game = playoff_mapping_pre2021.get(season_week, None)

        self.game_info_df.loc[0, 'playoff_game'] = playoff_game
    
    
    def _modify_game_stats_features(self) -> None:
        # Parse rushing stats into separate columns
        if 'rush_stats_combined' not in self.game_stats_df.columns:
            raise ValueError("Missing expected column: 'rush_stats_combined'")
        split_cols = self.game_stats_df['rush_stats_combined'].str.split('-', expand=True)
        self.game_stats_df['rushing_attempts'] = pd.to_numeric(split_cols[0], errors='coerce')
        self.game_stats_df['rushing_yards'] = pd.to_numeric(split_cols[1], errors='coerce')
        self.game_stats_df['rushing_touchdowns'] = pd.to_numeric(split_cols[2], errors='coerce')
        self.game_stats_df = self.game_stats_df.drop(columns=['rush_stats_combined'])

        # Parse passing stats into separate columns
        if 'passing_stats_combined' not in self.game_stats_df.columns:
            raise ValueError("Missing expected column: 'passing_stats_combined'")
        split_cols = self.game_stats_df['passing_stats_combined'].str.split('-', expand=True)
        self.game_stats_df['passing_attempts'] = pd.to_numeric(split_cols[0], errors='coerce')
        self.game_stats_df['passing_completions'] = pd.to_numeric(split_cols[1], errors='coerce')
        self.game_stats_df['passing_yards'] = pd.to_numeric(split_cols[2], errors='coerce')
        self.game_stats_df['passing_touchdowns'] = pd.to_numeric(split_cols[3], errors='coerce')
        self.game_stats_df['passing_interceptions'] = pd.to_numeric(split_cols[4], errors='coerce')
        self.game_stats_df = self.game_stats_df.drop(columns=['passing_stats_combined'])

        # Parse sack stats into separate columns
        if 'sack_stats_combined' not in self.game_stats_df.columns:
            raise ValueError("Missing expected column: 'sack_stats_combined'")
        split_cols = self.game_stats_df['sack_stats_combined'].str.split('-', expand=True)
        self.game_stats_df['sacks_total'] = pd.to_numeric(split_cols[0], errors='coerce')
        self.game_stats_df['sack_yards'] = pd.to_numeric(split_cols[1], errors='coerce')
        self.game_stats_df = self.game_stats_df.drop(columns=['sack_stats_combined'])

        # Parse fumble stats into separate columns
        if 'fumble_stats_combined' not in self.game_stats_df.columns:
            raise ValueError("Missing expected column: 'fumble_stats_combined'")
        split_cols = self.game_stats_df['fumble_stats_combined'].str.split('-', expand=True)
        self.game_stats_df['fumbles_total'] = pd.to_numeric(split_cols[0], errors='coerce')
        self.game_stats_df['fumbles_lost'] = pd.to_numeric(split_cols[1], errors='coerce')
        self.game_stats_df = self.game_stats_df.drop(columns=['fumble_stats_combined'])

        # Parse penalty stats into separate columns
        if 'penalty_stats_combined' not in self.game_stats_df.columns:
            raise ValueError("Missing expected column: 'penalty_stats_combined'")
        split_cols = self.game_stats_df['penalty_stats_combined'].str.split('-', expand=True)
        self.game_stats_df['penalties_total'] = pd.to_numeric(split_cols[0], errors='coerce')
        self.game_stats_df['penalty_yards'] = pd.to_numeric(split_cols[1], errors='coerce')
        self.game_stats_df = self.game_stats_df.drop(columns=['penalty_stats_combined'])

        # Parse third down stats into separate columns
        if 'third_down_stats_combined' not in self.game_stats_df.columns:
            raise ValueError("Missing expected column: 'third_down_stats_combined'")
        split_cols = self.game_stats_df['third_down_stats_combined'].str.split('-', expand=True)
        self.game_stats_df['third_down_conversions'] = pd.to_numeric(split_cols[0], errors='coerce')
        self.game_stats_df['third_down_attempts'] = pd.to_numeric(split_cols[1], errors='coerce')
        self.game_stats_df = self.game_stats_df.drop(columns=['third_down_stats_combined'])

        # Parse fourth down stats into separate columns
        if 'fourth_down_stats_combined' not in self.game_stats_df.columns:
            raise ValueError("Missing expected column: 'fourth_down_stats_combined'")
        split_cols = self.game_stats_df['fourth_down_stats_combined'].str.split('-', expand=True)
        self.game_stats_df['fourth_down_conversions'] = pd.to_numeric(split_cols[0], errors='coerce')
        self.game_stats_df['fourth_down_attempts'] = pd.to_numeric(split_cols[1], errors='coerce')
        self.game_stats_df = self.game_stats_df.drop(columns=['fourth_down_stats_combined'])


    def _modify_player_stats_features(self) -> None:    
        for col in self.player_stats_df.columns:
            col_data = self.player_stats_df[col]

            if col_data.dtype == object or pd.api.types.is_string_dtype(col_data):
                col_str = col_data.astype(str)

                if col_str.str.contains('%').any():
                    col_str = col_str.str.replace('%', '', regex=False)

                col_str = col_str.replace({'': np.nan, '<NA>': np.nan, 'nan': np.nan})

                self.player_stats_df[col] = col_str.infer_objects(copy=False)

            try:
                self.player_stats_df[col] = self.player_stats_df[col].astype(float)
            except (ValueError, TypeError):
                pass

                
        self.player_stats_df.dropna(subset=['team_id'], inplace=True)
        self.player_stats_df['team_id'] = self.player_stats_df['team_id'].apply(
            lambda x: TEAM_ABR_TO_TEAM_ID_MAP.get(x, x) if x not in TEAM_ABR_TO_TEAM_ID_MAP.values() else x
        )
        
        self.player_stats_df['id'] = self.player_stats_df['player_id'] + '_' + self.player_stats_df['game_id']
         
        self.player_stats_df = self.player_stats_df.convert_dtypes()
