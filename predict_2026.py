import json
import os
from pathlib import Path

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

try:
    from xgboost import XGBClassifier
    XGBOOST_AVAILABLE = True
except Exception:
    XGBOOST_AVAILABLE = False


BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "processed" / "modeling_dataset.csv"
CALENDAR_PATH = BASE_DIR / "data" / "processed" / "calendar_2026.csv"
OUTPUT_CSV_PATH = BASE_DIR / "model" / "predictions_2026.csv"
OUTPUT_JSON_PATH = BASE_DIR / "src" / "data" / "predictions_2026.json"

# No grid / qualifying for future races yet
FEATURE_COLS = [
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

COMPLETED_2026_ROUNDS = [1, 2, 3]


def build_pipeline(model):
    preprocessor = ColumnTransformer(
        transformers=[
            (
                "num",
                Pipeline(
                    steps=[
                        ("imputer", SimpleImputer(strategy="constant", fill_value=0)),
                        ("scaler", StandardScaler()),
                    ]
                ),
                FEATURE_COLS,
            )
        ],
        remainder="drop",
    )

    return Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", model),
        ]
    )


def get_models():
    models = {
        "logistic_regression": LogisticRegression(max_iter=2000, random_state=42),
        "random_forest": RandomForestClassifier(
            n_estimators=400,
            max_depth=10,
            min_samples_leaf=2,
            random_state=42,
        ),
    }

    if XGBOOST_AVAILABLE:
        models["xgboost"] = XGBClassifier(
            n_estimators=300,
            max_depth=4,
            learning_rate=0.05,
            subsample=0.9,
            colsample_bytree=0.9,
            eval_metric="logloss",
            random_state=42,
        )

    return models


def fit_ensemble_and_predict(train_df, predict_df):
    X_train = train_df[FEATURE_COLS]
    y_train = train_df["podium"].astype(int)

    X_predict = predict_df[FEATURE_COLS]

    model_probs = {}
    models = get_models()

    for model_name, model in models.items():
        pipeline = build_pipeline(model)
        pipeline.fit(X_train, y_train)
        probs = pipeline.predict_proba(X_predict)[:, 1]
        model_probs[model_name] = probs

    logistic_probs = model_probs.get("logistic_regression", 0)
    rf_probs = model_probs.get("random_forest", 0)
    xgb_probs = model_probs.get("xgboost", 0)

    if isinstance(xgb_probs, int):
        xgb_probs = 0

    ensemble_probs = (
        0.40 * logistic_probs
        + 0.30 * rf_probs
        + 0.30 * xgb_probs
    )

    return ensemble_probs


def latest_driver_snapshot(df):
    driver_cols = [
        "driver_id",
        "given_name",
        "family_name",
        "constructor_id",
        "constructor_name",
        "driver_prior_points",
        "driver_prior_wins",
        "driver_prior_podiums",
        "avg_finish_last_3",
        "avg_finish_last_5",
        "podiums_last_3",
        "podiums_last_5",
        "dnfs_last_5",
    ]

    latest = (
        df.sort_values(["driver_id", "season", "round"])
        .groupby("driver_id", as_index=False)
        .tail(1)[driver_cols]
        .copy()
    )

    return latest


def latest_constructor_snapshot(df):
    constructor_cols = [
        "constructor_id",
        "constructor_prior_points",
        "constructor_prior_wins",
        "constructor_prior_podiums",
    ]

    latest = (
        df.sort_values(["constructor_id", "season", "round"])
        .groupby("constructor_id", as_index=False)
        .tail(1)[constructor_cols]
        .drop_duplicates(subset=["constructor_id"])
        .copy()
    )

    return latest


def build_track_history(df):
    track_history = (
        df.sort_values(["driver_id", "circuit_id", "season", "round"])
        .groupby(["driver_id", "circuit_id"], as_index=False)
        .tail(1)[["driver_id", "circuit_id", "avg_finish_at_track", "podiums_at_track"]]
        .copy()
    )
    return track_history


