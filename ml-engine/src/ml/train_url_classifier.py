"""
Entraîne un modèle de régression logistique pour détecter le phishing
à partir des caractéristiques lexicales d'une URL.
"""

import os

import joblib
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

DATA_PATH = os.path.join(os.path.dirname(__file__), "url_dataset.csv")
MODEL_OUTPUT = os.path.join(os.path.dirname(__file__), "phishing_url_model.joblib")


def main():
    df = pd.read_csv(DATA_PATH)
    feature_columns = [col for col in df.columns if col != "label"]

    X = df[feature_columns]
    y = df["label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Mise à l'échelle des features : indispensable pour la régression logistique,
    # car url_length (ex: 80) et uses_https (0 ou 1) n'ont pas la même amplitude.
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    print(f"Entraînement sur {len(X_train)} échantillons, test sur {len(X_test)}.")

    model = LogisticRegression(class_weight="balanced", max_iter=1000, random_state=42)
    model.fit(X_train_scaled, y_train)

    y_pred = model.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)

    print()
    print(f"Précision (accuracy) sur le jeu de test : {accuracy:.2%}")
    print()
    print("Rapport de classification détaillé :")
    print(classification_report(y_test, y_pred, target_names=["légitime", "phishing"]))

    joblib.dump({"model": model, "scaler": scaler, "feature_columns": feature_columns}, MODEL_OUTPUT)
    print()
    print(f"Modèle sauvegardé dans {MODEL_OUTPUT}")


if __name__ == "__main__":
    main()