
import os

import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow import keras

from preprocessing import load_and_prepare_data

MODEL_OUTPUT = os.path.join(os.path.dirname(__file__), "risk_model_tensorflow.keras")


def main():
    X, y, encoders, df = load_and_prepare_data()

    # TensorFlow attend des labels numériques, pas du texte ("low"/"medium"/"high")
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)
    num_classes = len(label_encoder.classes_)

    X_train, X_test, y_train, y_test = train_test_split(
        X.values, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
    )

    print(f"Entraînement sur {len(X_train)} échantillons, test sur {len(X_test)}.")

    model = keras.Sequential([
        keras.layers.Input(shape=(X_train.shape[1],)),
        keras.layers.Dense(16, activation="relu"),
        keras.layers.Dense(8, activation="relu"),
        keras.layers.Dense(num_classes, activation="softmax"),
    ])

    model.compile(
        optimizer="adam",
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )

    history = model.fit(
        X_train, y_train,
        validation_split=0.1,
        epochs=30,
        batch_size=32,
        verbose=1,
    )

    test_loss, test_accuracy = model.evaluate(X_test, y_test, verbose=0)
    print(f"\Précision (accuracy) sur le jeu de test : {test_accuracy:.2%}")

    model.save(MODEL_OUTPUT)
    print(f"Modèle sauvegardé dans {MODEL_OUTPUT}")

    # Sauvegarde de l'encodeur de labels pour pouvoir décoder les prédictions plus tard
    import joblib
    joblib.dump(label_encoder, os.path.join(os.path.dirname(__file__), "tf_label_encoder.joblib"))


if __name__ == "__main__":
    main()