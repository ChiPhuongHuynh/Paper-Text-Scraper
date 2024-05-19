import pandas as pd

df = pd.read_csv("datatables-processed/cifar10-generation-processed.csv", delimiter=",", index_col=False)
df1 = pd.read_csv("datatables-processed/complete.csv",delimiter=",",index_col=False)
frames = [df, df1]
result = pd.concat(frames, ignore_index=True)
result.drop_duplicates()
print(result)
result.to_csv("datatables-processed/complete.csv", index=False)