import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from sklearn.model_selection import train_test_split

df = pd.read_csv("dataprocessed.csv", index_col=False)
df.dropna(inplace=True)
bool_cols = ['Dataset_CIFAR-10','Dataset_CIFAR-100','Dataset_COCO','Dataset_COCO minivar','Dataset_CityScapes','Dataset_ImageNet','Dataset_KITTI','Dataset_MNIST','Dataset_NYU Depth v2',
        'Dataset_SVHN','Dataset_ShapeNet','Task_Depth Estimation','Task_Image Classification','Task_Object Detection','Task_Semantic Segmentation','Task_Text to Image']
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
opt = keras.optimizers.Adam(learning_rate=0.0001)
model.compile(optimizer=opt, loss='mean_squared_error')

# Train the model
model.fit(X_train, y_train, epochs=50, batch_size=32, validation_split=0.1)

# Evaluate the model on the test set
loss= model.evaluate(X_test, y_test)
print('Test loss:', loss)
predictions = model.predict(X_test)
#print(predictions)