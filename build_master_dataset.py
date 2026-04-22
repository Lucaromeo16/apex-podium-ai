import os
import pandas as pd

os.makedirs("data/processed", exist_ok=True)

# -----------------------------
# LOAD RAW DATA
# -----------------------------
results_df = pd.read_csv("data/raw/results_2021_2025.csv")
qualifying_df = pd.read_csv("data/raw/qualifying_2021_2025.csv")

# -----------------------------
# CLEAN KEY COLUMNS
# -----------------------------
results_df["season"] = pd.to_numeric(results_df["season"], errors="coerce")
results_df["round"] = pd.to_numeric(results_df["round"], errors="coerce")
results_df["grid"] = pd.to_numeric(results_df["grid"], errors="coerce")
results_df["position"] = pd.to_numeric(results_df["position"], errors="coerce")
results_df["points"] = pd.to_numeric(results_df["points"], errors="coerce")

qualifying_df["season"] = pd.to_numeric(qualifying_df["season"], errors="coerce")
qualifying_df["round"] = pd.to_numeric(qualifying_df["round"], errors="coerce")
qualifying_df["qualifying_position"] = pd.to_numeric(qualifying_df["qualifying_position"], errors="coerce")

# -----------------------------
# SELECT QUALIFYING COLUMNS TO MERGE
# -----------------------------
qual_cols = [
    "season",
    "round",
    "driver_id",
    "qualifying_position",
    "q1",
    "q2",
    "q3"
]

qualifying_trimmed = qualifying_df[qual_cols].copy()

# -----------------------------
# MERGE RESULTS + QUALIFYING
# -----------------------------
master_df = results_df.merge(
    qualifying_trimmed,
    on=["season", "round", "driver_id"],
    how="left"
)

# -----------------------------
# CREATE TARGET VARIABLE
# -----------------------------
master_df["podium"] = master_df["position"].apply(
    lambda x: 1 if pd.notna(x) and x <= 3 else 0
)

# -----------------------------
# OPTIONAL HELPFUL FLAGS
# -----------------------------
master_df["finished_race"] = master_df["status"].apply(
    lambda x: 1 if isinstance(x, str) and x == "Finished" else 0
)

master_df["monaco_flag"] = master_df["race_name"].apply(
    lambda x: 1 if isinstance(x, str) and "Monaco" in x else 0
)

master_df["singapore_flag"] = master_df["race_name"].apply(
    lambda x: 1 if isinstance(x, str) and "Singapore" in x else 0
)

master_df["bahrain_flag"] = master_df["race_name"].apply(
    lambda x: 1 if isinstance(x, str) and "Bahrain" in x else 0
)

# -----------------------------
# SAVE OUTPUT
# -----------------------------
master_df.to_csv("data/processed/master_driver_race.csv", index=False)

print("Created: data/processed/master_driver_race.csv")
print(master_df.head())
print(master_df.shape)
print(master_df["podium"].value_counts(dropna=False))