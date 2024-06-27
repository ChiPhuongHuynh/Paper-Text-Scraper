import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import matplotlib.pyplot as plt
from sklearn.svm import SVR

df = pd.read_csv("dataprocessed3.csv", index_col=False)
df.dropna(inplace=True)
df = df.sort_values(by=['accuracy_norm'])

#print(df)
#bool_cols = df.columns.to_list()[:-2]
#df[bool_cols] = df[bool_cols].astype(int)

round_cols = ['accuracy_norm', 'PVI']
df[round_cols] = df[round_cols].round(2)

# Remove the dataset one hot encoding
y = df['PVI']
X = df.drop('PVI', axis=1)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

#model = SVR(kernel = 'rbf')
model = LinearRegression()
#Train the model using the training sets
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

# Calculate metrics
mse = mean_squared_error(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f'Mean Squared Error (MSE): {mse:.4f}')
print(f'Mean Absolute Error (MAE): {mae:.4f}')
print(f'R² Score: {r2:.4f}')

def plot(X_test, y_test, y_pred):
    plt.scatter(X_test['accuracy_norm'],y_test, color='darkorange',label='data')
    plt.scatter(X_test['accuracy_norm'],y_pred, color='cornflowerblue', label='prediction')
    plt.legend()
    plt.ylabel("Difficulty")
    plt.xlabel("Normalized Accuracy")
    plt.savefig('linearreg.png', bbox_inches='tight')
