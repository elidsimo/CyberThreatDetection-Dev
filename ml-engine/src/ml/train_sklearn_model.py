"""
Entraîne un modèle Random Forest pour prédire le niveau de risque
d'un indicateur de menace, à partir de son type, sa source et son pays.
"""

import os

import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.model_selection import train_test_split

from preprocessing import load_and_prepare_data

MODEL_OUTPUT = os.path.join(os.path.dirname(__file__), "risk_model_sklearn.joblib")


def main():
    X, y, encoders, df = load_and_prepare_data()

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print(f"Entraînement sur {len(X_train)} échantillons, test sur {len(X_test)}.")

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    print()
    print(f"Précision (accuracy) sur le jeu de test : {accuracy:.2%}")
    print()
    print("Rapport de classification détaillé :")
    print(classification_report(y_test, y_pred))

    joblib.dump({"model": model, "encoders": encoders}, MODEL_OUTPUT)
    print()
    print(f"Modèle sauvegardé dans {MODEL_OUTPUT}")


if __name__ == "__main__":
    main()