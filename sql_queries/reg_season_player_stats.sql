CREATE OR REPLACE FUNCTION public.populate_all_season_stats()
RETURNS void
LANGUAGE 'plpgsql'
COST 100
VOLATILE PARALLEL UNSAFE
AS $BODY$
BEGIN
    DELETE FROM regular_season_player_stats;

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
        punts,
        punt_yards,
        punt_yards_per_punt
    )
    SELECT 
        gps.player_id,
        gi.season_year,
        gps.team_id,
        MAX(gps.position), -- choose a representative position for the season
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
        END
    FROM game_player_stats gps
    JOIN game_info gi ON gps.game_id = gi.game_id
    WHERE gi.season_week <= 18
    GROUP BY gps.player_id, gi.season_year, gps.team_id;
END;
$BODY$;

ALTER FUNCTION public.populate_all_season_stats()
    OWNER TO postgres;