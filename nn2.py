import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from keras import ops
from matplotlib import pyplot as plt
import tensorflow.keras.backend as K

df = pd.read_csv("dataprocessed3.csv", index_col=False)
df.dropna(inplace=True)
df = df.sort_values(by=['accuracy_norm'])

round_cols = ['accuracy_norm', 'PVI']
df[round_cols] = df[round_cols].round(2)

# Remove the dataset one hot encoding
y = df['PVI']
X = df.drop('PVI', axis=1)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Build and Train the Model
model = keras.Sequential([
    keras.layers.Dense(2, activation='relu', input_shape=(X_train.shape[1],)),
    keras.layers.Dense(2, activation='relu'),
    keras.layers.Dense(1)
])

#Optimizer and Metrics
opt = keras.optimizers.Adam(learning_rate=0.0001)
model.compile(optimizer=opt, loss='mean_squared_error')
#'mse', 'mae','mape','cosine_similarity'
# Train the model
history = model.fit(X_train, y_train, epochs=100, batch_size=64, validation_split=0.1, verbose=2)

# Evaluate the model on the test set
predictions = model.predict(X_test)

mse = mean_squared_error(y_test, predictions)
mae = mean_absolute_error(y_test, predictions)
r2 = r2_score(y_test, predictions)

print(f'Mean Squared Error (MSE): {mse:.4f}')
print(f'Mean Absolute Error (MAE): {mae:.4f}')
print(f'R² Score: {r2:.4f}')

"""loss = model.evaluate(X_test, y_test)
print('Test loss:', loss)
predictions = model.predict(X_test)"""

model.save('prediction_nodt.keras')

def coeff_determination(y_true, y_pred):
    y_true = tf.convert_to_tensor(y_true, dtype=tf.float32)
    SS_res =  K.sum(K.square( y_true-y_pred ))
    SS_tot = K.sum(K.square( y_true - K.mean(y_true) ) )
    return ( 1 - SS_res/(SS_tot + K.epsilon()) )
def plot(history):
    plt.plot(history.history['mse'], "-b", label = "Mean Squared Error")
    plt.plot(history.history['mae'], "-r", label = "Mean Absolute Error")
    plt.plot(history.history['mape'], "-g", label = "Mean Absolute Percentage Error")
    plt.plot(history.history['cosine_similarity'], "-y", label = "Cosine Similarity")
    plt.legend(loc="upper right")
    plt.ylim(-1.5, 2.0)
    plt.title("Metrics of Difficulty Estimation Model")
    plt.xlabel("Epoch")
print(coeff_determination(y_test, predictions[0]))