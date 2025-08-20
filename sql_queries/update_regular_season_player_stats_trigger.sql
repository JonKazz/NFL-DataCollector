CREATE OR REPLACE FUNCTION public.update_regular_season_player_stats()
RETURNS trigger
LANGUAGE 'plpgsql'
AS $BODY$
DECLARE
    v_season_year INTEGER;
    v_team_id VARCHAR(10);
    v_position VARCHAR(10);
BEGIN
    -- Get season year of the game being inserted/updated
    SELECT EXTRACT(YEAR FROM gi.date::DATE)
    INTO v_season_year
    FROM game_info gi
    WHERE gi.game_id = NEW.game_id;

    -- Get latest team_id and position for this player-season-team
    SELECT gps2.team_id, gps2.position
    INTO v_team_id, v_position
    FROM game_player_stats gps2
    JOIN game_info gi2 ON gps2.game_id = gi2.game_id
    WHERE gps2.player_id = NEW.player_id
      AND EXTRACT(YEAR FROM gi2.date::DATE) = v_season_year
      AND gi2.season_week <= 18
    ORDER BY gi2.date DESC, gps2.game_id DESC
    LIMIT 1;

    -- Upsert logic: insert or update the row
    INSERT INTO regular_season_player_stats (
        player_id,
        season_year,
        team_id,
        position,
        games_played,
        passing_attempts,
        passing_completions,
        passing_yards,
        passing_touchdowns,
        passing_interceptions,
        rushing_attempts,
        rushing_yards,
        rushing_yards_per_attempt,
        rushing_touchdowns,
        fumbles_lost,
        receiving_targets,
        receiving_receptions,
        receiving_yards,
        receiving_touchdowns,
        receiving_yards_per_reception,
        defensive_interceptions,
        defensive_passes_defended,
        defensive_sacks,
        defensive_tackles_combined,
        defensive_tackles_loss,
        defensive_qb_hits,
        defensive_pressures,
        extra_points_made,
        extra_points_attempted,
        field_goals_made,
        field_goals_attempted,
        punts,
        punt_yards,
        punt_yards_per_punt,
        updated_at
    )
    SELECT 
        gps.player_id,
        v_season_year,
        gps.team_id,
        v_position,
        COUNT(DISTINCT gps.game_id),
        COALESCE(SUM(gps.pass_attempts), 0),
        COALESCE(SUM(gps.pass_completions), 0),
        COALESCE(SUM(gps.pass_yards), 0),
        COALESCE(SUM(gps.pass_touchdowns), 0),
        COALESCE(SUM(gps.pass_interceptions), 0),
        COALESCE(SUM(gps.rush_attempts), 0),
        COALESCE(SUM(gps.rush_yards), 0),
        CASE 
            WHEN SUM(gps.rush_attempts) > 0 THEN 
                ROUND(SUM(gps.rush_yards)::NUMERIC / SUM(gps.rush_attempts), 1)
            ELSE 0 
        END,
        COALESCE(SUM(gps.rush_touchdowns), 0),
        COALESCE(SUM(gps.fumbles_lost), 0),
        COALESCE(SUM(gps.receiving_targets), 0),
        COALESCE(SUM(gps.receiving_receptions), 0),
        COALESCE(SUM(gps.receiving_yards), 0),
        COALESCE(SUM(gps.receiving_touchdowns), 0),
        CASE 
            WHEN SUM(gps.receiving_receptions) > 0 THEN 
                ROUND(SUM(gps.receiving_yards)::NUMERIC / SUM(gps.receiving_receptions), 1)
            ELSE 0 
        END,
        COALESCE(SUM(gps.defensive_interceptions), 0),
        COALESCE(SUM(gps.defensive_passes_defended), 0),
        COALESCE(SUM(gps.defensive_sacks), 0),
        COALESCE(SUM(gps.defensive_tackles_combined), 0),
        COALESCE(SUM(gps.defensive_tackles_loss), 0),
        COALESCE(SUM(gps.defensive_qb_hits), 0),
        COALESCE(SUM(gps.defensive_pressures), 0),
        COALESCE(SUM(gps.extra_points_made), 0),
        COALESCE(SUM(gps.extra_points_attempted), 0),
        COALESCE(SUM(gps.field_goals_made), 0),
        COALESCE(SUM(gps.field_goals_attempted), 0),
        COALESCE(SUM(gps.punts), 0),
        COALESCE(SUM(gps.punt_yards), 0),
        CASE 
            WHEN SUM(gps.punts) > 0 THEN 
                ROUND(SUM(gps.punt_yards)::NUMERIC / SUM(gps.punts), 1)
            ELSE 0 
        END,
        CURRENT_TIMESTAMP
    FROM game_player_stats gps
    JOIN game_info gi ON gps.game_id = gi.game_id
    WHERE gps.player_id = NEW.player_id
      AND gps.team_id = v_team_id
      AND EXTRACT(YEAR FROM gi.date::DATE) = v_season_year
      AND gi.season_week <= 18
    GROUP BY gps.player_id, gps.team_id
    ON CONFLICT (player_id, season_year, team_id) DO UPDATE
    SET
        games_played = EXCLUDED.games_played,
        passing_attempts = EXCLUDED.passing_attempts,
        passing_completions = EXCLUDED.passing_completions,
        passing_yards = EXCLUDED.passing_yards,
        passing_touchdowns = EXCLUDED.passing_touchdowns,
        passing_interceptions = EXCLUDED.passing_interceptions,
        rushing_attempts = EXCLUDED.rushing_attempts,
        rushing_yards = EXCLUDED.rushing_yards,
        rushing_yards_per_attempt = EXCLUDED.rushing_yards_per_attempt,
        rushing_touchdowns = EXCLUDED.rushing_touchdowns,
        fumbles_lost = EXCLUDED.fumbles_lost,
        receiving_targets = EXCLUDED.receiving_targets,
        receiving_receptions = EXCLUDED.receiving_receptions,
        receiving_yards = EXCLUDED.receiving_yards,
        receiving_touchdowns = EXCLUDED.receiving_touchdowns,
        receiving_yards_per_reception = EXCLUDED.receiving_yards_per_reception,
        defensive_interceptions = EXCLUDED.defensive_interceptions,
        defensive_passes_defended = EXCLUDED.defensive_passes_defended,
        defensive_sacks = EXCLUDED.defensive_sacks,
        defensive_tackles_combined = EXCLUDED.defensive_tackles_combined,
        defensive_tackles_loss = EXCLUDED.defensive_tackles_loss,
        defensive_qb_hits = EXCLUDED.defensive_qb_hits,
        defensive_pressures = EXCLUDED.defensive_pressures,
        extra_points_made = EXCLUDED.extra_points_made,
        extra_points_attempted = EXCLUDED.extra_points_attempted,
        field_goals_made = EXCLUDED.field_goals_made,
        field_goals_attempted = EXCLUDED.field_goals_attempted,
        punts = EXCLUDED.punts,
        punt_yards = EXCLUDED.punt_yards,
        punt_yards_per_punt = EXCLUDED.punt_yards_per_punt,
        updated_at = CURRENT_TIMESTAMP,
        -- Only update position if it changed
        position = CASE 
                      WHEN regular_season_player_stats.position <> EXCLUDED.position THEN EXCLUDED.position 
                      ELSE regular_season_player_stats.position 
                  END;

    RETURN NEW;
END;
$BODY$;

ALTER FUNCTION public.update_regular_season_player_stats()
OWNER TO postgres;
