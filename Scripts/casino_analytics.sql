USE casino_db;

-- 1. Execute Stored Procedure for Loyalty Analysis
CALL get_player_loyalty_tiers();

-- 2. Fetch Active Security Dispatches (INNER JOIN)
SELECT 
    v.alert_id,
    p.player_name,
    v.large_wager,
    v.alert_status,
    v.alert_timestamp
FROM vip_alerts v
INNER JOIN player_activity p 
    ON v.player_id = p.player_id;

-- 3. Audit Gaming Floor Asset Utilization (FIXED LEFT JOIN)
SELECT 
    g.game_name,
    g.game_type,
    g.daily_revenue,
    v.alert_status
FROM game_revenue g
LEFT JOIN vip_alerts v 
    ON g.game_id = v.game_id; -- FIXED: Game ID matches Game ID now!