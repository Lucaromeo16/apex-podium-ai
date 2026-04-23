import os
import pandas as pd

os.makedirs("data/processed", exist_ok=True)

# -----------------------------
# LOAD RAW DATA
# -----------------------------
results_df = pd.read_csv("data/raw/results_2016_2026.csv")
qualifying_df = pd.read_csv("data/raw/qualifying_2016_2026.csv")

# -----------------------------
# CLEAN KEY COLUMNS
# -----------------------------
for col in ["season", "round", "grid", "position", "points"]:
    if col in results_df.columns:
        results_df[col] = pd.to_numeric(results_df[col], errors="coerce")

for col in ["season", "round", "qualifying_position"]:
    if col in qualifying_df.columns:
        qualifying_df[col] = pd.to_numeric(qualifying_df[col], errors="coerce")

results_df["race_date"] = pd.to_datetime(results_df["race_date"], errors="coerce")

# -----------------------------
# KEEP ONLY NEEDED QUALIFYING COLS
# -----------------------------
qual_cols = [
    "season",
    "round",
    "driver_id",
    "qualifying_position",
    "q1",
    "q2",
    "q3",
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
# TARGETS
# -----------------------------
master_df["winner"] = master_df["position"].apply(
    lambda x: 1 if pd.notna(x) and x == 1 else 0
)

master_df["podium"] = master_df["position"].apply(
    lambda x: 1 if pd.notna(x) and x <= 3 else 0
)

# -----------------------------
# FINISH / CLASSIFICATION FLAGS
# -----------------------------
def classify_finished(status):
    if not isinstance(status, str):
        return 0
    status = status.strip()
    if status == "Finished":
        return 1
    if "Lap" in status:
        return 1
    return 0

master_df["finished_race"] = master_df["status"].apply(classify_finished)
master_df["dnf_flag"] = 1 - master_df["finished_race"]

# -----------------------------
# OPTIONAL TRACK FLAGS
# -----------------------------
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
# DRIVER / CONSTRUCTOR RACE-LEVEL POINTS + WINS
# -----------------------------
master_df["driver_points_this_race"] = master_df["points"].fillna(0)
master_df["driver_win_this_race"] = master_df["winner"]
master_df["driver_podium_this_race"] = master_df["podium"]

constructor_race = (
    master_df.groupby(
        ["season", "round", "constructor_id", "constructor_name"],
        as_index=False
    )
    .agg(
        constructor_points_this_race=("points", "sum"),
        constructor_wins_this_race=("winner", "sum"),
        constructor_podiums_this_race=("podium", "sum"),
    )
)

master_df = master_df.merge(
    constructor_race,
    on=["season", "round", "constructor_id", "constructor_name"],
    how="left"
)

# -----------------------------
# SORT CLEANLY
# -----------------------------
master_df = master_df.sort_values(
    ["season", "round", "position", "driver_id"],
    na_position="last"
).reset_index(drop=True)

# -----------------------------
# SAVE OUTPUT
# -----------------------------
master_df.to_csv("data/processed/master_driver_race.csv", index=False)

print("Created: data/processed/master_driver_race.csv")
print("Shape:", master_df.shape)

print("\nWinner counts by season:")
print(master_df.groupby("season")["winner"].sum().sort_index())

print("\nPodium counts by season:")
print(master_df.groupby("season")["podium"].sum().sort_index())

print("\nSample rows:")
print(
    master_df[
        [
            "season",
            "round",
            "race_name",
            "given_name",
            "family_name",
            "constructor_name",
            "grid",
            "qualifying_position",
            "position",
            "points",
            "winner",
            "podium",
            "finished_race",
            "dnf_flag",
            "driver_points_this_race",
            "constructor_points_this_race",
        ]
    ].head(15)
)