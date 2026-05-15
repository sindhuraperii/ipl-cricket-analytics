import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv('data/raw/matches.csv', low_memory=False)

# Create a figure with multiple subplots
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('IPL Cricket Data Analysis', fontsize=16, fontweight='bold')

# 1. Top 10 Batters
ax1 = axes[0, 0]
top_batters = df.groupby('batter')['batter_runs'].sum().nlargest(10)
top_batters.plot(kind='barh', ax=ax1, color='steelblue')
ax1.set_title('Top 10 Batters by Total Runs')
ax1.set_xlabel('Total Runs')

# 2. Top 10 Bowlers
ax2 = axes[0, 1]
top_bowlers = df.groupby('bowler')['bowler_wicket'].sum().nlargest(10)
top_bowlers.plot(kind='barh', ax=ax2, color='coral')
ax2.set_title('Top 10 Bowlers by Total Wickets')
ax2.set_xlabel('Total Wickets')

# 3. Runs Distribution
ax3 = axes[1, 0]
df['batter_runs'].value_counts().sort_index().plot(kind='bar', ax=ax3, color='green')
ax3.set_title('Distribution of Runs per Ball')
ax3.set_xlabel('Runs Scored')
ax3.set_ylabel('Frequency')

# 4. Matches by Team
ax4 = axes[1, 1]
team_matches = df['batting_team'].value_counts().head(10)
team_matches.plot(kind='barh', ax=ax4, color='purple')
ax4.set_title('Top 10 Teams by Ball Count')
ax4.set_xlabel('Number of Balls Faced')

plt.tight_layout()
plt.savefig('visualizations/ipl_analysis.png', dpi=300, bbox_inches='tight')
print("✅ Visualization saved to: visualizations/ipl_analysis.png")
plt.show()