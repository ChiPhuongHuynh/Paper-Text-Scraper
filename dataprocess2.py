from scipy.spatial.distance import euclidean, pdist, squareform
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

df = pd.read_csv("complete2.csv", delimiter=",", index_col=False)
df1 = pd.read_csv("pvi.csv", index_col=False)
print(df1.head())
dt = list(df1['Dataset'])
#dt = [x[1:] for x in dt]
#print(dt)
new_df = df[(df['Task'] == "Image Classification")]
df = new_df[(new_df['Dataset'].isin(dt))]
print(df.head())
df2 = pd.read_csv("normalized-task-data2.csv", index_col=False)
merged_df = pd.merge(df, df1[['Task', 'Dataset', 'PVI']], on=['Task', 'Dataset'], how='left')
merged_df = pd.merge(merged_df, df2[['Task','Dataset','PVI','difficulty']], on=['Task','Dataset'],how='left')

print(merged_df)

X_categorical = pd.get_dummies(merged_df[['Task']], drop_first=True)
X_numerical = merged_df[['accuracy_norm', 'difficulty']]
X_processed = pd.concat([X_categorical, X_numerical], axis=1)

print(X_processed)

X_processed.to_csv("dataprocessed5.csv", index=False)
