import pandas as pd

"""
df = pd.read_csv("datatables-processed/complete.csv", delimiter=",", index_col=False)
df1 = pd.read_csv("datatables-processed/cifar10-generation-processed.csv",delimiter=",", index_col=False)
df2 = pd.read_csv("datatables-processed/imagenet-256-generation-processed.csv", delimiter=",", index_col=False)

frames = [df, df1, df2]
result = pd.concat(frames, ignore_index=True)
result.to_csv("complete.csv", index=False)

#cols = ['Task', 'Dataset', 'name', 'accuracy', 'accuracy_norm', 'params', 'tags', 'id']
#df = df[cols]

def process(df, dataset, task):
    df["Dataset"] = dataset
    df["Task"] = task

    df.loc[df["tags"] == "[']']", "tags"] = "[]"
    df.loc[df["tags"] == "[']}]</script']", "tags"] = "[]"
    df = df[df['accuracy'].notna()]
    df = df[df['id'].notna()]

    df["accuracy"] = df["accuracy"].str[:-1]
    df["accuracy"] = df["accuracy"].astype(float)
    df["accuracy_norm"] = (df["accuracy"] - df["accuracy"].min()) / (df["accuracy"].max() - df["accuracy"].min())

    cols = ['Task', 'Dataset', 'name', 'accuracy', 'accuracy_norm', 'params', 'tags', 'id']
    df = df[cols]
    return df

#cur = process(df, "ImageNet 256x256", "Image Generation")
#cur.to_csv("imagenet-256-generation-processed.csv", index=False)
"""
df = pd.read_csv("complete.csv", index_col= False)

idx = df.groupby(['Dataset', 'Task'])['accuracy'].idxmax()
max_scores = df.loc[idx]
max_scores.to_csv("normalized-task-data.csv", index=False)