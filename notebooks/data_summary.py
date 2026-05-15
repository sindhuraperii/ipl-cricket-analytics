import pandas as pd
import numpy as np

# Load the data
df = pd.read_csv('data/raw/matches.csv', low_memory=False)

print("\n" + "=" * 80)
print("📊 IPL CRICKET DATA ANALYSIS SUMMARY")
print("=" * 80 + "\n")

# 1. Basic Stats
print("📈 DATASET OVERVIEW:")
print(f"   • Total Records: {len(df):,} (ball-by-ball data)")
print(f"   • Total Columns: {len(df.columns)}")
print(f"   • Memory Usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB\n")

# 2. Date Range
df['date'] = pd.to_datetime(df['date'])
print("📅 DATA TIME PERIOD:")
print(f"   • Start Date: {df['date'].min().date()}")
print(f"   • End Date: {df['date'].max().date()}")
print(f"   • Total Years: {df['date'].dt.year.max() - df['date'].dt.year.min() + 1} years\n")

# 3. Teams
teams = sorted(df['batting_team'].unique())
print(f"🏏 TEAMS ({len(teams)} total):")
for i, team in enumerate(teams, 1):
    print(f"   {i:2d}. {team}")
print()

# 4. Matches Info
print(f"⚡ MATCH INFORMATION:")
print(f"   • Unique Matches: {df['match_id'].nunique():,}")
print(f"   • Venues: {df['venue'].nunique()}")
print(f"   • Cities: {df['city'].nunique()}")
print(f"   • Match Types: {df['match_type'].unique().tolist()}\n")

# 5. Player Stats
print(f"👥 PLAYER STATISTICS:")
print(f"   • Unique Batters: {df['batter'].nunique()}")
print(f"   • Unique Bowlers: {df['bowler'].nunique()}")
print(f"   • Total Wickets: {df['wicket_kind'].notna().sum():,}\n")

# 6. Runs Stats
print(f"📊 RUNS STATISTICS:")
print(f"   • Total Runs by Batters: {df['batter_runs'].sum():,}")
print(f"   • Average Runs per Ball: {df['batter_runs'].mean():.2f}")
print(f"   • Max Runs in Single Ball: {df['batter_runs'].max()}")
print(f"   • Total Extras: {df['runs_extras'].sum():,}\n")

# 7. Data Quality
print(f"✅ DATA QUALITY:")
total_cells = len(df) * len(df.columns)
null_cells = df.isnull().sum().sum()
data_quality = ((total_cells - null_cells) / total_cells) * 100
print(f"   • Total Data Points: {total_cells:,}")
print(f"   • Missing Values: {null_cells:,}")
print(f"   • Data Quality: {data_quality:.2f}%\n")

# 8. Top Performing Batters
print(f"🌟 TOP 5 BATTERS (by total runs):")
top_batters = df.groupby('batter')['batter_runs'].sum().nlargest(5)
for i, (batter, runs) in enumerate(top_batters.items(), 1):
    print(f"   {i}. {batter}: {runs} runs")
print()

# 9. Top Bowling Performers
print(f"⚽ TOP 5 BOWLERS (by wickets):")
top_bowlers = df.groupby('bowler')['bowler_wicket'].sum().nlargest(5)
for i, (bowler, wickets) in enumerate(top_bowlers.items(), 1):
    print(f"   {i}. {bowler}: {int(wickets)} wickets")
print()

print("=" * 80)
print("✅ ANALYSIS COMPLETE!")
print("=" * 80 + "\n")