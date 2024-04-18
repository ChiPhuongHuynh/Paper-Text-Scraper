import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from sklearn.model_selection import train_test_split
from keras import ops
from matplotlib import pyplot

df = pd.read_csv("dataprocessed.csv", index_col=False)
df.dropna(inplace=True)
bool_cols = df.columns.to_list()[:-2]

df[bool_cols] = df[bool_cols].astype(int)
#print(df)
round_cols = ['accuracy_norm', 'difficulty']
df[round_cols] = df[round_cols].round(2)
print(df)

y = df['difficulty']
X = df.drop('difficulty', axis=1)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
#print(X_train.tail(X_train.shape[0]-1))
print(X_train.shape[1])

model = keras.Sequential([
    keras.layers.Dense(6, activation='relu', input_shape=(X_train.shape[1],)),
    keras.layers.Dense(6, activation='relu'),
    keras.layers.Dense(1)
])
#Optimizer and Metrics
opt = keras.optimizers.Adam(learning_rate=0.0001)
model.compile(optimizer=opt, loss='mean_squared_error', metrics = ['mse', 'mae','mape','cosine_similarity'])

# Train the model
history = model.fit(X_train, y_train, epochs=100, batch_size=32, validation_split=0.1, verbose=2)

# Evaluate the model on the test set
loss= model.evaluate(X_test, y_test)
print('Test loss:', loss)
predictions = model.predict(X_test)

model.save('prediction.keras')

#plot metrics
pyplot.plot(history.history['mse'], "-b", label = "Mean Squared Error")
pyplot.plot(history.history['mae'], "-r", label = "Mean Absolute Error")
#pyplot.plot(history.history['mape'], "-g", label = "Mean Absolute Percentage Error")
pyplot.plot(history.history['cosine_similarity'], "-y", label = "Cosine Similarity")
pyplot.legend(loc="upper right")
pyplot.ylim(-1.5, 2.0)
pyplot.title("Metrics of Difficulty Estimation Model")
pyplot.xlabel("Epoch")
pyplot.savefig('data.png', bbox_inches='tight')
pyplot.close()