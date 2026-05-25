import os
import sqlite3
import pandas as pd

# Define paths - pointing straight to your data folder
db_path = os.path.join("Data", "casino.db")
player_csv = os.path.join("Data", "player_activity.csv")
game_revenue_csv = os.path.join("Data", "game_revenue.csv")

print("🚢 Initializing Casino SQLite Database Setup...\n")

# 1. Connect to SQLite
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 2. Create the tables
print("🛠️ Creating tables inside casino.db...")
cursor.execute("""
CREATE TABLE IF NOT EXISTS player_activity (
    player_id INTEGER PRIMARY KEY,
    player_name TEXT,
    total_wagered REAL
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS game_revenue (
    game_id INTEGER PRIMARY KEY,
    game_name TEXT,
    game_type TEXT,
    daily_revenue REAL
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS vip_alerts (
    alert_id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER,
    game_id INTEGER,
    large_wager REAL,
    alert_status TEXT,
    alert_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
""")
conn.commit()

# 3. Load CSV data into the database
print("📂 Importing CSV datasets into tables...")

if os.path.exists(player_csv):
    df_players = pd.read_csv(player_csv)
    df_players.to_sql("player_activity", conn, if_exists="replace", index=False)
    print(f"   ✅ Imported {len(df_players)} players to 'player_activity'")

if os.path.exists(game_revenue_csv):
    df_games = pd.read_csv(game_revenue_csv)
    df_games.to_sql("game_revenue", conn, if_exists="replace", index=False)
    print(f"   ✅ Imported {len(df_games)} games to 'game_revenue'")

# 4. Populate sample alerts for demo purposes
cursor.execute("DELETE FROM vip_alerts")
cursor.execute("""
INSERT INTO vip_alerts (player_id, game_id, large_wager, alert_status)
VALUES 
(1001, 501, 168123.00, 'Host Assigned'),
(1002, 503, 214050.00, 'Host Assigned'),
(1010, 502, 231500.00, 'Investigating')
""")
conn.commit()

# 5. Execute and display analytics queries
print("\n📊 ===============================================")
print("📈 RUNNING BUSINESS INTELLIGENCE JOINS")
print("==================================================\n")

print("🔴 SECURITY DISPATCH PROTOCOL (INNER JOIN)")
inner_join_query = """
SELECT v.alert_id, p.player_name, v.large_wager, v.alert_status
FROM vip_alerts v
INNER JOIN player_activity p ON v.player_id = p.player_id;
"""
print(pd.read_sql_query(inner_join_query, conn).to_string(index=False))

print("\n" + "="*50 + "\n")

print("🎰 GAMING FLOOR UTILIZATION AUDIT (LEFT JOIN)")
left_join_query = """
SELECT g.game_name, g.game_type, g.daily_revenue, COALESCE(v.alert_status, 'No Alerts') AS security_status
FROM game_revenue g
LEFT JOIN vip_alerts v ON g.game_id = v.game_id;
"""
print(pd.read_sql_query(left_join_query, conn).to_string(index=False))

conn.close()
print("\n🎉 Database runs completed! Setup script safely verified.")

## pip install pandas
## python setup_local_db.py