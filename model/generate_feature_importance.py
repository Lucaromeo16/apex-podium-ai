"""
Generate feature importance from trained XGBoost model.
Outputs JSON for frontend display.
"""

from __future__ import annotations

import json
import warnings
from pathlib import Path

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

try:
    from xgboost import XGBClassifier
    XGBOOST_AVAILABLE = True
except Exception:
    XGBOOST_AVAILABLE = False

warnings.filterwarnings("ignore")

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR.parent / "data" / "processed" / "modeling_dataset.csv"
OUTPUT_PATH = BASE_DIR.parent / "src" / "data" / "feature_importance.json"

# Human-readable feature labels
FEATURE_LABELS = {
    "grid": "Grid Position",
    "qualifying_position": "Qualifying Position",
    "avg_finish_last_3": "Avg Finish (Last 3 Races)",
    "avg_finish_last_5": "Avg Finish (Last 5 Races)",
    "podiums_last_3": "Podiums (Last 3 Races)",
    "podiums_last_5": "Podiums (Last 5 Races)",
    "dnfs_last_5": "DNFs (Last 5 Races)",
    "avg_finish_at_track": "Avg Finish at Track",
    "podiums_at_track": "Podiums at Track",
}


def build_feature_lists():
    return [
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


def time_based_split(df):
    df = df.sort_values(["season", "round"]).reset_index(drop=True)
    split_idx = int(len(df) * 0.8)
    return df.iloc[:split_idx].copy(), df.iloc[split_idx:].copy()


def build_pipeline(model, feature_cols):
    transformer = ColumnTransformer(
        transformers=[
            (
                "num",
                Pipeline(
                    steps=[
                        ("imputer", SimpleImputer(strategy="median")),
                        ("scaler", StandardScaler()),
                    ]
                ),
                feature_cols,
            )
        ],
        remainder="drop",
    )

    return Pipeline(
        steps=[
            ("prep", transformer),
            ("model", model),
        ]
    )


def main():
    print("Loading data...")
    df = pd.read_csv(DATA_PATH)
    feature_cols = build_feature_lists()

    # Drop rows with missing features or target
    df = df.dropna(subset=feature_cols + ["podium"]).reset_index(drop=True)

    train_df, test_df = time_based_split(df)

    X_train = train_df[feature_cols]
    y_train = train_df["podium"]

    # Use XGBoost if available, otherwise Random Forest
    if XGBOOST_AVAILABLE:
        print("Training XGBoost model for feature importance...")
        model = XGBClassifier(
            n_estimators=250,
            max_depth=4,
            learning_rate=0.05,
            subsample=0.9,
            colsample_bytree=0.9,
            eval_metric="logloss",
            random_state=42,
        )
        model_name = "XGBoost"
    else:
        print("Training Random Forest model for feature importance...")
        model = RandomForestClassifier(
            n_estimators=300,
            max_depth=8,
            random_state=42,
        )
        model_name = "Random Forest"

    # Build and fit pipeline
    pipeline = build_pipeline(model, feature_cols)
    pipeline.fit(X_train, y_train)

    # Get feature importance from the model
    # XGBoost and Random Forest both have feature_importances_
    importances = pipeline.named_steps["model"].feature_importances_

    # Create feature importance list
    feature_importance_list = []
    for feature, importance in zip(feature_cols, importances):
        feature_importance_list.append({
            "feature": feature,
            "label": FEATURE_LABELS.get(feature, feature),
            "importance": float(importance),
        })

    # Sort by importance (descending)
    feature_importance_list.sort(key=lambda x: x["importance"], reverse=True)

    # Calculate percentages
    total_importance = sum(item["importance"] for item in feature_importance_list)
    for item in feature_importance_list:
        item["importance_percent"] = round((item["importance"] / total_importance) * 100, 1)

    # Create output structure
    output = {
        "model_used": model_name,
        "description": "These features were among the most influential drivers of podium predictions in the model.",
        "features": feature_importance_list,
    }

    # Save to JSON
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(output, f, indent=2)

    print(f"\nFeature importance saved to: {OUTPUT_PATH}")
    print(f"\nModel used: {model_name}")
    print("\nTop features by importance:")
    for i, item in enumerate(feature_importance_list[:5], 1):
        print(f"  {i}. {item['label']}: {item['importance_percent']}%")


if __name__ == "__main__":
    main()