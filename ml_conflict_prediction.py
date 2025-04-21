"""
ML-based Merge Conflict Prediction Pipeline for Test Automation
- Extracts features from git history and test coverage
- Trains a Random Forest classifier to predict likely conflicts
- Outputs conflict risk scores for PRs/branches
"""
import os
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

def extract_features(history_csv):
    df = pd.read_csv(history_csv)
    # Advanced features: add test_failure_rate, lines_changed, num_files_changed if present
    feature_cols = ["file_mod_count", "branch_divergence", "coverage_overlap"]
    for col in ["test_failure_rate", "lines_changed", "num_files_changed"]:
        if col in df.columns:
            feature_cols.append(col)
    X = df[feature_cols]
    y = df["conflict"]
    return X, y

def train_model(history_csv, out_model="conflict_predictor.pkl"):
    X, y = extract_features(history_csv)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)
    print(classification_report(y_test, clf.predict(X_test)))
    joblib.dump(clf, out_model)
    print(f"Model saved to {out_model}")

if __name__ == "__main__":
    # Usage: python ml_conflict_prediction.py history.csv
    import sys
    if len(sys.argv) < 2:
        print("Usage: python ml_conflict_prediction.py history.csv")
        exit(1)
    train_model(sys.argv[1])
