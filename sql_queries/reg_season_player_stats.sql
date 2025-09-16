CREATE OR REPLACE FUNCTION public.populate_all_season_stats()
RETURNS void
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM regular_season_player_stats;

    INSERT INTO regular_season_player_stats (
        id,
        player_id,
        player_name,
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
        punts,
        punt_yards,
        punt_yards_per_punt,
        passer_rating
        -- NOTE: extra_points and field_goals columns exist in the table,
        -- but are not populated here unless you extend the source query.
    )
    SELECT 
        gi.season_year || '_' || gps.player_id || '_' || gps.team_id AS id,
        gps.player_id,
        gps.player_name,
        gi.season_year,
        gps.team_id,
        MAX(gps.position),
        COUNT(DISTINCT gps.game_id),
        COALESCE(SUM(gps.pass_attempts), 0),
        COALESCE(SUM(gps.pass_completions), 0),
        COALESCE(SUM(gps.pass_yards), 0),
        COALESCE(SUM(gps.pass_touchdowns), 0),
        COALESCE(SUM(gps.pass_interceptions), 0),
        COALESCE(SUM(gps.rush_attempts), 0),
        COALESCE(SUM(gps.rush_yards), 0),
        CASE 
            WHEN COALESCE(SUM(gps.rush_attempts), 0) > 0 THEN 
                ROUND((SUM(gps.rush_yards) / SUM(gps.rush_attempts))::NUMERIC, 2)
            ELSE 0 
        END,
        COALESCE(SUM(gps.rush_touchdowns), 0),
        COALESCE(SUM(gps.fumbles_lost), 0),
        COALESCE(SUM(gps.receiving_targets), 0),
        COALESCE(SUM(gps.receiving_receptions), 0),
        COALESCE(SUM(gps.receiving_yards), 0),
        COALESCE(SUM(gps.receiving_touchdowns), 0),
        CASE 
            WHEN COALESCE(SUM(gps.receiving_receptions), 0) > 0 THEN 
                ROUND((SUM(gps.receiving_yards) / SUM(gps.receiving_receptions))::NUMERIC, 2)
            ELSE 0 
        END,
        COALESCE(SUM(gps.defensive_interceptions), 0),
        COALESCE(SUM(gps.defensive_passes_defended), 0),
        COALESCE(SUM(gps.defensive_sacks), 0),
        COALESCE(SUM(gps.defensive_tackles_combined), 0),
        COALESCE(SUM(gps.defensive_tackles_loss), 0),
        COALESCE(SUM(gps.defensive_qb_hits), 0),
        COALESCE(SUM(gps.defensive_pressures), 0),
        COALESCE(SUM(gps.punts), 0),
        COALESCE(SUM(gps.punt_yards), 0),
        CASE 
            WHEN COALESCE(SUM(gps.punts), 0) > 0 THEN 
                ROUND((SUM(gps.punt_yards) / SUM(gps.punts))::NUMERIC, 2)
            ELSE 0 
        END,
        CASE 
            WHEN COALESCE(SUM(gps.pass_attempts), 0) > 0 THEN
                ROUND((
				    (
				        GREATEST(0, LEAST((((SUM(gps.pass_completions)::numeric / NULLIF(SUM(gps.pass_attempts), 0)) - 0.3) * 5), 2.375)) +
				        GREATEST(0, LEAST((((SUM(gps.pass_yards)::numeric       / NULLIF(SUM(gps.pass_attempts), 0)) - 3)   * 0.25), 2.375)) +
				        GREATEST(0, LEAST((( SUM(gps.pass_touchdowns)::numeric / NULLIF(SUM(gps.pass_attempts), 0)) * 20), 2.375)) +
				        GREATEST(0, LEAST(( 2.375 - ((SUM(gps.pass_interceptions)::numeric / NULLIF(SUM(gps.pass_attempts), 0)) * 25)), 2.375))
				    ) / 6.0 * 100.0
				)::numeric, 1)
            ELSE 0.0
        END
    FROM game_player_stats gps
    JOIN game_info gi ON gps.game_id = gi.game_id
    WHERE gi.playoff_game IS NULL
    GROUP BY gps.player_id, gps.player_name, gi.season_year, gps.team_id;
END;
$$;

ALTER FUNCTION public.populate_all_season_stats()
    OWNER TO postgres;
