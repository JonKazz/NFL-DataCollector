import psycopg2
import sqlalchemy
from sqlalchemy.dialects.postgresql import insert
from nfl_datacollector.config import DatabaseConfig

class DatabaseLoader:
    def __init__(self, config: DatabaseConfig):
        self.config = config
        self.engine = None

    def get_connection(self):
        return psycopg2.connect(
            host=self.config.hostname,
            dbname=self.config.database,
            user=self.config.username,
            password=self.config.password,
            port=self.config.port
        )

    def get_engine(self):
        if self.engine is None:
            self.engine = sqlalchemy.create_engine(self.config.get_connection_string())
        return self.engine
    
    
    def get_all_game_urls(self) -> list[str]:
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT url FROM game_info;")
                    rows = cur.fetchall()
                    return [row[0] for row in rows]
        except Exception as e:
            print("Error fetching URLs from game_info:", e)
            return []
    
    
    def get_all_player_urls(self) -> list[str]:
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT url FROM player_profiles;")
                    rows = cur.fetchall()
                    return [row[0] for row in rows]
        except Exception as e:
            print("Error fetching URLs from player_profiles:", e)
            return []
    
    
    def create_table(self, query: str, table_name: str):
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(query)
                    print(f"{table_name} table created successfully")
        except Exception as e:
            print(f"Error creating {table_name} table:", e)
    
    def create_season_team_info_table(self):
        query = '''
        DROP TABLE IF EXISTS season_team_info;
        CREATE TABLE season_team_info (
            id VARCHAR(50) PRIMARY KEY NOT NULL,
            team_id VARCHAR(50) NOT NULL,
            year INT NOT NULL,
            name VARCHAR(100) NOT NULL,
            city VARCHAR(100) NOT NULL,
            stadium VARCHAR(500),
            wins INT,
            losses INT,
            ties INT,
            division_rank INT,
            division VARCHAR(100),
            playoffs VARCHAR(100),
            points_for INT NOT NULL,
            points_against INT NOT NULL,
            coach VARCHAR(100),
            off_coordinator VARCHAR(500),
            def_coordinator VARCHAR(500),
            off_scheme VARCHAR(500),
            def_alignment VARCHAR(500),
            logo VARCHAR(300) NOT NULL
        );
        '''
        self.create_table(query, 'season_team_info')
    
    
    def create_game_info_table(self):
        query = '''
        DROP TABLE IF EXISTS game_info;
        CREATE TABLE game_info (
            game_id VARCHAR(50) NOT NULL,
            season_week INT NOT NULL,
            season_year INT NOT NULL,
            playoff_game VARCHAR(100),
            date VARCHAR(30) NOT NULL,
            away_team_id VARCHAR(10) NOT NULL,
            home_team_id VARCHAR(10) NOT NULL,
            winning_team_id VARCHAR(10) NOT NULL,
            home_team_record VARCHAR(10) NOT NULL,
            away_team_record VARCHAR(10) NOT NULL,
            away_points INT NOT NULL,
            home_points INT NOT NULL,
            overtime BOOLEAN NOT NULL,
            won_toss VARCHAR(100),
            roof_type VARCHAR(100),
            surface_type VARCHAR(100),
            game_duration VARCHAR(100),
            weather VARCHAR(100),
            vegas_line VARCHAR(100),
            over_under VARCHAR(100),
            attendance INT,
            start_time VARCHAR(100),
            stadium VARCHAR(100),
            url VARCHAR(200) NOT NULL,
            PRIMARY KEY (game_id)
        );
        '''
        self.create_table(query, 'game_info')
    
    
    def create_game_stats_table(self):
        query = '''
        DROP TABLE IF EXISTS game_stats;
        CREATE TABLE game_stats (
            game_id VARCHAR(50) NOT NULL,
            team_id VARCHAR(10) NOT NULL,
            first_downs_total INT,
            net_passing_yards INT,
            total_yards INT,
            turnovers INT,
            time_of_possession VARCHAR(20),
            points_q1 INT NOT NULL,
            points_q2 INT NOT NULL,
            points_q3 INT NOT NULL,
            points_q4 INT NOT NULL,
            points_overtime INT NOT NULL,
            points_total INT NOT NULL,
            rushing_attempts INT,
            rushing_yards INT,
            rushing_touchdowns INT,
            passing_attempts INT,
            passing_completions INT,
            passing_yards INT,
            passing_touchdowns INT,
            passing_interceptions INT,
            sacks_total INT,
            sack_yards INT,
            fumbles_total INT,
            fumbles_lost INT,
            penalties_total INT,
            penalty_yards INT,
            third_down_conversions INT,
            third_down_attempts INT,
            fourth_down_conversions INT,
            fourth_down_attempts INT,
            PRIMARY KEY (game_id, team_id)
        );
        '''
        self.create_table(query, 'game_stats')
    
    
    def create_game_player_stats_table(self):
        query = '''
        DROP TABLE IF EXISTS game_player_stats;
        CREATE TABLE game_player_stats (
            game_id VARCHAR(50) NOT NULL,
            player_id VARCHAR(50) NOT NULL,
            team_id VARCHAR(50) NOT NULL,
            position VARCHAR(10),
            pass_completions REAL,
            pass_attempts REAL,
            pass_yards REAL,
            pass_touchdowns REAL,
            pass_interceptions REAL,
            pass_sacked REAL,
            pass_sacked_yards REAL,
            pass_long REAL,
            pass_rating REAL,
            pass_first_downs REAL,
            pass_first_down_percentage REAL,
            pass_target_yds REAL,
            pass_target_yards_per_attempt REAL,
            pass_air_yards REAL,
            pass_air_yards_per_completion REAL,
            pass_air_yds_per_att REAL,
            pass_yards_after_catch REAL,
            pass_yards_after_catch_per_completion REAL,
            pass_drops REAL,
            pass_drop_percentage REAL,
            pass_poor_throws REAL,
            pass_poor_throw_percentage REAL,
            pass_blitzed REAL,
            pass_hurried REAL,
            pass_hits REAL,
            pass_pressured REAL,
            pass_pressured_percentage REAL,
            rush_attempts REAL,
            rush_yards REAL,
            rush_touchdowns REAL,
            rush_long REAL,
            rush_scrambles REAL,
            rush_scrambles_yards_per_attempt REAL,
            rush_first_downs REAL,
            rush_yards_before_contact REAL,
            rush_yards_before_contact_per_rush REAL,
            rush_yards_after_catch REAL,
            rush_yards_after_catch_per_rush REAL,
            rush_broken_tackles REAL,
            rush_broken_tackles_per_rush REAL,
            receiving_targets REAL,
            receiving_receptions REAL,
            receiving_yards REAL,
            receiving_touchdowns REAL,
            receiving_long REAL,
            receiving_first_downs REAL,
            receiving_air_yards REAL,
            receiving_air_yards_per_reception REAL,
            receiving_yards_after_catch REAL,
            receiving_yards_after_catch_per_reception REAL,
            receiving_average_depth_of_target REAL,
            receiving_broken_tackles REAL,
            receiving_broken_tackles_per_reception REAL,
            receiving_drops REAL,
            receiving_drop_percentage REAL,
            receiving_target_interceptions REAL,
            receiving_passer_rating REAL,
            fumbles_total REAL,
            fumbles_lost REAL,
            fumbles_recovered REAL,
            fumbles_recovered_yards REAL,
            fumbles_recovered_touchdowns REAL,
            fumbles_forced REAL,
            defensive_interceptions REAL,
            defensive_interception_yards REAL,
            defensive_interception_touchdowns REAL,
            defensive_interception_long REAL,
            defensive_passes_defended REAL,
            defensive_sacks REAL,
            defensive_tackles_combined REAL,
            defensive_tackles_solo REAL,
            defensive_tackles_assists REAL,
            defensive_tackles_loss REAL,
            defensive_qb_hits REAL,
            defensive_targets REAL,
            defensive_completions REAL,
            defensive_completion_percentage REAL,
            defensive_completion_yards REAL,
            defensive_completion_yards_per_completion REAL,
            defensive_completion_yards_per_target REAL,
            defensive_completion_touchdowns REAL,
            defensive_pass_rating REAL,
            defensive_target_yards_per_attempt REAL,
            defensive_air_yds REAL,
            defensive_yards_after_catch REAL,
            defensive_blitzes REAL,
            defensive_qb_hurries REAL,
            defensive_qb_knockdowns REAL,
            defensive_pressures REAL,
            defensive_tackles_missed REAL,
            defensive_tackles_missed_percentage REAL,
            extra_points_made REAL,
            extra_points_attempted REAL,
            field_goals_made REAL,
            field_goals_attempted REAL,
            punts REAL,
            punt_yards REAL,
            punt_yards_per_punt REAL,
            punt_long REAL,
            kick_returns REAL,
            kick_return_yards REAL,
            kick_return_yards_per_return REAL,
            kick_return_touchdowns REAL,
            kick_return_long REAL,
            punt_returns REAL,
            punt_return_yards REAL,
            punt_return_yards_per_return REAL,
            punt_return_touchdowns REAL,
            punt_return_long REAL,
            snapcounts_offense REAL,
            snapcounts_offense_percentage REAL,
            snapcounts_defense REAL,
            snapcounts_defense_percentage REAL,
            snapcounts_special_teams REAL,
            snapcounts_special_teams_percentage REAL,
            PRIMARY KEY (game_id, player_id)
        );
        '''
        self.create_table(query, 'game_player_stats')
    
    
    def create_player_profiles_table(self):
        query = '''
        DROP TABLE IF EXISTS player_profiles;
        CREATE TABLE player_profiles (
            player_id VARCHAR(50) NOT NULL,
            img VARCHAR(300),
            name VARCHAR(100) NOT NULL,
            height VARCHAR(50) NOT NULL,
            weight VARCHAR(50),
            dob VARCHAR(50) NOT NULL,
            college VARCHAR(100) NOT NULL,
            url VARCHAR(200) NOT NULL,
            PRIMARY KEY (player_id)
        )
        '''
        self.create_table(query, 'player_profiles')
    
    def create_game_drives_table(self):
        query = '''
        DROP TABLE IF EXISTS game_drives;
        CREATE TABLE game_drives (
            id SERIAL PRIMARY KEY,
            game_id VARCHAR(50) NOT NULL,
            team_id VARCHAR(10) NOT NULL,
            drive_num VARCHAR(10),
            quarter VARCHAR(10),
            time_start VARCHAR(20),
            start_at VARCHAR(50),
            plays VARCHAR(100),
            time_total VARCHAR(20),
            net_yds VARCHAR(20),
            end_event VARCHAR(100),
            opposing_touchdown BOOLEAN DEFAULT FALSE,
            points_scored INTEGER DEFAULT 0,
            FOREIGN KEY (game_id) REFERENCES game_info(game_id) ON DELETE CASCADE
        );
        
        -- Create index for better query performance
        CREATE INDEX idx_game_drives_game_id ON game_drives(game_id);
        '''
        self.create_table(query, 'game_drives')
    
    
    def create_season_info_table(self):
        query = '''
        DROP TABLE IF EXISTS season_info;
        CREATE TABLE season_info (
            season_year INT PRIMARY KEY,
            url VARCHAR(200),
            sb_champ VARCHAR(100),
            mvp_id VARCHAR(50),
            opoy_id VARCHAR(50),
            dpoy_id VARCHAR(50),
            oroy_id VARCHAR(50),
            droy_id VARCHAR(50),
        );
        '''
        self.create_table(query, 'season_info')
    

    def create_ap_team_votes_table(self):
        query = '''
        DROP TABLE IF EXISTS ap_team_votes;
        CREATE TABLE ap_team_votes (
            season_year INT NOT NULL,
            player_id   VARCHAR(10) NOT NULL,
            team        VARCHAR(10) NOT NULL,
            position    VARCHAR(10) NOT NULL,
            ap_team     INT NOT NULL,
            PRIMARY KEY (season_year, player_id)
        );
        '''
        self.create_table(query, 'ap_team_votes')

    
    def insert_df(self, df, table_name):
        engine = self.get_engine()
        
        with engine.begin() as conn:
            meta = sqlalchemy.MetaData()
            table = sqlalchemy.Table(table_name, meta, autoload_with=engine)
            
            for _, row in df.iterrows():
                stmt = insert(table).values(**row.to_dict())
                
                # Handle conflicts based on table type
                if table_name == 'game_stats':
                    stmt = stmt.on_conflict_do_nothing(index_elements=['game_id', 'team_id'])
                elif table_name == 'game_info':
                    stmt = stmt.on_conflict_do_nothing(index_elements=['game_id'])
                elif table_name == 'game_player_stats':
                    stmt = stmt.on_conflict_do_nothing(index_elements=['game_id', 'player_id'])
                elif table_name == 'player_profiles':
                    stmt = stmt.on_conflict_do_nothing(index_elements=['player_id'])
                elif table_name == 'season_team_info':
                    stmt = stmt.on_conflict_do_nothing(index_elements=['id'])
                elif table_name == 'game_drives':
                    stmt = stmt.on_conflict_do_nothing(index_elements=['game_id', 'team_id', 'drive_num'])
                elif table_name == 'season_info':
                    stmt = stmt.on_conflict_do_nothing(index_elements=['season_year'])
                elif table_name == 'ap_team_votes':
                    stmt = stmt.on_conflict_do_nothing(index_elements=['season_year', 'player_id'])
                else:
                    raise ValueError(f'Invalid table name: {table_name}')
                
                result = conn.execute(stmt)
                
                # Log insertion results for game_info table
                if table_name == 'game_info':
                    if result.rowcount == 0:
                        print(f"Skipped duplicate for game_id={row['game_id']}")
                    else:
                        print(f"Inserted row for game_id={row['game_id']}")
                
                if table_name == 'season_team_info':
                    if result.rowcount == 0:
                        print(f"Skipped duplicate for id={row['id']}")
                    else:
                        print(f"Inserted row for id={row['id']}")

                if table_name == 'player_profiles':
                    if result.rowcount == 0:
                        print(f"Skipped duplicate for player_id={row['player_id']}")
                    else:
                        print(f"Inserted row for player_id={row['player_id']}")
                
                if table_name == 'season_info':
                    if result.rowcount == 0:
                        print(f"Skipped duplicate for season_info year={row['season_year']}")
                    else:
                        print(f"Inserted row for season_info year={row['season_year']}")
                
                if table_name == 'ap_team_votes':
                    if result.rowcount == 0:
                        print(f"Skipped duplicate for ap_team_votes year={row['season_year']}")
                    else:
                        print(f"Inserted row for ap_team_votes year={row['season_year']}")
    
    def insert_game_stats_df(self, df):
        self.insert_df(df, 'game_stats')
    
    def insert_game_player_stats_df(self, df):
        self.insert_df(df, 'game_player_stats')
    
    def insert_game_info_df(self, df):
        self.insert_df(df, 'game_info')
    
    def insert_player_profile_df(self, df):
        self.insert_df(df, 'player_profiles')
    
    def insert_season_team_info_df(self, df):
        self.insert_df(df, 'season_team_info')
    
    def insert_game_drives_df(self, df):
        self.insert_df(df, 'game_drives')
        
    def insert_season_info_df(self, df):
        self.insert_df(df, 'season_info')
    
    def insert_ap_team_votes_df(self, df):
        self.insert_df(df, 'ap_team_votes')
    
    def create_all_tables(self):
        print("Creating all database tables...")
        self.create_game_info_table()
        self.create_game_stats_table()
        self.create_game_player_stats_table()
        self.create_player_profiles_table()
        self.create_season_team_info_table()
        self.create_game_drives_table()
        self.create_season_info_table()
        self.create_ap_team_votes_table()
        print("All tables created successfully!")


