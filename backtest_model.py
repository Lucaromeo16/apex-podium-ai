import json
import os
from pathlib import Path

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

try:
    from xgboost import XGBClassifier
    XGBOOST_AVAILABLE = True
except Exception:
    XGBOOST_AVAILABLE = False


BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "processed" / "modeling_dataset.csv"
OUTPUT_CSV_PATH = BASE_DIR / "model" / "historical_backtest.csv"
OUTPUT_JSON_PATH = BASE_DIR / "src" / "data" / "historical_backtest.json"


FEATURE_COLS = [
    "grid",
    "qualifying_position",
    "avg_finish_last_3",
    "avg_finish_last_5",
    "podiums_last_3",
    "podiums_last_5",
    "dnfs_last_5",
    "avg_finish_at_track",
    "podiums_at_track",
]

TARGET_SEASONS = [2021, 2022, 2023, 2024, 2025]
MIN_TRAIN_ROWS = 20


def build_pipeline(model):
    preprocessor = ColumnTransformer(
        transformers=[
            (
                "num",
                Pipeline(
                    steps=[
                        ("imputer", SimpleImputer(strategy="median")),
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
        "logistic_regression": LogisticRegression(max_iter=1000, random_state=42),
        "random_forest": RandomForestClassifier(
            n_estimators=300,
            max_depth=8,
            random_state=42,
        ),
    }

    if XGBOOST_AVAILABLE:
        models["xgboost"] = XGBClassifier(
            n_estimators=250,
            max_depth=4,
            learning_rate=0.05,
            subsample=0.9,
            colsample_bytree=0.9,
            eval_metric="logloss",
            random_state=42,
        )

    return models


def fit_ensemble_and_predict(train_df, test_df):
    X_train = train_df[FEATURE_COLS]
    y_train = train_df["podium"]

    X_test = test_df[FEATURE_COLS]

    model_probs = {}
    models = get_models()

    for model_name, model in models.items():
        pipeline = build_pipeline(model)
        pipeline.fit(X_train, y_train)
        probs = pipeline.predict_proba(X_test)[:, 1]
        model_probs[model_name] = probs

    logistic_probs = model_probs.get("logistic_regression", 0)
    rf_probs = model_probs.get("random_forest", 0)
    xgb_probs = model_probs.get("xgboost", 0)

    if isinstance(xgb_probs, int):
        xgb_probs = 0

    ensemble_probs = (
        0.50 * logistic_probs
        + 0.30 * rf_probs
        + 0.20 * xgb_probs
    )

    return ensemble_probs


def main():
    df = pd.read_csv(DATA_PATH)

    keep_cols = [
        "season",
        "round",
        "race_name",
        "race_date",
        "given_name",
        "family_name",
        "constructor_name",
        "position",
        "podium",
    ] + FEATURE_COLS

    df = df[keep_cols].copy()

    # Only require essential columns; allow feature missing values so imputer can handle them
    df = df.dropna(
        subset=[
            "season",
            "round",
            "race_name",
            "given_name",
            "family_name",
            "constructor_name",
            "position",
            "podium",
        ]
    ).reset_index(drop=True)

    df = df.sort_values(["season", "round"]).reset_index(drop=True)

    target_df = df[df["season"].isin(TARGET_SEASONS)].copy()

    unique_races = (
        target_df[["season", "round", "race_name", "race_date"]]
        .drop_duplicates()
        .sort_values(["season", "round"])
        .reset_index(drop=True)
    )

    all_predictions = []
    skipped_races = []

    for _, race_row in unique_races.iterrows():
        season = race_row["season"]
        rnd = race_row["round"]
        race_name = race_row["race_name"]

        test_mask = (df["season"] == season) & (df["round"] == rnd)
        train_mask = (df["season"] < season) | ((df["season"] == season) & (df["round"] < rnd))

        train_df = df[train_mask].copy()
        test_df = df[test_mask].copy()

        # Skip only if truly not enough prior information
        if len(train_df) < MIN_TRAIN_ROWS or len(test_df) == 0:
            skipped_races.append((season, rnd, race_name, len(train_df)))
            continue

        probs = fit_ensemble_and_predict(train_df, test_df)

        race_preds = test_df.copy()
        race_preds["driver"] = (
            race_preds["given_name"].fillna("") + " " + race_preds["family_name"].fillna("")
        ).str.strip()

        race_preds["predicted_podium_probability"] = probs
        race_preds = race_preds.sort_values(
            "predicted_podium_probability", ascending=False
        ).reset_index(drop=True)

        race_preds["predicted_rank"] = race_preds.index + 1
        race_preds["predicted_podium_flag"] = (race_preds["predicted_rank"] <= 3).astype(int)
        race_preds["actual_podium_flag"] = race_preds["podium"].astype(int)
        race_preds["correct_prediction"] = (
            race_preds["predicted_podium_flag"] == race_preds["actual_podium_flag"]
        ).astype(int)

        actual_winner = race_preds.loc[race_preds["position"] == 1, "driver"]
        predicted_winner = race_preds.loc[race_preds["predicted_rank"] == 1, "driver"]

        actual_winner = actual_winner.iloc[0] if len(actual_winner) > 0 else None
        predicted_winner = predicted_winner.iloc[0] if len(predicted_winner) > 0 else None

        predicted_top3 = set(race_preds.loc[race_preds["predicted_rank"] <= 3, "driver"])
        actual_top3 = set(race_preds.loc[race_preds["actual_podium_flag"] == 1, "driver"])

        top3_overlap = len(predicted_top3.intersection(actual_top3))
        winner_hit = int(predicted_winner == actual_winner) if predicted_winner and actual_winner else 0

        race_preds["top3_overlap"] = top3_overlap
        race_preds["winner_hit"] = winner_hit
        race_preds["race_correct_label"] = f"{top3_overlap}/3 correct"

        all_predictions.append(race_preds)

    if not all_predictions:
        raise ValueError("No backtest predictions were created. There may not be enough prior race data.")

    backtest_df = pd.concat(all_predictions, ignore_index=True)

    y_true = backtest_df["actual_podium_flag"]
    y_pred = backtest_df["predicted_podium_flag"]

    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred, zero_division=0)
    recall = recall_score(y_true, y_pred, zero_division=0)

    backtest_df.to_csv(OUTPUT_CSV_PATH, index=False)
    print(f"Created: {OUTPUT_CSV_PATH}")

    os.makedirs(BASE_DIR / "src" / "data", exist_ok=True)

    race_summaries = []
    race_groups = backtest_df.groupby(["season", "round", "race_name"], sort=True)

    for (season, rnd, race_name), group in race_groups:
        group = group.sort_values("predicted_rank")

        predicted_top3_rows = group[group["predicted_rank"] <= 3].sort_values("predicted_rank")
        actual_top3_rows = group[group["actual_podium_flag"] == 1].sort_values("position")

        predicted_top3 = [
            {
                "rank": int(row["predicted_rank"]),
                "driver": row["driver"],
                "team": row["constructor_name"],
                "probability": round(float(row["predicted_podium_probability"]) * 100, 1),
            }
            for _, row in predicted_top3_rows.iterrows()
        ]

        actual_top3 = [
            {
                "finish_position": int(row["position"]),
                "driver": row["driver"],
                "team": row["constructor_name"],
            }
            for _, row in actual_top3_rows.iterrows()
        ]

        full_rankings = [
            {
                "predicted_rank": int(row["predicted_rank"]),
                "driver": row["driver"],
                "team": row["constructor_name"],
                "probability": round(float(row["predicted_podium_probability"]) * 100, 1),
                "actual_finish": int(row["position"]) if pd.notna(row["position"]) else None,
                "actual_podium": int(row["actual_podium_flag"]),
                "predicted_podium": int(row["predicted_podium_flag"]),
                "correct_prediction": int(row["correct_prediction"]),
            }
            for _, row in group.sort_values("predicted_rank").iterrows()
        ]

        top3_overlap = int(group["top3_overlap"].iloc[0])
        winner_hit = int(group["winner_hit"].iloc[0])

        race_summaries.append(
            {
                "season": int(season),
                "round": int(rnd),
                "grand_prix": race_name,
                "predicted_top3": predicted_top3,
                "actual_top3": actual_top3,
                "top3_overlap": top3_overlap,
                "winner_hit": winner_hit,
                "result_label": f"{top3_overlap}/3 predicted podium drivers were correct",
                "full_rankings": full_rankings,
            }
        )

    season_counts = (
        pd.DataFrame(race_summaries)["season"]
        .value_counts()
        .sort_index()
        .to_dict()
    )

    total_races = len(race_summaries)
    winner_hits = sum(race["winner_hit"] for race in race_summaries)
    top3_overlap_total = sum(race["top3_overlap"] for race in race_summaries)
    races_with_2plus = sum(1 for race in race_summaries if race["top3_overlap"] >= 2)

    output = {
        "summary_metrics": {
            "accuracy": round(float(accuracy) * 100, 1),
            "precision": round(float(precision) * 100, 1),
            "recall": round(float(recall) * 100, 1),
            "winner_hit_rate": round((winner_hits / total_races) * 100, 1) if total_races else 0.0,
            "avg_top3_overlap": round((top3_overlap_total / total_races), 2) if total_races else 0.0,
            "races_with_2plus_correct": round((races_with_2plus / total_races) * 100, 1) if total_races else 0.0,
        },
        "season_counts": {str(k): int(v) for k, v in season_counts.items()},
        "skipped_races": [
            {
                "season": int(season),
                "round": int(rnd),
                "grand_prix": race_name,
                "prior_training_rows": int(train_rows),
            }
            for season, rnd, race_name, train_rows in skipped_races
        ],
        "races": race_summaries,
    }

    with open(OUTPUT_JSON_PATH, "w") as f:
        json.dump(output, f, indent=2)

    print(f"Created: {OUTPUT_JSON_PATH}")
    print("\nSummary metrics:")
    print(output["summary_metrics"])
    print("\nBacktested races by season:")
    print(output["season_counts"])
    print(f"\nSkipped races: {len(skipped_races)}")


if __name__ == "__main__":
    main()