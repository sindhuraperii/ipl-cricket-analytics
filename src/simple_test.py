import pandas as pd

print("Reading CSV file...")
df = pd.read_csv('data/raw/matches.csv')
print(f"Success! File has {len(df)} rows and {len(df.columns)} columns")
print(f"Columns: {list(df.columns)}")