# Legacy function wrappers for backward compatibility
def get_db_connection(loader: DatabaseLoader):
    return loader.get_connection()

def get_all_db_game_urls(loader: DatabaseLoader) -> list[str]:
    return loader.get_all_game_urls()

def get_all_db_player_urls(loader: DatabaseLoader) -> list[str]:
    return loader.get_all_player_urls()


def create_table(query: str, table_name: str, loader: DatabaseLoader):
    loader.create_table(query, table_name)

def create_game_info_table(loader: DatabaseLoader):
    loader.create_game_info_table()

def create_game_stats_table(loader: DatabaseLoader):
    loader.create_game_stats_table()

def create_game_player_stats_table(loader: DatabaseLoader):
    loader.create_game_player_stats_table()

def create_player_profiles_table(loader: DatabaseLoader):
    loader.create_player_profiles_table()
    
def create_game_drives_table(loader: DatabaseLoader):
    loader.create_game_drives_table()

def create_season_info_table(loader: DatabaseLoader):
    loader.create_season_info_table()

def create_ap_team_votes_table(loader: DatabaseLoader):
    loader.create_ap_team_votes_table()
    
    
def insert_df(df, table_name, loader: DatabaseLoader):
    loader.insert_df(df, table_name)

def insert_game_stats_df(df, loader: DatabaseLoader):
    loader.insert_df(df, 'game_stats')

def insert_game_player_stats_df(df, loader: DatabaseLoader):
    loader.insert_df(df, 'game_player_stats')

def insert_game_info_df(df, loader: DatabaseLoader):
    loader.insert_df(df, 'game_info')

def insert_player_profile_df(df, loader: DatabaseLoader):
    loader.insert_df(df, 'player_profiles')

def insert_game_drives_df(df, loader: DatabaseLoader):
    loader.insert_df(df, 'game_drives')
    
def insert_season_info_df(df, loader: DatabaseLoader):
    loader.insert_df(df, 'season_info')

def insert_ap_team_votes_df(df, loader: DatabaseLoader):
    loader.insert_df(df, 'ap_team_votes')