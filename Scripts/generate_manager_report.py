import os
import sqlite3
import pandas as pd

# Define path to the database
db_path = os.path.join("..", "Data", "casino.db")
if not os.path.exists(db_path):
    db_path = os.path.join("Data", "casino.db")

print("📊 GENERATING OPERATIONAL PERFORMANCE REPORT...\n")

conn = sqlite3.connect(db_path)

# Query 1: Floor Revenue Performance
revenue_query = """
SELECT 
    game_type AS [Sector],
    COUNT(game_id) AS [Units],
    PRINTF("$%,.2f", SUM(daily_revenue)) AS [Total Revenue],
    PRINTF("$%,.2f", AVG(daily_revenue)) AS [Avg Per Unit]
FROM game_revenue
GROUP BY game_type;
"""

# Query 2: VIP Risk Allocation
risk_query = """
SELECT 
    v.alert_status AS [Protocol],
    COUNT(p.player_id) AS [VIP Count],
    PRINTF("$%,.2f", SUM(v.large_wager)) AS [Total Exposure],
    CASE 
        WHEN v.alert_status = 'Host Assigned' THEN '🟢 [LOW RISK]'
        WHEN v.alert_status = 'Investigating' THEN '🚨 [CRITICAL]'
        ELSE '⚪ [STANDARD]'
    END AS [Signal]
FROM vip_alerts v
INNER JOIN player_activity p ON v.player_id = p.player_id
GROUP BY v.alert_status;
"""

df_revenue = pd.read_sql_query(revenue_query, conn)
df_risk = pd.read_sql_query(risk_query, conn)
conn.close()

# Markdown Dashboard
report_content = f"""# CASINO OPERATIONAL PERFORMANCE REPORT
**Status:** Live Database Metrics  

---

## 💵 1. Gaming Floor Revenue Performance
Performance breakdown by gaming sector.

{df_revenue.to_markdown(index=False)}

---

## 🕯️ 2. Risk Allocation & Floor Signals
Real-time tracking for high-exposure accounts.

{df_risk.to_markdown(index=False)}

---
**Report generated successfully from automated pipeline engine.**
"""

# Save out the dashboard file
output_path = os.path.join("..", "MANAGEMENT_REPORT.md")
with open(output_path, "w", encoding="utf-8") as f:
    f.write(report_content)

print("✨ Success! Dashboard saved to root directory as 'MANAGEMENT_REPORT.md'")