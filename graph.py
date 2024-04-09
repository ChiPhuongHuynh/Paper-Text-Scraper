import pandas as pd

df = pd.read_csv("combined.csv", delimiter=',', index_col=False)

ax = df.plot.scatter(x='accuracy_norm', y='accuracy')