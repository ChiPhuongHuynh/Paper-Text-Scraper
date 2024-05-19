import pandas as pd

df0 = pd.read_csv("datatables-processed/complete.csv", delimiter=",", index_col=False)

#cols = ['Task', 'Dataset', 'name', 'accuracy', 'accuracy_norm', 'params', 'tags', 'id']
#df = df[cols]
#df = pd.read_csv("datatables-unprocessed/coco-text2image.csv", delimiter="|", index_col=False)
def process(df, dataset, task, max = True):
    df["Dataset"] = dataset
    df["Task"] = task

    df.loc[df["tags"] == "[']']", "tags"] = "[]"
    df.loc[df["tags"] == "[']}]</script']", "tags"] = "[]"
    df = df[df['accuracy'].notna()]
    df = df[df['id'].notna()]

    #if df["accuracy"].dtypes != "std":
    #df["accuracy"] = df["accuracy"].str.replace("%", "")
    df["accuracy"] = df["accuracy"].astype(float)
    if max:
        df["accuracy_norm"] = (df["accuracy"] - df["accuracy"].min()) / (df["accuracy"].max() - df["accuracy"].min())
    else: df["accuracy_norm"] = (df["accuracy"].max() - df["accuracy"]) / (df["accuracy"].max() - df["accuracy"].min())

    cols = ['Task', 'Dataset', 'name', 'accuracy', 'accuracy_norm', 'params', 'tags', 'id']
    df = df[cols]
    return df

#cur = process(df, "CIFAR-10", "Image Generation", False)
#print(cur)
#cur.to_csv("datatables-processed/cifar10-generation-processed.csv", index = False)

"""
df = pd.read_csv("normalized-task-data.csv", index_col= False)
df["accuracy"] = df["accuracy"].astype(float)
df["accuracy_norm"] = (df["accuracy"] - df["accuracy"].min()) / (df["accuracy"].max() - df["accuracy"].min())
print(df)
df.to_csv("normalized-task-data.csv", index=False)

df0 = df0.replace("Text-to-Image", "Text to Image")
df0.to_csv("datatables-processed/complete.csv", index=False)
sample = df0.loc[df0.groupby(['Task', 'Dataset'])['accuracy_norm'].idxmax()]
#print(sample)

maxima = sample.groupby(['Task'])['accuracy'].max()
sample['max'] = sample['Task'].map(maxima)
minima = sample.groupby(['Task'])['accuracy'].min()
sample['min'] = sample['Task'].map(minima)
sample.loc[sample['accuracy'] == sample['max'], 'difficulty'] = 1
sample.loc[sample['accuracy'] == sample['min'], 'difficulty'] = 0
sample.loc[(sample['accuracy'] != sample['max']) & (sample['accuracy'] != sample['min']), 'difficulty'] = (sample['accuracy'] - sample['min']) / (sample['max'] - sample['min'])

sample.to_csv("normalized-task-data.csv", index=False)
"""

print(df0.count())
