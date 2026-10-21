
from pathlib import Path

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.base import BaseEstimator, TransformerMixin

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "dataset" / "profiles.csv"
MODEL_DIR = BASE_DIR / "model"
MODEL_PATH = MODEL_DIR / "fake_profile_model.joblib"

TEXT_COLUMNS = ["bio"]
NUMERIC_COLUMNS = [
    "followers",
    "following",
    "posts",
    "account_age_days",
]


def main():
    MODEL_DIR.mkdir(exist_ok=True)

    data = pd.read_csv(DATA_PATH)
    data = data.dropna(subset=["bio", "label"]).copy()
    data["label"] = data["label"].str.lower().str.strip()

    data = data[data["label"].isin(["fake", "genuine"])]

    if len(data) < 10 or data["label"].nunique() < 2:
        raise ValueError("Dataset needs at least 10 rows and both labels.")

    X = data[TEXT_COLUMNS + NUMERIC_COLUMNS]
    y = data["label"]

    # Keep the pipeline simple and combine text and numeric features.
    preprocessor = ColumnTransformer(
        transformers=[
            (
                "bio_text",
                TfidfVectorizer(
                    lowercase=True,
                    stop_words="english",
                    ngram_range=(1, 2),
                ),
                "bio",
            ),
            (
                "profile_numbers",
                Pipeline([
                    ("imputer", SimpleImputer(strategy="constant", fill_value=0)),
                    ("scaler", StandardScaler()),
                ]),
                NUMERIC_COLUMNS,
            ),
        ]
    )

    model = Pipeline([
        ("features", preprocessor),
        ("classifier", RandomForestClassifier(
            n_estimators=100,
            random_state=42,
            class_weight="balanced",
        )),
    ])

    # Stratified split: keep both classes represented in train and test.
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.3,
        random_state=42,
        stratify=y,
    )

    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    print("\nModel evaluation")
    print("----------------")
    print(f"Test accuracy: {accuracy_score(y_test, predictions):.2%}")
    print(classification_report(y_test, predictions, zero_division=0))

    joblib.dump(model, MODEL_PATH)
    print(f"Model saved to: {MODEL_PATH}")


if __name__ == "__main__":
    main()