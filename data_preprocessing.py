# ============================================================
#   DISASTER MANAGEMENT AI - Group 11
#   Phase 2: Data Loading & Cleaning
#   File: data_cleaning.py
# ============================================================

import pandas as pd

# ─────────────────────────────────────────
# STEP 1: Load the CSV file
# ─────────────────────────────────────────
print("=" * 55)
print("  DISASTER MANAGEMENT AI — Data Cleaning Script")
print("=" * 55)

print("\n[STEP 1] Loading CSV file: em_dat_disaster.csv ...")

try:
    df = pd.read_csv("em_dat_disaster.csv")
    print("  ✅ File loaded successfully!")
except FileNotFoundError:
    print("  ❌ ERROR: 'em_dat_disaster.csv' not found!")
    print("     Make sure the file is in the same folder as this script.")
    exit()

# ─────────────────────────────────────────
# STEP 2: Show shape and column names
# ─────────────────────────────────────────
print("\n[STEP 2] Exploring the dataset ...")

print(f"\n  📐 Shape (rows x columns): {df.shape}")
print(f"  → Total rows    : {df.shape[0]}")
print(f"  → Total columns : {df.shape[1]}")

print(f"\n  📋 Column Names ({len(df.columns)} total):")
for i, col in enumerate(df.columns, start=1):
    print(f"     {i:>2}. {col}")

print(f"\n  🔍 First 3 rows preview:")
print(df.head(3).to_string(index=False))

# ─────────────────────────────────────────
# STEP 3: Filter rows where Country == India
# ─────────────────────────────────────────
print("\n[STEP 3] Filtering rows where Country = 'India' ...")

# Detect country column automatically (case-insensitive)
country_col = None
for col in df.columns:
    if col.strip().lower() in ["country", "country name", "country_name"]:
        country_col = col
        break

if country_col is None:
    print("  ❌ ERROR: Could not find a 'Country' column in the dataset.")
    print(f"     Available columns: {list(df.columns)}")
    exit()

print(f"  ℹ️  Using column: '{country_col}'")

before_filter = len(df)
df = df[df[country_col].str.strip().str.lower() == "india"]
after_filter = len(df)

print(f"  ✅ Filter applied!")
print(f"  → Rows before filter : {before_filter}")
print(f"  → Rows after filter  : {after_filter} (India only)")

if after_filter == 0:
    print("\n  ⚠️  WARNING: No rows found for 'India'.")
    print("     Possible reason: Country names might be spelled differently.")
    print(f"     Unique values in '{country_col}':", df[country_col].unique()[:10])
    exit()

# ─────────────────────────────────────────
# STEP 4: Drop rows with null values
# ─────────────────────────────────────────
print("\n[STEP 4] Dropping rows with null values in key columns ...")

# Columns to check for nulls — auto-match (case-insensitive)
required_cols_input = ["year", "disaster_type", "deaths"]
matched_cols = []

for req in required_cols_input:
    for col in df.columns:
        if col.strip().lower().replace(" ", "_") == req.lower():
            matched_cols.append(col)
            break

print(f"\n  ℹ️  Checking for nulls in: {matched_cols}")

# Show null counts before dropping
print("\n  📊 Null value counts BEFORE cleaning:")
for col in matched_cols:
    null_count = df[col].isnull().sum()
    print(f"     '{col}' → {null_count} null(s)")

before_drop = len(df)
df = df.dropna(subset=matched_cols)
after_drop = len(df)

print(f"\n  ✅ Null rows dropped!")
print(f"  → Rows before dropping nulls : {before_drop}")
print(f"  → Rows after dropping nulls  : {after_drop}")
print(f"  → Total rows removed         : {before_drop - after_drop}")

# ─────────────────────────────────────────
# STEP 5: Save cleaned file
# ─────────────────────────────────────────
print("\n[STEP 5] Saving cleaned data to 'cleaned_disaster_data.csv' ...")

output_file = "cleaned_disaster_data.csv"
df.to_csv(output_file, index=False)

print(f"  ✅ File saved successfully: {output_file}")
print(f"  → Final dataset shape: {df.shape}")

# ─────────────────────────────────────────
# SUMMARY
# ─────────────────────────────────────────
print("\n" + "=" * 55)
print("  ✅ DATA CLEANING COMPLETE — Summary")
print("=" * 55)
print(f"  Original rows loaded     : {before_filter}")
print(f"  After India filter       : {after_filter}")
print(f"  After dropping nulls     : {after_drop}")
print(f"  Rows removed (total)     : {before_filter - after_drop}")
print(f"  Output file              : {output_file}")
print("=" * 55)
print("\n  🎉 Group 11 — Disaster Management AI | Phase 2 Done!\n")