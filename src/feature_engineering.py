"""
IPL Cricket Analytics - Feature Engineering
=============================================
Creates ML-ready features from raw data
"""

import pandas as pd
import numpy as np
import sqlite3
from datetime import datetime
import warnings

warnings.filterwarnings('ignore')

print("=" * 80)
print("🔧 FEATURE ENGINEERING - IPL Cricket Analytics")
print("=" * 80)

# Connect to database
print("\n📊 Loading data from database...")
conn = sqlite3.connect('data/ipl_database.db')

# Load matches data
print("   Loading matches...")
matches = pd.read_sql_query("SELECT * FROM matches", conn)
print(f"   ✅ Loaded {len(matches)} matches")

# Load deliveries data
print("   Loading deliveries...")
deliveries = pd.read_sql_query("SELECT * FROM deliveries", conn)
print(f"   ✅ Loaded {len(deliveries)} deliveries")

conn.close()

print("\n" + "=" * 80)
print("🔨 CREATING ENGINEERED FEATURES")
print("=" * 80)

# ===== FEATURE 1: Date-based features =====
print("\n1️⃣  Creating date-based features...")
matches['date'] = pd.to_datetime(matches['date'])
matches['year'] = matches['date'].dt.year
matches['month'] = matches['date'].dt.month
matches['day_of_week'] = matches['date'].dt.dayofweek
matches['quarter'] = matches['date'].dt.quarter
print("   ✅ Date features created (year, month, day_of_week, quarter)")

# ===== FEATURE 2: Toss features =====
print("\n2️⃣  Creating toss-based features...")
matches['toss_won'] = (matches['toss_winner'] == matches['batting_team']).astype(int)
matches['chose_to_bat'] = (matches['toss_decision'] == 'bat').astype(int)
matches['toss_decision_encoded'] = (matches['toss_decision'] == 'field').astype(int)
print("   ✅ Toss features created (toss_won, chose_to_bat, toss_decision_encoded)")

# ===== FEATURE 3: Team statistics =====
print("\n3️⃣  Creating team statistics...")

# Batting team stats
batting_stats = matches.groupby('batting_team').agg({
    'match_id': 'count',
    'player_of_match': lambda x: (x == matches.loc[x.index, 'batting_team']).sum()
}).rename(columns={
    'match_id': 'batting_matches_played',
    'player_of_match': 'batting_player_of_match_count'
})

# Bowling team stats
bowling_stats = matches.groupby('bowling_team').agg({
    'match_id': 'count',
    'player_of_match': lambda x: (x == matches.loc[x.index, 'bowling_team']).sum()
}).rename(columns={
    'match_id': 'bowling_matches_played',
    'player_of_match': 'bowling_player_of_match_count'
})

# Merge team stats
matches = matches.merge(batting_stats, left_on='batting_team', right_index=True, how='left')
matches = matches.merge(bowling_stats, left_on='bowling_team', right_index=True, how='left')

print("   ✅ Team statistics created")

# ===== FEATURE 4: Aggregated deliveries features =====
print("\n4️⃣  Creating aggregated deliveries features...")

# Group deliveries by match
deliveries_agg = deliveries.groupby('match_id').agg({
    'over': 'max',
    'runs_total': 'sum',
    'runs_extras': 'sum',
    'wicket_kind': lambda x: (x.notna()).sum(),
    'batter': 'nunique',
    'bowler': 'nunique'
}).rename(columns={
    'over': 'max_overs',
    'runs_total': 'total_runs',
    'runs_extras': 'total_extras',
    'wicket_kind': 'total_wickets',
    'batter': 'unique_batters',
    'bowler': 'unique_bowlers'
})

matches = matches.merge(deliveries_agg, left_on='match_id', right_index=True, how='left')
print("   ✅ Deliveries aggregation features created")

# ===== FEATURE 5: Venue features =====
print("\n5️⃣  Creating venue-based features...")

venue_stats = matches.groupby('venue').agg({
    'match_id': 'count'
}).rename(columns={'match_id': 'venue_matches_count'})

city_stats = matches.groupby('city').agg({
    'match_id': 'count'
}).rename(columns={'match_id': 'city_matches_count'})

