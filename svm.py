import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.linear_model import LinearRegression
from matplotlib import pyplot as plt
from sklearn import metrics
from keras import backend as K
from sklearn.metrics import mean_squared_error

df = pd.read_csv("dataprocessed.csv", index_col=False)
df.dropna(inplace=True)
df = df.sort_values(by=['accuracy_norm'])
#print(df)
bool_cols = df.columns.to_list()[:-2]

df[bool_cols] = df[bool_cols].astype(int)
#print(df)
round_cols = ['accuracy_norm', 'difficulty']
df[round_cols] = df[round_cols].round(2)
#print(df)
# Remove the dataset one hot encoding
y = df['difficulty']
X = df.drop('difficulty', axis=1)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


model = svm.SVR(kernel = 'rbf')
#model = LinearRegression()
#Train the model using the training sets
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
scores = model.score(X_test, y_test)
print("MSE: " + str(mean_squared_error(y_test, y_pred)))
def plot(X_test, y_test, y_pred):
    plt.scatter(X_test['accuracy_norm'],y_test, color='darkorange',label='data')
    plt.scatter(X_test['accuracy_norm'],y_pred, color='cornflowerblue', label='prediction')
    plt.legend()
    plt.ylabel("Difficulty")
    plt.xlabel("Normalized Accuracy")
    plt.savefig('linearreg.png', bbox_inches='tight')


print("R2: " + str(scores))