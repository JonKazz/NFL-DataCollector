DROP TABLE IF EXISTS regular_season_player_stats;

CREATE TABLE regular_season_player_stats (
    player_id VARCHAR(50) NOT NULL,
    season_year INTEGER NOT NULL,
    team_id VARCHAR(10) NOT NULL,
    position VARCHAR(10) NOT NULL,
    games_played INTEGER NOT NULL,

    -- Passing stats
    passing_attempts INTEGER DEFAULT 0,
    passing_completions INTEGER DEFAULT 0,
    passing_yards INTEGER DEFAULT 0,
    passing_touchdowns INTEGER DEFAULT 0,
    passing_interceptions INTEGER DEFAULT 0,

    -- Rushing stats
    rushing_attempts INTEGER DEFAULT 0,
    rushing_yards INTEGER DEFAULT 0,
    rushing_yards_per_attempt DECIMAL(4,1) DEFAULT 0.0,
    rushing_touchdowns INTEGER DEFAULT 0,

    -- Fumbles
    fumbles_lost INTEGER DEFAULT 0,

    -- Receiving stats
    receiving_targets INTEGER DEFAULT 0,
    receiving_receptions INTEGER DEFAULT 0,
    receiving_yards INTEGER DEFAULT 0,
    receiving_touchdowns INTEGER DEFAULT 0,
    receiving_yards_per_reception DECIMAL(4,1) DEFAULT 0.0,

    -- Defensive stats
    defensive_interceptions INTEGER DEFAULT 0,
    defensive_passes_defended INTEGER DEFAULT 0,
    defensive_sacks INTEGER DEFAULT 0,
    defensive_tackles_combined INTEGER DEFAULT 0,
    defensive_tackles_loss INTEGER DEFAULT 0,
    defensive_qb_hits INTEGER DEFAULT 0,
    defensive_pressures INTEGER DEFAULT 0,


    -- Kicking stats
    extra_points_made INTEGER DEFAULT 0,
    extra_points_attempted INTEGER DEFAULT 0,
    field_goals_made INTEGER DEFAULT 0,
    field_goals_attempted INTEGER DEFAULT 0,

    -- Punting stats
    punts INTEGER DEFAULT 0,
    punt_yards INTEGER DEFAULT 0,
    punt_yards_per_punt DECIMAL(4,1) DEFAULT 0.0,

    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Composite primary key
    PRIMARY KEY (player_id, season_year, team_id)
);

CREATE INDEX IF NOT EXISTS idx_regular_season_player_stats_team 
    ON regular_season_player_stats(team_id);

CREATE INDEX IF NOT EXISTS idx_regular_season_player_stats_season_year 
    ON regular_season_player_stats(season_year);
