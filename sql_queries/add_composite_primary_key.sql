-- Add composite primary key constraint to game_stats table
-- This will ensure the table has the proper constraint for ON CONFLICT handling

-- First, check if the constraint already exists
SELECT 
    tc.constraint_name, 
    tc.table_name, 
    kcu.column_name, 
    tc.constraint_type
FROM information_schema.table_constraints tc
JOIN information_schema.key_column_usage kcu 
    ON tc.constraint_name = kcu.constraint_name
WHERE tc.table_name = 'game_stats' 
    AND tc.constraint_type = 'PRIMARY KEY';

-- If no primary key exists, add it
-- Note: This will fail if there are duplicate (game_id, team_id) combinations
ALTER TABLE game_stats 
ADD CONSTRAINT game_stats_pkey PRIMARY KEY (game_id, team_id);

-- Verify the constraint was added
SELECT 
    tc.constraint_name, 
    tc.table_name, 
    kcu.column_name, 
    tc.constraint_type
FROM information_schema.table_constraints tc
JOIN information_schema.key_column_usage kcu 
    ON tc.constraint_name = kcu.constraint_name
WHERE tc.table_name = 'game_stats' 
    AND tc.constraint_type = 'PRIMARY KEY';
