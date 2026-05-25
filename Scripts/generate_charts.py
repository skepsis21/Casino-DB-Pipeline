import matplotlib.pyplot as plt

# Data matching your mock dataset breakdown
labels = ['Gold Tier', 'Platinum Tier', 'Diamond VIP']
sizes = [40, 33.3, 26.7] # Percentage breakdown from your 15 players
colors = ['#d4af37', '#b0c4de', '#1e90ff'] # Gold, Platinum Silver, Diamond Blue
explode = (0, 0, 0.1)  # Pop out the Diamond VIP slice for visual emphasis

# Create the donut chart
plt.figure(figsize=(6, 6))
plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', 
        startangle=140, pctdistance=0.85, textprops={'fontsize': 12, 'weight': 'bold'})

# Turn it into a donut chart by drawing a white circle in the center
centre_circle = plt.Circle((0,0), 0.70, fc='white')
fig = plt.gcf()
fig.gca().add_artist(centre_circle)

plt.title('Cruise Line Casino: Player Loyalty Tier Distribution', fontsize=14, weight='bold', pad=20)
plt.tight_layout()

# Save it straight to your project folder
plt.savefig('tier_distribution_chart.png', dpi=300)
print("Chart successfully generated and saved!")