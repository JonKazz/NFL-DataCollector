CREATE TABLE public.regular_season_player_stats (
    id VARCHAR(100) PRIMARY KEY, -- season_year + '_' + player_id + '_' + team_id

    player_id VARCHAR(20) NOT NULL,
    player_name VARCHAR(200) NOT NULL,
    season_year INT NOT NULL,
    team_id VARCHAR(10) NOT NULL,
    position VARCHAR(10),
    games_played INT DEFAULT 0,

    -- Passing stats
    passing_attempts INT DEFAULT 0,
    passing_completions INT DEFAULT 0,
    passing_yards INT DEFAULT 0,
    passing_touchdowns INT DEFAULT 0,
    passing_interceptions INT DEFAULT 0,
    passer_rating NUMERIC(5,1) DEFAULT 0.0,

    -- Rushing stats
    rushing_attempts INT DEFAULT 0,
    rushing_yards INT DEFAULT 0,
    rushing_yards_per_attempt NUMERIC(6,2) DEFAULT 0.00,
    rushing_touchdowns INT DEFAULT 0,

    -- Fumbles
    fumbles_total INT DEFAULT 0, -- you added this in entity (not in the function)
    fumbles_lost INT DEFAULT 0,

    -- Receiving stats
    receiving_targets INT DEFAULT 0,
    receiving_receptions INT DEFAULT 0,
    receiving_yards INT DEFAULT 0,
    receiving_touchdowns INT DEFAULT 0,
    receiving_yards_per_reception NUMERIC(6,2) DEFAULT 0.00,

    -- Defensive stats
    defensive_interceptions INT DEFAULT 0,
    defensive_passes_defended INT DEFAULT 0,
    defensive_sacks INT DEFAULT 0,
    defensive_tackles_combined INT DEFAULT 0,
    defensive_tackles_loss INT DEFAULT 0,
    defensive_qb_hits INT DEFAULT 0,
    defensive_pressures INT DEFAULT 0,

    -- Kicking stats (not in the function, but in your entity)
    extra_points_made INT DEFAULT 0,
    extra_points_attempted INT DEFAULT 0,
    field_goals_made INT DEFAULT 0,
    field_goals_attempted INT DEFAULT 0,

    -- Punting stats
    punts INT DEFAULT 0,
    punt_yards INT DEFAULT 0,
    punt_yards_per_punt NUMERIC(6,2) DEFAULT 0.00
);
