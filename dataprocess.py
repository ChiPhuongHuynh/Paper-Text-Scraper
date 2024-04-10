from scipy.spatial.distance import euclidean, pdist, squareform
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
df1 = pd.read_csv("normalized-task-data.csv", delimiter=",", index_col=False)
df = pd.read_csv("complete.csv", delimiter=",", index_col=False)

merged_df = pd.merge(df, df1[['Task', 'Dataset', 'difficulty']], on=['Task', 'Dataset'], how='left')
#print(merged_df)
X_categorical = pd.get_dummies(merged_df[['Dataset', 'Task']], drop_first=True)
X_numerical = merged_df[['accuracy', 'accuracy_norm', 'difficulty']]
X_processed = pd.concat([X_categorical, X_numerical], axis=1)

print(X_processed)

#max_accuracy_df = df.groupby(['Dataset', 'Task'])['accuracy'].max().reset_index()
#print(max_accuracy_df)