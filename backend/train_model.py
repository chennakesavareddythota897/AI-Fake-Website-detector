import csv
import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

from features import extract_features, features_to_vector, FEATURE_ORDER


def load_dataset(path="dataset.csv"):
    urls, labels = [], []
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            urls.append(row["url"])
            labels.append(int(row["label"]))
    return urls, labels


def main():
    urls, labels = load_dataset()
    X = np.array([features_to_vector(extract_features(u)) for u in urls])
    y = np.array(labels)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=8,
        random_state=42,
        class_weight="balanced",
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print(classification_report(y_test, y_pred, target_names=["Legit", "Phishing"]))

    joblib.dump(model, "model.pkl")
    print("\nSaved model -> model.pkl")


if __name__ == "__main__":
    main()