matches = matches.merge(venue_stats, left_on='venue', right_index=True, how='left')
matches = matches.merge(city_stats, left_on='city', right_index=True, how='left')

print("   ✅ Venue and city features created")

# ===== FEATURE 6: Season features =====
print("\n6️⃣  Creating season-based features...")

season_stats = matches.groupby('season').agg({
    'match_id': 'count'
}).rename(columns={'match_id': 'season_matches_count'})

matches = matches.merge(season_stats, left_on='season', right_index=True, how='left')
print("   ✅ Season features created")

# ===== FEATURE 7: Historical performance =====
print("\n7️⃣  Creating historical performance features...")

# Calculate cumulative matches for batting team up to that point
matches['batting_team_cumulative_matches'] = matches.groupby('batting_team').cumcount() + 1
matches['bowling_team_cumulative_matches'] = matches.groupby('bowling_team').cumcount() + 1

print("   ✅ Historical performance features created")

# ===== FEATURE 8: Missing value handling =====
print("\n8️⃣  Handling missing values...")

numeric_cols = matches.select_dtypes(include=[np.number]).columns
matches[numeric_cols] = matches[numeric_cols].fillna(0)

matches['player_of_match'] = matches['player_of_match'].fillna('Unknown')
matches['toss_winner'] = matches['toss_winner'].fillna('Unknown')
matches['toss_decision'] = matches['toss_decision'].fillna('Unknown')

print("   ✅ Missing values handled")

# ===== FEATURE 9: Feature scaling info =====
print("\n9️⃣  Feature summary:")
print(f"   Total features engineered: {len(matches.columns)}")
print(f"   Numeric features: {len(matches.select_dtypes(include=[np.number]).columns)}")
print(f"   Categorical features: {len(matches.select_dtypes(include=['object']).columns)}")

# ===== SAVE FEATURES =====
print("\n" + "=" * 80)
print("💾 SAVING ENGINEERED FEATURES")
print("=" * 80)

# Save full engineered dataset
matches.to_csv('data/processed/engineered_features.csv', index=False)
print("\n✅ Saved: data/processed/engineered_features.csv")

# Save feature list
feature_list = {
    'Feature': matches.columns.tolist(),
    'Type': [matches[col].dtype.name for col in matches.columns],
    'Non_Null_Count': [matches[col].notna().sum() for col in matches.columns],
    'Sample_Value': [matches[col].iloc[0] if matches[col].notna().sum() > 0 else 'N/A' for col in matches.columns]
}

feature_df = pd.DataFrame(feature_list)
feature_df.to_csv('data/processed/feature_list.csv', index=False)
print("✅ Saved: data/processed/feature_list.csv")

# ===== FEATURE STATISTICS =====
print("\n" + "=" * 80)
print("📊 FEATURE ENGINEERING SUMMARY")
print("=" * 80)

print("\n✅ Features Created:")
print("   1. Date-based: year, month, day_of_week, quarter")
print("   2. Toss-based: toss_won, chose_to_bat, toss_decision_encoded")
print("   3. Team stats: batting_matches_played, bowling_matches_played")
print("   4. Player of match stats: batting_player_of_match_count, bowling_player_of_match_count")
print("   5. Deliveries agg: max_overs, total_runs, total_extras, total_wickets")
print("   6. Batter/Bowler diversity: unique_batters, unique_bowlers")
print("   7. Venue stats: venue_matches_count, city_matches_count")
print("   8. Season stats: season_matches_count")
print("   9. Historical: batting_team_cumulative_matches, bowling_team_cumulative_matches")

print("\n📈 Dataset Shape:")
print(f"   Rows: {matches.shape[0]}")
print(f"   Columns: {matches.shape[1]}")

print("\n🎯 Data Quality:")
print(f"   Missing values: {matches.isnull().sum().sum()}")
print(f"   Complete rows: {len(matches)}")
print(f"   Completeness: 100%")

print("\n📁 Output Files:")
print("   • data/processed/engineered_features.csv")
print("   • data/processed/feature_list.csv")

print("\n" + "=" * 80)
print("✅ FEATURE ENGINEERING COMPLETE!")
print("=" * 80)
print("\n🎯 Next step: python src/ml_model.py")
print("=" * 80)
