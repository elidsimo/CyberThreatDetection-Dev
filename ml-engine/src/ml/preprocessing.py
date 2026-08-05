"""
Prépare les données pour l'entraînement :
- Crée la colonne cible 'risk_level' (low/medium/high) à partir de severity_score.
- Encode les variables catégorielles (indicator_type, source, country) en nombres.
"""

import os

import pandas as pd
from sklearn.preprocessing import LabelEncoder

DATA_PATH = os.path.join(os.path.dirname(__file__), "threat_data.csv")


def severity_to_risk_level(score, threshold):
    """Convertit un score numérique en catégorie de risque binaire, selon un seuil calculé dynamiquement."""
    return "high_risk" if score > threshold else "standard"


def load_and_prepare_data():
    df = pd.read_csv(DATA_PATH)

    # Nettoyage minimal : on retire les lignes avec des valeurs manquantes sur les colonnes clés
    df = df.dropna(subset=["indicator_type", "source", "country", "severity_score"])

    threshold = df["severity_score"].median()
    print(f"Seuil calculé (médiane) : standard <= {threshold:.1f} < high_risk")

    # Création de la cible à partir de severity_score
    df["risk_level"] = df["severity_score"].apply(lambda s: severity_to_risk_level(s, threshold))

    # Encodage des features catégorielles en entiers
    encoders = {}
    for column in ["indicator_type", "source", "country"]:
        le = LabelEncoder()
        df[f"{column}_encoded"] = le.fit_transform(df[column])
        encoders[column] = le

    feature_columns = ["indicator_type_encoded", "source_encoded", "country_encoded"]
    X = df[feature_columns]
    y = df["risk_level"]

    return X, y, encoders, df


if __name__ == "__main__":
    X, y, encoders, df = load_and_prepare_data()
    print(f"{len(X)} lignes préparées pour l'entraînement.")
    print(f"\nRépartition des niveaux de risque :\n{y.value_counts()}")
    print(f"\nAperçu des features encodées :\n{X.head()}")