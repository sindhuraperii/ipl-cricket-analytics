import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import pickle

print("=" * 80)
print("🔧 PREPARING DATA FOR MACHINE LEARNING")
print("=" * 80 + "\n")

# Load raw data
print("📥 Loading data...")
df = pd.read_csv('data/raw/matches.csv', low_memory=False)

# Convert date to datetime
df['date'] = pd.to_datetime(df['date'])

print(f"   ✅ Loaded {len(df):,} records\n")

# ============================================
# AGGREGATE BY MATCH
# ============================================

print("🔨 Creating features...\n")

print("   1. Aggregating by match...")

match_data = df.groupby('match_id').agg({
    'date': 'first',
    'batting_team': 'first',
    'bowling_team': 'first',
    'toss_winner': 'first',
    'toss_decision': 'first',
    'match_won_by': 'first',
    'venue': 'first',
    'city': 'first',
    'batter_runs': 'sum',
    'bowler_wicket': 'sum',
    'runs_extras': 'sum',
}).reset_index()

print(f"      Created {len(match_data)} unique matches\n")

# Rename columns
match_data = match_data.rename(columns={
    'batting_team': 'team1', 
    'bowling_team': 'team2'
})

# ============================================
# CREATE TARGET VARIABLE FIRST
# ============================================

print("   2. Creating target variable...")

# Determine winner: 1 if team1 won, 0 if team2 won
match_data['winner'] = (match_data['match_won_by'] == match_data['team1']).astype(int)

# Remove no result matches
match_data = match_data[match_data['match_won_by'] != 'No Result'].reset_index(drop=True)

print(f"      Total matches: {len(match_data)}")
print(f"      Team1 wins: {(match_data['winner'] == 1).sum()}")
print(f"      Team2 wins: {(match_data['winner'] == 0).sum()}\n")

# ============================================
# CALCULATE CUMULATIVE WINS BEFORE EACH MATCH
# ============================================

print("   3. Calculating team statistics...\n")

# Sort by date to get historical wins
match_data = match_data.sort_values('date').reset_index(drop=True)

# Initialize win columns
match_data['team1_wins'] = 0.0
match_data['team2_wins'] = 0.0

# Calculate cumulative wins for each team at each match
for idx in range(len(match_data)):
    team1 = match_data.loc[idx, 'team1']
    team2 = match_data.loc[idx, 'team2']
    
    # Count wins before this match
    past_matches = match_data[:idx]
    team1_wins = ((past_matches['match_won_by'] == team1).sum())
    team2_wins = ((past_matches['match_won_by'] == team2).sum())
    
    match_data.loc[idx, 'team1_wins'] = team1_wins
    match_data.loc[idx, 'team2_wins'] = team2_wins

print("      ✅ Team statistics calculated\n")

# ============================================
# ENCODE CATEGORICAL FEATURES
# ============================================

print("   4. Encoding categorical variables...\n")

le_toss = LabelEncoder()
match_data['toss_decision_encoded'] = le_toss.fit_transform(match_data['toss_decision'].fillna('bat'))

# ============================================
# PREPARE FEATURES
# ============================================

print("   5. Preparing features...\n")

feature_columns = [
    'team1_wins',           # Historical wins for team1
    'team2_wins',           # Historical wins for team2
    'batter_runs',          # Total runs scored
    'bowler_wicket',        # Wickets taken
    'runs_extras',          # Extras conceded
    'toss_decision_encoded' # Toss decision (bat/field)
]

X = match_data[feature_columns].fillna(0)
y = match_data['winner']

print(f"      Features shape: {X.shape}")
print(f"      Target shape: {y.shape}\n")

# ============================================
# SPLIT DATA
# ============================================

print("✂️ Splitting data into train/test...\n")

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"   Training set: {X_train.shape[0]} matches")
print(f"   Testing set: {X_test.shape[0]} matches\n")

# ============================================
# SAVE PREPARED DATA
# ============================================

print("💾 Saving prepared data...\n")

# Save to CSV
match_data.to_csv('data/processed/match_data_processed.csv', index=False)
X_train.to_csv('data/processed/X_train.csv', index=False)
X_test.to_csv('data/processed/X_test.csv', index=False)
y_train.to_csv('data/processed/y_train.csv', index=False)
y_test.to_csv('data/processed/y_test.csv', index=False)

# Save label encoder
with open('models/label_encoder.pkl', 'wb') as f:
    pickle.dump(le_toss, f)

print("=" * 80)
print("✅ DATA PREPARATION COMPLETE!")
print("=" * 80 + "\n")

print("📁 Files saved:")
print("   • data/processed/match_data_processed.csv")
print("   • data/processed/X_train.csv")
print("   • data/processed/X_test.csv")
print("   • data/processed/y_train.csv")
print("   • data/processed/y_test.csv")
print("   • models/label_encoder.pkl\n")