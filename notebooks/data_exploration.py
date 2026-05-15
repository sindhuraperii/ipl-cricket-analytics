import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
df = pd.read_csv('data/raw/matches.csv')

print("=" * 80)
print("IPL CRICKET DATA EXPLORATION")
print("=" * 80)

# 1. Basic Information
print("\n1️⃣ DATASET SIZE AND SHAPE")
print(f"   Total Rows: {len(df):,}")
print(f"   Total Columns: {len(df.columns)}")

# 2. Column Information
print("\n2️⃣ COLUMN NAMES AND TYPES")
print(df.info())

# 3. First Few Rows
print("\n3️⃣ FIRST 5 ROWS OF DATA")
print(df.head())

# 4. Statistical Summary
print("\n4️⃣ STATISTICAL SUMMARY")
print(df.describe())

# 5. Missing Values
print("\n5️⃣ MISSING VALUES (NULL VALUES)")
missing = df.isnull().sum()
if missing.sum() > 0:
    print(missing[missing > 0])
else:
    print("   No missing values found!")

# 6. Data Types
print("\n6️⃣ DATA TYPES")
print(df.dtypes)

# 7. Unique Values in Key Columns
print("\n7️⃣ UNIQUE VALUES IN IMPORTANT COLUMNS")
if 'batting_team' in df.columns:
    print(f"   Unique Batting Teams: {df['batting_team'].nunique()}")
    print(f"   Teams: {sorted(df['batting_team'].unique())}")
if 'season' in df.columns:
    print(f"   Unique Seasons: {df['season'].nunique()}")
    print(f"   Seasons: {sorted(df['season'].unique())}")

print("\n" + "=" * 80)
print("✅ Data Exploration Complete!")
print("=" * 80)