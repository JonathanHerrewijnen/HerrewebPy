from herrewebpy import logger

import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import StandardScaler


def perceptron_build_model(df, hidden_units=64):
    numerical_features = df.select_dtypes(include=[np.number])

    # Standardize the numerical features
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(numerical_features)

    # Define the Perceptron model
    input_dim = scaled_data.shape[1]

    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(input_dim,)),
        tf.keras.layers.Dense(hidden_units, activation='relu'),
        tf.keras.layers.Dense(1)  # Output layer for regression
    ])

    # Compile the model
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model, scaled_data


def train_model(df):
    model, scaled_data = perceptron_build_model(df)
    epochs = 100
    batch_size = 32

    model.fit(scaled_data, scaled_data, epochs=epochs, batch_size=batch_size, verbose=1)
