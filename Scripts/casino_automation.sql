
-- Dynamic tier assignment based on lifetime wager thresholds.

DROP PROCEDURE IF EXISTS get_player_loyalty_tiers;
DELIMITER $$
CREATE PROCEDURE get_player_loyalty_tiers()
BEGIN
    SELECT player_id, player_name, total_wagered,
    CASE
        WHEN total_wagered >= 100000 THEN 'Diamond VIP'
        WHEN total_wagered >= 25000 THEN 'Platinum'
        ELSE 'Gold'
    END AS loyalty_status
    FROM player_activity;
END $$
DELIMITER ;

CALL get_player_loyalty_tiers;

-- Automatically intercepts massive bets to notify VIP Floor Hosts instantly.

DROP TRIGGER IF EXISTS flag_high_roller;
DELIMITER $$
CREATE TRIGGER flag_high_roller
AFTER INSERT ON player_activity
FOR EACH ROW
BEGIN
    INSERT INTO vip_alerts (player_id, large_wager, alert_status)
    VALUES(NEW.player_id, NEW.total_wagered, 'Host Assigned');
END $$
DELIMITER ;


-- Scheduled background routine running daily to clear out inactive, $0 revenue machines.
DROP EVENT IF EXISTS purge_zero_revenue_games;
DELIMITER $$
CREATE EVENT purge_zero_revenue_games
ON SCHEDULE EVERY 1 DAY
DO
BEGIN
    DELETE FROM game_revenue
    WHERE daily_revenue = 0;
END $$
DELIMITER ;