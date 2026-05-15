"""
IPL Cricket Analytics - Exploratory Data Analysis (EDA)
========================================================
Creates visualizations and analyzes patterns in IPL data
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
import warnings

warnings.filterwarnings('ignore')

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)
sns.set_palette("husl")

print("=" * 80)
print("🏏 IPL CRICKET ANALYTICS - EXPLORATORY DATA ANALYSIS (EDA)")
print("=" * 80)

# Connect to database
print("\n📊 Connecting to database...")
conn = sqlite3.connect('data/ipl_database.db')

# Load data
print("📥 Loading data from database...")
matches = pd.read_sql_query("SELECT * FROM matches", conn)
print(f"   ✅ Loaded {len(matches)} match records")

conn.close()

# ===== EDA ANALYSIS =====

print("\n" + "=" * 80)
print("📈 EXPLORATORY DATA ANALYSIS")
print("=" * 80)

# 1. BASIC STATISTICS
print("\n1️⃣  BASIC STATISTICS")
print("-" * 80)
print(f"Total matches: {len(matches)}")
print(f"Date range: {matches['date'].min()} to {matches['date'].max()}")
print(f"Unique batsmen: {matches['batting_team'].nunique()}")
print(f"Unique venues: {matches['venue'].nunique()}")
print(f"Unique cities: {matches['city'].nunique()}")

# Get unique teams
all_teams = set()
all_teams.update(matches['batting_team'].unique())
all_teams.update(matches['bowling_team'].unique())
all_teams = sorted(list(all_teams))
print(f"Total teams: {len([t for t in all_teams if pd.notna(t)])}")

# 2. TEAM WINS ANALYSIS
print("\n2️⃣  TEAM PERFORMANCE ANALYSIS")
print("-" * 80)

try:
    team_wins = matches['player_of_match'].value_counts().head(15)
    
    plt.figure(figsize=(14, 8))
    sns.barplot(x=team_wins.values, y=team_wins.index, palette='viridis')
    plt.title('Top 15 Players - Player of the Match Awards', fontsize=16, fontweight='bold')
    plt.xlabel('Number of Awards', fontsize=12)
    plt.ylabel('Player', fontsize=12)
    plt.tight_layout()
    plt.savefig('visualizations/player_of_match.png', dpi=300, bbox_inches='tight')
    print("   ✅ Saved: visualizations/player_of_match.png")
    plt.close()
except Exception as e:
    print(f"   ⚠️  Could not create player_of_match chart: {e}")

# 3. TOSS IMPACT ANALYSIS
print("\n3️⃣  TOSS IMPACT ANALYSIS")
print("-" * 80)

try:
    toss_data = matches[['toss_winner', 'toss_decision']].dropna()
    print(f"   Matches with toss data: {len(toss_data)}")
    
    toss_decision_counts = toss_data['toss_decision'].value_counts()
    
    plt.figure(figsize=(10, 6))
    colors = ['#3498db', '#e74c3c']
    plt.pie(toss_decision_counts.values, labels=toss_decision_counts.index, 
            autopct='%1.1f%%', colors=colors, startangle=90,
            textprops={'fontsize': 12, 'weight': 'bold'})
    plt.title('Toss Decision Distribution (Bat vs Field)', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig('visualizations/toss_impact.png', dpi=300, bbox_inches='tight')
    print("   ✅ Saved: visualizations/toss_impact.png")
    plt.close()
except Exception as e:
    print(f"   ⚠️  Could not create toss_impact chart: {e}")

# 4. VENUE ANALYSIS
print("\n4️⃣  VENUE ANALYSIS")
print("-" * 80)

try:
    venue_counts = matches['venue'].value_counts().head(10)
    print(f"   Top venue: {venue_counts.index[0]} ({venue_counts.values[0]} matches)")
    
    plt.figure(figsize=(14, 8))
    sns.barplot(x=venue_counts.values, y=venue_counts.index, palette='coolwarm')
    plt.title('Top 10 IPL Venues (Most Matches)', fontsize=16, fontweight='bold')
    plt.xlabel('Number of Matches', fontsize=12)
    plt.ylabel('Venue', fontsize=12)
    plt.tight_layout()
    plt.savefig('visualizations/top_venues.png', dpi=300, bbox_inches='tight')
    print("   ✅ Saved: visualizations/top_venues.png")
    plt.close()
except Exception as e:
    print(f"   ⚠️  Could not create top_venues chart: {e}")

# 5. CITY ANALYSIS
print("\n5️⃣  CITY ANALYSIS")
print("-" * 80)

try:
    city_counts = matches['city'].value_counts().head(10)
    print(f"   Top city: {city_counts.index[0]} ({city_counts.values[0]} matches)")
    
    plt.figure(figsize=(14, 8))
    sns.barplot(x=city_counts.values, y=city_counts.index, palette='rocket')
    plt.title('Top 10 Cities Hosting IPL Matches', fontsize=16, fontweight='bold')
    plt.xlabel('Number of Matches', fontsize=12)
    plt.ylabel('City', fontsize=12)
    plt.tight_layout()
    plt.savefig('visualizations/cities_distribution.png', dpi=300, bbox_inches='tight')
    print("   ✅ Saved: visualizations/cities_distribution.png")
    plt.close()
except Exception as e:
    print(f"   ⚠️  Could not create cities_distribution chart: {e}")

# 6. BATTING TEAM ANALYSIS
print("\n6️⃣  BATTING TEAM ANALYSIS")
print("-" * 80)

try:
    batting_team_counts = matches['batting_team'].value_counts().head(10)
    print(f"   Team with most matches: {batting_team_counts.index[0]} ({batting_team_counts.values[0]} matches)")
    
    plt.figure(figsize=(14, 8))
    sns.barplot(x=batting_team_counts.values, y=batting_team_counts.index, palette='Set2')
    plt.title('Top 10 Teams by Number of Matches (Batting)', fontsize=16, fontweight='bold')
    plt.xlabel('Number of Matches', fontsize=12)
    plt.ylabel('Team', fontsize=12)
    plt.tight_layout()
    plt.savefig('visualizations/batting_teams.png', dpi=300, bbox_inches='tight')
    print("   ✅ Saved: visualizations/batting_teams.png")
    plt.close()
except Exception as e:
    print(f"   ⚠️  Could not create batting_teams chart: {e}")

# 7. BOWLING TEAM ANALYSIS
print("\n7️⃣  BOWLING TEAM ANALYSIS")
print("-" * 80)

try:
    bowling_team_counts = matches['bowling_team'].value_counts().head(10)
    print(f"   Team with most matches: {bowling_team_counts.index[0]} ({bowling_team_counts.values[0]} matches)")
    
    plt.figure(figsize=(14, 8))
    sns.barplot(x=bowling_team_counts.values, y=bowling_team_counts.index, palette='Set1')
    plt.title('Top 10 Teams by Number of Matches (Bowling)', fontsize=16, fontweight='bold')
    plt.xlabel('Number of Matches', fontsize=12)
    plt.ylabel('Team', fontsize=12)
    plt.tight_layout()
    plt.savefig('visualizations/bowling_teams.png', dpi=300, bbox_inches='tight')
    print("   ✅ Saved: visualizations/bowling_teams.png")
    plt.close()
except Exception as e:
    print(f"   ⚠️  Could not create bowling_teams chart: {e}")

# 8. DATE DISTRIBUTION
print("\n8️⃣  DATE DISTRIBUTION")
print("-" * 80)

try:
    matches['date'] = pd.to_datetime(matches['date'])
    matches['year'] = matches['date'].dt.year
    
    matches_per_year = matches['year'].value_counts().sort_index()
    print(f"   Years covered: {matches['year'].min()} to {matches['year'].max()}")
    
    plt.figure(figsize=(14, 6))
    plt.bar(matches_per_year.index, matches_per_year.values, color='steelblue', edgecolor='black')
    plt.title('IPL Matches per Year', fontsize=16, fontweight='bold')
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Number of Matches', fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig('visualizations/matches_per_year.png', dpi=300, bbox_inches='tight')
    print("   ✅ Saved: visualizations/matches_per_year.png")
    plt.close()
except Exception as e:
    print(f"   ⚠️  Could not create matches_per_year chart: {e}")

# ===== SUMMARY STATISTICS =====

print("\n" + "=" * 80)
print("📊 KEY INSIGHTS")
print("=" * 80)

print("\n✅ Most Frequent Player of Match Awards:")
try:
    potm_top = matches['player_of_match'].value_counts().head(5)
    for i, (player, count) in enumerate(potm_top.items(), 1):
        if pd.notna(player):
            print(f"   {i}. {player}: {count} awards")
except Exception as e:
    print(f"   ⚠️  Could not generate this insight: {e}")

print("\n✅ Toss Decision Preference:")
try:
    toss_pref = matches['toss_decision'].value_counts()
    for decision, count in toss_pref.items():
        if pd.notna(decision):
            pct = (count / len(matches[matches['toss_decision'].notna()]) * 100)
            print(f"   {decision}: {count} times ({pct:.1f}%)")
except Exception as e:
    print(f"   ⚠️  Could not generate this insight: {e}")

print("\n✅ Top 5 Venues:")
try:
    venues_top = matches['venue'].value_counts().head(5)
    for i, (venue, count) in enumerate(venues_top.items(), 1):
        if pd.notna(venue):
            print(f"   {i}. {venue}: {count} matches")
except Exception as e:
    print(f"   ⚠️  Could not generate this insight: {e}")

print("\n✅ Top 5 Cities:")
try:
    cities_top = matches['city'].value_counts().head(5)
    for i, (city, count) in enumerate(cities_top.items(), 1):
        if pd.notna(city):
            print(f"   {i}. {city}: {count} matches")
except Exception as e:
    print(f"   ⚠️  Could not generate this insight: {e}")

# ===== SAVE SUMMARY =====

print("\n" + "=" * 80)
print("✅ EDA COMPLETE!")
print("=" * 80)

print("\n📁 Generated visualizations:")
print("   • player_of_match.png")
print("   • toss_impact.png")
print("   • top_venues.png")
print("   • cities_distribution.png")
print("   • batting_teams.png")
print("   • bowling_teams.png")
print("   • matches_per_year.png")

# Save EDA summary
try:
    summary_stats = {
        'Metric': [
            'Total Matches',
            'Date Range',
            'Unique Batsmen',
            'Unique Venues',
            'Unique Cities',
            'Total Teams'
        ],
        'Value': [
            len(matches),
            f"{matches['date'].min()} to {matches['date'].max()}",
            matches['batting_team'].nunique(),
            matches['venue'].nunique(),
            matches['city'].nunique(),
            len([t for t in all_teams if pd.notna(t)])
        ]
    }
    
    summary_df = pd.DataFrame(summary_stats)
    summary_df.to_csv('data/eda_summary.csv', index=False)
    print("\n   • data/eda_summary.csv")
except Exception as e:
    print(f"   ⚠️  Could not save summary: {e}")

print("\n🎯 Next step: python src/feature_engineering.py")
print("=" * 80)
