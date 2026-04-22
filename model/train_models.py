from __future__ import annotations

import warnings
from pathlib import Path

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, log_loss, roc_auc_score
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
PREDICTIONS_PATH = BASE_DIR / "predictions.csv"


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


def evaluate_model(name, model, X_train, y_train, X_test, y_test, feature_cols):
    pipeline = build_pipeline(model, feature_cols)
    pipeline.fit(X_train, y_train)

    probs = pipeline.predict_proba(X_test)[:, 1]

    threshold = 0.3
    preds = (probs >= threshold).astype(int)

    metrics = {
        "model": name,
        "accuracy": accuracy_score(y_test, preds),
        "log_loss": log_loss(y_test, probs),
        "roc_auc": roc_auc_score(y_test, probs),
    }

    return metrics, probs


def main():
    df = pd.read_csv(DATA_PATH)

    feature_cols = build_feature_lists()

    metadata_cols = [
        col for col in [
            "season",
            "round",
            "race_name",
            "given_name",
            "family_name",
            "constructor_name",
            "podium",
        ]
        if col in df.columns
    ]

    df = df.dropna(subset=feature_cols + ["podium"]).reset_index(drop=True)

    train_df, test_df = time_based_split(df)

    X_train = train_df[feature_cols]
    y_train = train_df["podium"]

    X_test = test_df[feature_cols]
    y_test = test_df["podium"]

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

    results = []
    prediction_frames = []

    for name, model in models.items():
        metrics, probs = evaluate_model(
            name,
            model,
            X_train,
            y_train,
            X_test,
            y_test,
            feature_cols,
        )
        results.append(metrics)

        temp = test_df[metadata_cols].copy()
        temp["predicted_podium_probability"] = probs
        temp["model"] = name
        prediction_frames.append(temp)

    results_df = pd.DataFrame(results).sort_values("log_loss")

    print("\nModel comparison:")
    print(results_df.to_string(index=False))

    combined_predictions = pd.concat(prediction_frames, ignore_index=True)

    output_cols = [
        col for col in [
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
        if col in combined_predictions.columns
    ]

    combined_predictions[output_cols].to_csv(PREDICTIONS_PATH, index=False)

    print(f"\nSaved predictions to: {PREDICTIONS_PATH}")
    print("\nSaved columns:")
    print(output_cols)


if __name__ == "__main__":
    main()