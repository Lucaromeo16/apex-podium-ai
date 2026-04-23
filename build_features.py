import os
import pandas as pd

os.makedirs("data/processed", exist_ok=True)

df = pd.read_csv("data/processed/master_driver_race.csv")

# -----------------------------
# CLEAN TYPES
# -----------------------------
num_cols = [
    "season",
    "round",
    "grid",
    "qualifying_position",
    "position",
    "points",
    "winner",
    "podium",
    "dnf_flag",
    "driver_points_this_race",
    "driver_win_this_race",
    "driver_podium_this_race",
    "constructor_points_this_race",
    "constructor_wins_this_race",
    "constructor_podiums_this_race",
]

for col in num_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# -----------------------------
# DRIVER SEASON-TO-DATE FEATURES
# -----------------------------
df = df.sort_values(["driver_id", "season", "round"]).reset_index(drop=True)

df["driver_prior_points"] = (
    df.groupby(["driver_id", "season"])["driver_points_this_race"]
    .transform(lambda x: x.shift(1).fillna(0).cumsum())
)

df["driver_prior_wins"] = (
    df.groupby(["driver_id", "season"])["driver_win_this_race"]
    .transform(lambda x: x.shift(1).fillna(0).cumsum())
)

df["driver_prior_podiums"] = (
    df.groupby(["driver_id", "season"])["driver_podium_this_race"]
    .transform(lambda x: x.shift(1).fillna(0).cumsum())
)

# -----------------------------
# CONSTRUCTOR SEASON-TO-DATE FEATURES
# -----------------------------
constructor_season = (
    df[
        [
            "season",
            "round",
            "constructor_id",
            "constructor_points_this_race",
            "constructor_wins_this_race",
            "constructor_podiums_this_race",
        ]
    ]
    .drop_duplicates(subset=["season", "round", "constructor_id"])
    .sort_values(["constructor_id", "season", "round"])
    .reset_index(drop=True)
)

constructor_season["constructor_prior_points"] = (
    constructor_season.groupby(["constructor_id", "season"])["constructor_points_this_race"]
    .transform(lambda x: x.shift(1).fillna(0).cumsum())
)

constructor_season["constructor_prior_wins"] = (
    constructor_season.groupby(["constructor_id", "season"])["constructor_wins_this_race"]
    .transform(lambda x: x.shift(1).fillna(0).cumsum())
)

constructor_season["constructor_prior_podiums"] = (
    constructor_season.groupby(["constructor_id", "season"])["constructor_podiums_this_race"]
    .transform(lambda x: x.shift(1).fillna(0).cumsum())
)

constructor_features = constructor_season[
    [
        "season",
        "round",
        "constructor_id",
        "constructor_prior_points",
        "constructor_prior_wins",
        "constructor_prior_podiums",
    ]
].copy()

df = df.merge(
    constructor_features,
    on=["season", "round", "constructor_id"],
    how="left",
)

# -----------------------------
# ROLLING DRIVER FORM
# -----------------------------
df = df.sort_values(["driver_id", "season", "round"]).reset_index(drop=True)

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
# TRACK HISTORY
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
# FINAL SORT
# -----------------------------
df = df.sort_values(["season", "round", "driver_id"]).reset_index(drop=True)

# -----------------------------
# SAVE
# -----------------------------
df.to_csv("data/processed/modeling_dataset.csv", index=False)

print("Created: data/processed/modeling_dataset.csv")
print("Shape:", df.shape)

check_cols = [
    "driver_prior_points",
    "driver_prior_wins",
    "driver_prior_podiums",
    "constructor_prior_points",
    "constructor_prior_wins",
    "constructor_prior_podiums",
    "avg_finish_last_3",
    "avg_finish_last_5",
    "podiums_last_3",
    "podiums_last_5",
    "dnfs_last_5",
    "avg_finish_at_track",
    "podiums_at_track",
]

print("\nColumns present:")
print([c for c in check_cols if c in df.columns])

print("\nSample rows:")
print(
    df[
        [
            "driver_id",
            "season",
            "round",
            "driver_prior_points",
            "driver_prior_wins",
            "driver_prior_podiums",
            "constructor_prior_points",
            "constructor_prior_wins",
            "constructor_prior_podiums",
            "avg_finish_last_3",
            "avg_finish_last_5",
            "podiums_last_3",
            "podiums_last_5",
            "dnfs_last_5",
            "avg_finish_at_track",
            "podiums_at_track",
        ]
    ].head(15)
)