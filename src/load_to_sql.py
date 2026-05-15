import pandas as pd
import sqlite3
import os

print("=" * 80)
print("🗄️  IPL CRICKET DATABASE SETUP")
print("=" * 80)

# Step 1: Check if cleaned data exists
print("\n📋 Step 1: Checking if cleaned data exists...")

if not os.path.exists('data/processed/cleaned_matches.csv'):
    print("❌ ERROR: data/processed/cleaned_matches.csv not found!")
    print("   Please run data cleaning first")
    exit()

if not os.path.exists('data/processed/cleaned_deliveries.csv'):
    print("❌ ERROR: data/processed/cleaned_deliveries.csv not found!")
    print("   Please run data cleaning first")
    exit()

print("✅ Found: data/processed/cleaned_matches.csv")
print("✅ Found: data/processed/cleaned_deliveries.csv")

# Step 2: Load CSV files
print("\n📊 Step 2: Loading CSV files into memory...")

try:
    matches = pd.read_csv('data/processed/cleaned_matches.csv', low_memory=False)
    deliveries = pd.read_csv('data/processed/cleaned_deliveries.csv', low_memory=False)
    
    print(f"✅ Matches: {len(matches)} rows, {len(matches.columns)} columns")
    print(f"✅ Deliveries: {len(deliveries)} rows, {len(deliveries.columns)} columns")
except Exception as e:
    print(f"❌ ERROR loading CSV: {e}")
    exit()

# Step 3: Create database connection
print("\n🗄️  Step 3: Creating SQLite database and tables...")

try:
    # Remove existing database if it exists
    if os.path.exists('data/ipl_database.db'):
        os.remove('data/ipl_database.db')
    
    conn = sqlite3.connect('data/ipl_database.db')
    cursor = conn.cursor()
    
    print("✅ Database created: data/ipl_database.db")
except Exception as e:
    print(f"❌ ERROR creating database: {e}")
    exit()

# Step 4: Create tables with simple schema
print("\n📝 Creating MATCHES table...")

try:
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS matches (
        match_id INTEGER PRIMARY KEY,
        date TEXT,
        batting_team TEXT,
        bowling_team TEXT,
        player_of_match TEXT,
        toss_winner TEXT,
        toss_decision TEXT,
        venue TEXT,
        city TEXT,
        season INTEGER
    )
    ''')
    print("✅ MATCHES table created")
except Exception as e:
    print(f"❌ ERROR creating MATCHES table: {e}")
    exit()

print("\n📝 Creating DELIVERIES table...")

try:
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS deliveries (
        match_id INTEGER,
        innings INTEGER,
        over INTEGER,
        ball INTEGER,
        batter TEXT,
        bowler TEXT,
        runs_total INTEGER,
        runs_extras INTEGER,
        wicket_kind TEXT,
        FOREIGN KEY (match_id) REFERENCES matches(match_id)
    )
    ''')
    print("✅ DELIVERIES table created")
except Exception as e:
    print(f"❌ ERROR creating DELIVERIES table: {e}")
    exit()

# Step 5: Insert data
print("\n💾 Step 4: Loading data into tables...")

# Clean data before inserting
matches['match_id'] = pd.to_numeric(matches['match_id'], errors='coerce')
matches['season'] = pd.to_numeric(matches['season'], errors='coerce')
matches = matches.dropna(subset=['match_id'])

deliveries['match_id'] = pd.to_numeric(deliveries['match_id'], errors='coerce')
deliveries['innings'] = pd.to_numeric(deliveries['innings'], errors='coerce')
deliveries['over'] = pd.to_numeric(deliveries['over'], errors='coerce')
deliveries['ball'] = pd.to_numeric(deliveries['ball'], errors='coerce')
deliveries['runs_total'] = pd.to_numeric(deliveries['runs_total'], errors='coerce')
deliveries['runs_extras'] = pd.to_numeric(deliveries['runs_extras'], errors='coerce')

print("   Loading matches data...")
try:
    matches.to_sql('matches', conn, if_exists='replace', index=False)
    print(f"   ✅ Inserted {len(matches)} matches")
except Exception as e:
    print(f"   ❌ ERROR inserting matches: {e}")

print("   Loading deliveries data...")
try:
    deliveries.to_sql('deliveries', conn, if_exists='replace', index=False)
    print(f"   ✅ Inserted {len(deliveries)} deliveries")
except Exception as e:
    print(f"   ❌ ERROR inserting deliveries: {e}")

# Step 6: Create indexes for performance
print("\n🚀 Step 5: Creating indexes for performance...")

try:
    cursor.execute('CREATE INDEX idx_matches_date ON matches(date)')
    cursor.execute('CREATE INDEX idx_matches_season ON matches(season)')
    cursor.execute('CREATE INDEX idx_matches_venue ON matches(venue)')
    cursor.execute('CREATE INDEX idx_deliveries_match ON deliveries(match_id)')
    cursor.execute('CREATE INDEX idx_deliveries_batter ON deliveries(batter)')
    cursor.execute('CREATE INDEX idx_deliveries_bowler ON deliveries(bowler)')
    print("✅ Indexes created for faster queries")
except Exception as e:
    print(f"❌ ERROR creating indexes: {e}")

# Step 7: Verify data
print("\n✅ Step 6: Verifying data...")

try:
    cursor.execute("SELECT COUNT(*) FROM matches")
    match_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM deliveries")
    delivery_count = cursor.fetchone()[0]
    
    print(f"   ✅ Total matches in database: {match_count}")
    print(f"   ✅ Total deliveries in database: {delivery_count}")
except Exception as e:
    print(f"   ❌ ERROR verifying: {e}")

# Step 8: Show sample data
print("\n📊 Step 7: Sample data from database...")

try:
    sample_matches = pd.read_sql_query("SELECT * FROM matches LIMIT 3", conn)
    print("\n   Sample Matches:")
    print(sample_matches.to_string())
except Exception as e:
    print(f"   ❌ ERROR reading sample: {e}")

# Commit and close
conn.commit()
conn.close()

print("\n" + "=" * 80)
print("✅ DATABASE SETUP COMPLETE!")
print("=" * 80)
print("\n📁 Database created: data/ipl_database.db")
print("📊 Ready for analysis!")
print("\n🎯 Next step: python src/eda.py")
print("=" * 80 + "\n")
