-- IPL CRICKET ANALYTICS - SQL QUERIES
-- ====================================

-- 1. BASIC STATISTICS
SELECT 
    COUNT(DISTINCT match_id) as total_matches,
    COUNT(DISTINCT batting_team) as total_teams,
    COUNT(DISTINCT venue) as total_venues,
    COUNT(DISTINCT city) as total_cities
FROM matches;

-- 2. TOP 10 TEAMS BY MATCHES PLAYED
SELECT 
    batting_team as team,
    COUNT(*) as matches_played
FROM matches
GROUP BY batting_team
ORDER BY matches_played DESC
LIMIT 10;

-- 3. TOP 10 PLAYERS - PLAYER OF MATCH AWARDS
SELECT 
    player_of_match as player,
    COUNT(*) as awards
FROM matches
WHERE player_of_match IS NOT NULL
GROUP BY player_of_match
ORDER BY awards DESC
LIMIT 10;

-- 4. TOP 10 VENUES BY MATCHES HOSTED
SELECT 
    venue,
    COUNT(*) as matches,
    COUNT(DISTINCT city) as cities
FROM matches
WHERE venue IS NOT NULL
GROUP BY venue
ORDER BY matches DESC
LIMIT 10;

-- 5. TOP 10 CITIES BY MATCHES HOSTED
SELECT 
    city,
    COUNT(*) as matches,
    COUNT(DISTINCT venue) as venues
FROM matches
WHERE city IS NOT NULL
GROUP BY city
ORDER BY matches DESC
LIMIT 10;

-- 6. MATCHES PER YEAR
SELECT 
    CAST(SUBSTR(date, 1, 4) AS INTEGER) as year,
    COUNT(*) as matches
FROM matches
GROUP BY year
ORDER BY year;

-- 7. TOSS DECISION ANALYSIS
SELECT 
    toss_decision,
    COUNT(*) as count,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM matches), 2) as percentage
FROM matches
WHERE toss_decision IS NOT NULL
GROUP BY toss_decision;

-- 8. TOSS WINNER ANALYSIS (TOP 10)
SELECT 
    toss_winner,
    COUNT(*) as toss_wins
FROM matches
WHERE toss_winner IS NOT NULL
GROUP BY toss_winner
ORDER BY toss_wins DESC
LIMIT 10;

-- 9. DELIVERIES STATISTICS
SELECT 
    COUNT(*) as total_deliveries,
    SUM(runs_total) as total_runs,
    SUM(runs_extras) as total_extras,
    COUNT(DISTINCT match_id) as matches_in_deliveries,
    COUNT(DISTINCT batter) as unique_batters,
    COUNT(DISTINCT bowler) as unique_bowlers
FROM deliveries;

-- 10. TOP 10 BATTERS BY RUNS SCORED
SELECT 
    batter,
    COUNT(*) as balls_faced,
    SUM(runs_total) as total_runs,
    ROUND(100.0 * SUM(runs_total) / COUNT(*), 2) as strike_rate
FROM deliveries
WHERE batter IS NOT NULL
GROUP BY batter
ORDER BY total_runs DESC
LIMIT 10;

-- 11. TOP 10 BOWLERS BY WICKETS
SELECT 
    bowler,
    COUNT(DISTINCT match_id) as matches,
    COUNT(*) as balls_bowled,
    COUNT(CASE WHEN wicket_kind IS NOT NULL THEN 1 END) as wickets
FROM deliveries
WHERE bowler IS NOT NULL
GROUP BY bowler
HAVING COUNT(CASE WHEN wicket_kind IS NOT NULL THEN 1 END) > 0
ORDER BY wickets DESC
LIMIT 10;

-- 12. MATCHES PER TEAM (HOME AND AWAY)
SELECT 
    batting_team,
    COUNT(*) as matches_as_batting_team
FROM matches
GROUP BY batting_team
ORDER BY matches_as_batting_team DESC;

-- 13. VENUE-WISE CITY DISTRIBUTION
SELECT 
    city,
    venue,
    COUNT(*) as matches
FROM matches
WHERE city IS NOT NULL AND venue IS NOT NULL
GROUP BY city, venue
ORDER BY city, matches DESC;

-- 14. SEASON ANALYSIS
SELECT 
    season,
    COUNT(*) as matches,
    COUNT(DISTINCT batting_team) as teams
FROM matches
WHERE season IS NOT NULL
GROUP BY season
ORDER BY season DESC;

-- 15. OVERS STATISTICS (FROM DELIVERIES)
SELECT 
    MAX(over) as max_overs_in_match,
    COUNT(DISTINCT match_id) as matches_analyzed,
    AVG(CAST(over AS FLOAT)) as avg_overs_per_match
FROM deliveries;
