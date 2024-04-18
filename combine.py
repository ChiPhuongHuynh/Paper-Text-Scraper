import pandas as pd

df0 = pd.read_csv("complete.csv", delimiter=",", index_col=False)
"""
df = pd.read_csv("datatables-processed/kitti-monocular-depth-estimation.csv", delimiter=",", index_col=False)
df1 = pd.read_csv("datatables-processed/ade20k-semantic-segmentation.csv",delimiter=",", index_col=False)
df2 = pd.read_csv("datatables-processed/cityscape-semantic-segmentation.csv", delimiter=",", index_col=False)
df3 = pd.read_csv("datatables-processed/coco-text2image.csv", delimiter=",", index_col=False)
df4 = pd.read_csv("datatables-processed/nyu-depthv2-semantic-segmentation.csv", delimiter=",", index_col=False)
df5 = pd.read_csv("datatables-processed/shapenet-3d-part-segmentation.csv", delimiter=",", index_col=False)
frames = [df0,df, df1, df2, df3, df4, df5]
result = pd.concat(frames, ignore_index=True)
print(result)
result.to_csv("complete.csv", index=False)
"""
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
"""
cur = process(df, "COCO", "Text to Image", False)
print(cur)
cur.to_csv("datatables-processed/coco-text2image.csv", index = False)

df = pd.read_csv("normalized-task-data.csv", index_col= False)
df["accuracy"] = df["accuracy"].astype(float)
df["accuracy_norm"] = (df["accuracy"] - df["accuracy"].min()) / (df["accuracy"].max() - df["accuracy"].min())
print(df)
df.to_csv("normalized-task-data.csv", index=False)
"""

sample = df0.loc[df0.groupby(['Task', 'Dataset'])['accuracy_norm'].idxmax()]
print(sample)

maxima = sample.groupby(['Task'])['accuracy'].max()
sample['max'] = sample['Task'].map(maxima)
minima = sample.groupby(['Task'])['accuracy'].min()
sample['min'] = sample['Task'].map(minima)
sample.loc[sample['accuracy'] == sample['max'], 'difficulty'] = 1
sample.loc[sample['accuracy'] == sample['min'], 'difficulty'] = 0
sample.loc[(sample['accuracy'] != sample['max']) & (sample['accuracy'] != sample['min']), 'difficulty'] = (sample['accuracy'] - sample['min']) / (sample['max'] - sample['min'])

sample.to_csv("normalized-task-data.csv", index=False)