import os
import pandas as pd

os.makedirs("data/processed", exist_ok=True)

# -----------------------------
# LOAD MASTER DATASET
# -----------------------------
df = pd.read_csv("data/processed/master_driver_race.csv")

# -----------------------------
# CLEAN / CONVERT DATA TYPES
# -----------------------------
df["season"] = pd.to_numeric(df["season"], errors="coerce")
df["round"] = pd.to_numeric(df["round"], errors="coerce")
df["grid"] = pd.to_numeric(df["grid"], errors="coerce")
df["position"] = pd.to_numeric(df["position"], errors="coerce")
df["points"] = pd.to_numeric(df["points"], errors="coerce")
df["qualifying_position"] = pd.to_numeric(df["qualifying_position"], errors="coerce")

# If podium column somehow isn't numeric yet
df["podium"] = pd.to_numeric(df["podium"], errors="coerce")

# DNF flag
df["dnf_flag"] = df["finished_race"].apply(lambda x: 0 if x == 1 else 1)

# -----------------------------
# SORT DATA CORRECTLY
# -----------------------------
df = df.sort_values(["driver_id", "season", "round"]).reset_index(drop=True)

# -----------------------------
# ROLLING DRIVER FORM FEATURES
# -----------------------------
df["avg_finish_last_3"] = (
    df.groupby("driver_id")["position"]
      .transform(lambda x: x.shift(1).rolling(3, min_periods=1).mean())
)

df["avg_finish_last_5"] = (
    df.groupby("driver_id")["position"]
      .transform(lambda x: x.shift(1).rolling(5, min_periods=1).mean())
)

df["podiums_last_3"] = (
    df.groupby("driver_id")["podium"]
      .transform(lambda x: x.shift(1).rolling(3, min_periods=1).sum())
)

df["podiums_last_5"] = (
    df.groupby("driver_id")["podium"]
      .transform(lambda x: x.shift(1).rolling(5, min_periods=1).sum())
)

df["dnfs_last_5"] = (
    df.groupby("driver_id")["dnf_flag"]
      .transform(lambda x: x.shift(1).rolling(5, min_periods=1).sum())
)

# -----------------------------
# TRACK-SPECIFIC HISTORY
# -----------------------------
df = df.sort_values(["driver_id", "circuit_id", "season", "round"]).reset_index(drop=True)

df["avg_finish_at_track"] = (
    df.groupby(["driver_id", "circuit_id"])["position"]
      .transform(lambda x: x.shift(1).expanding().mean())
)

df["podiums_at_track"] = (
    df.groupby(["driver_id", "circuit_id"])["podium"]
      .transform(lambda x: x.shift(1).expanding().sum())
)

# -----------------------------
# RESORT FINAL DATASET
# -----------------------------
df = df.sort_values(["season", "round", "driver_id"]).reset_index(drop=True)

# -----------------------------
# SAVE MODELING DATASET
# -----------------------------
df.to_csv("data/processed/modeling_dataset.csv", index=False)

print("Created: data/processed/modeling_dataset.csv")
print(df.head())
print(df.shape)
print(df[[
    "driver_id",
    "season",
    "round",
    "avg_finish_last_3",
    "avg_finish_last_5",
    "podiums_last_3",
    "podiums_last_5",
    "dnfs_last_5",
    "avg_finish_at_track",
    "podiums_at_track"
]].head(15))