def main():
    os.makedirs(BASE_DIR / "model", exist_ok=True)
    os.makedirs(BASE_DIR / "src" / "data", exist_ok=True)

    df = pd.read_csv(DATA_PATH)
    calendar_df = pd.read_csv(CALENDAR_PATH)

    numeric_cols = FEATURE_COLS + ["season", "round", "podium"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Training data includes all history through completed 2026 rounds
    train_df = df[
        (df["season"] < 2026) | ((df["season"] == 2026) & (df["round"].isin(COMPLETED_2026_ROUNDS)))
    ].copy()

    latest_2026 = df[
        (df["season"] == 2026) & (df["round"].isin(COMPLETED_2026_ROUNDS))
    ].copy()

    if latest_2026.empty:
        raise ValueError("No completed 2026 races found in modeling_dataset.csv")

    drivers_latest = latest_driver_snapshot(latest_2026)
    constructors_latest = latest_constructor_snapshot(latest_2026)
    track_history = build_track_history(df[df["season"] <= 2026].copy())

    upcoming = calendar_df[calendar_df["race_status"] == "upcoming"].copy()
    canceled = calendar_df[calendar_df["race_status"] == "canceled"].copy()
    completed = calendar_df[calendar_df["race_status"] == "completed"].copy()

    future_rows = []
    for _, race in upcoming.iterrows():
        race_circuit = race["circuit_id"]

        race_df = drivers_latest.copy()
        race_df["season"] = 2026
        race_df["round"] = race["round"]
        race_df["race_name"] = race["race_name"]
        race_df["race_date"] = race["race_date"]
        race_df["circuit_id"] = race_circuit

        race_df = race_df.merge(
            constructors_latest,
            on="constructor_id",
            how="left",
            suffixes=("", "_constructor")
        )

        race_df = race_df.merge(
            track_history,
            on=["driver_id", "circuit_id"],
            how="left"
        )

        future_rows.append(race_df)

    predict_df = pd.concat(future_rows, ignore_index=True)

    probs = fit_ensemble_and_predict(train_df, predict_df)
    predict_df["predicted_podium_probability"] = probs
    predict_df["driver"] = (
        predict_df["given_name"].fillna("") + " " + predict_df["family_name"].fillna("")
    ).str.strip()

    predict_df = predict_df.sort_values(
        ["season", "round", "predicted_podium_probability"],
        ascending=[True, True, False]
    ).reset_index(drop=True)

    predict_df["predicted_rank"] = (
        predict_df.groupby(["season", "round", "race_name"])["predicted_podium_probability"]
        .rank(method="first", ascending=False)
        .astype(int)
    )

    predict_df["predicted_podium_flag"] = (predict_df["predicted_rank"] <= 3).astype(int)
    predict_df["predicted_winner_flag"] = (predict_df["predicted_rank"] == 1).astype(int)

    output_cols = [
        "season",
        "round",
        "race_name",
        "race_date",
        "circuit_id",
        "driver_id",
        "given_name",
        "family_name",
        "driver",
        "constructor_name",
        "predicted_podium_probability",
        "predicted_rank",
        "predicted_podium_flag",
        "predicted_winner_flag",
    ]

    predict_df[output_cols].to_csv(OUTPUT_CSV_PATH, index=False)

    completed_actuals = df[
        (df["season"] == 2026) & (df["round"].isin(COMPLETED_2026_ROUNDS)) & (df["podium"] == 1)
    ].copy()

    completed_payload = []
    for _, race in completed.iterrows():
        race_rows = completed_actuals[completed_actuals["round"] == race["round"]].sort_values("position")
        completed_payload.append({
            "season": 2026,
            "round": int(race["round"]),
            "grand_prix": race["race_name"],
            "race_status": "completed",
            "actual_top3": [
                {
                    "finish_position": int(row["position"]),
                    "driver": f"{row['given_name']} {row['family_name']}".strip(),
                    "team": row["constructor_name"],
                }
                for _, row in race_rows.iterrows()
            ]
        })

    canceled_payload = [
        {
            "season": 2026,
            "round": None,
            "grand_prix": row["race_name"],
            "race_status": "canceled",
            "message": "Canceled — no prediction generated"
        }
        for _, row in canceled.iterrows()
    ]

    upcoming_payload = []
    for (season, rnd, race_name), group in predict_df.groupby(["season", "round", "race_name"], sort=True):
        group = group.sort_values("predicted_rank")
        upcoming_payload.append({
            "season": int(season),
            "round": int(rnd),
            "grand_prix": race_name,
            "race_status": "upcoming",
            "predictions": [
                {
                    "rank": int(row["predicted_rank"]),
                    "driver": row["driver"],
                    "team": row["constructor_name"],
                    "probability": round(float(row["predicted_podium_probability"]) * 100, 1),
                }
                for _, row in group.head(10).iterrows()
            ]
        })

    payload = {
        "completed": completed_payload,
        "canceled": canceled_payload,
        "upcoming": upcoming_payload,
    }

    with open(OUTPUT_JSON_PATH, "w") as f:
        json.dump(payload, f, indent=2)

    print(f"Created: {OUTPUT_CSV_PATH}")
    print(f"Created: {OUTPUT_JSON_PATH}")
    print("\nUpcoming races predicted:", len(upcoming_payload))
    if upcoming_payload:
        print("\nSample next race prediction:")
        print(upcoming_payload[0])
    print("\nCanceled races captured:", len(canceled_payload))
    print("Completed races captured:", len(completed_payload))


if __name__ == "__main__":
    main()