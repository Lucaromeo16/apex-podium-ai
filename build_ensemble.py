import json
import os
import pandas as pd

PREDICTIONS_PATH = "model/predictions.csv"
OUTPUT_CSV_PATH = "model/ensemble_predictions.csv"
OUTPUT_JSON_PATH = "src/data/ensemble_predictions.json"

df = pd.read_csv(PREDICTIONS_PATH)

required_cols = [
    "season",
    "round",
    "race_name",
    "given_name",
    "family_name",
    "constructor_name",
    "podium",
    "predicted_podium_probability",
    "model",
]

missing = [col for col in required_cols if col not in df.columns]
if missing:
    raise ValueError(f"Missing required columns in predictions.csv: {missing}")

pivot_df = df.pivot_table(
    index=[
        "season",
        "round",
        "race_name",
        "given_name",
        "family_name",
        "constructor_name",
        "podium",
    ],
    columns="model",
    values="predicted_podium_probability",
    aggfunc="first",
).reset_index()

pivot_df.columns.name = None

for col in ["logistic_regression", "random_forest", "xgboost"]:
    if col not in pivot_df.columns:
        pivot_df[col] = 0.0

pivot_df["ensemble_probability"] = (
    0.50 * pivot_df["logistic_regression"]
    + 0.30 * pivot_df["random_forest"]
    + 0.20 * pivot_df["xgboost"]
)

pivot_df["driver"] = pivot_df["given_name"].fillna("") + " " + pivot_df["family_name"].fillna("")
pivot_df["driver"] = pivot_df["driver"].str.strip()

pivot_df = pivot_df.sort_values(
    ["season", "round", "ensemble_probability"],
    ascending=[True, True, False]
).reset_index(drop=True)

pivot_df["rank"] = (
    pivot_df.groupby(["season", "round", "race_name"])["ensemble_probability"]
    .rank(method="first", ascending=False)
    .astype(int)
)

pivot_df.to_csv(OUTPUT_CSV_PATH, index=False)
print(f"Created: {OUTPUT_CSV_PATH}")

os.makedirs("src/data", exist_ok=True)

json_output = []

for (season, rnd, race_name), group in pivot_df.groupby(["season", "round", "race_name"]):
    group = group.sort_values("ensemble_probability", ascending=False)

    predictions = []
    for _, row in group.iterrows():
        predictions.append({
            "rank": int(row["rank"]),
            "driver": row["driver"],
            "team": row["constructor_name"],
            "probability": round(float(row["ensemble_probability"]) * 100, 1)
        })

    json_output.append({
        "grand_prix": race_name,
        "season": int(season),
        "round": int(rnd),
        "predictions": predictions
    })

with open(OUTPUT_JSON_PATH, "w") as f:
    json.dump(json_output, f, indent=2)

print(f"Created: {OUTPUT_JSON_PATH}")
print("\nSample preview:")
print(pivot_df[[
    "season",
    "round",
    "race_name",
    "driver",
    "constructor_name",
    "ensemble_probability",
    "rank"
]].head(10))