import pandas as pd

df0 = pd.read_csv("complete2.csv", delimiter=",", index_col=False)

#cols = ['Task', 'Dataset', 'name', 'accuracy', 'accuracy_norm', 'params', 'tags', 'id']
#df = df[cols]
#df = pd.read_csv("datatables-unprocessed/imagenet-image-classification.csv", delimiter=",", index_col=False)
def process(df, dataset, task, max = True):
    df["Dataset"] = dataset
    df["Task"] = task

    df.loc[df["tags"] == "[']']", "tags"] = "[]"
    df.loc[df["tags"] == "[']}]</script']", "tags"] = "[]"
    df = df[df['accuracy'].notna()]
    df = df[df['id'].notna()]

    if df["accuracy"].dtypes != "std":
        df["accuracy"] = df["accuracy"].apply(str).str[0:5]
        df["accuracy"] = df["accuracy"].apply(str).str.replace("%", "")
        df["accuracy"] = df["accuracy"].apply(str).str.replace("}", "")
    df["accuracy"] = df["accuracy"].astype(float)

    if max:
        df["accuracy_norm"] = (df["accuracy"] - df["accuracy"].min()) / (df["accuracy"].max() - df["accuracy"].min())
    else:
        df["accuracy_norm"] = (df["accuracy"].max() - df["accuracy"]) / (df["accuracy"].max() - df["accuracy"].min())
        df["accuracy"] = 100 - df["accuracy"]


    cols = ['Task', 'Dataset', 'name', 'accuracy', 'accuracy_norm', 'params', 'tags', 'id']
    df = df[cols]
    if df.shape[0] == 1: df['accuracy_norm'][0] = 1.0
    ##df['accuracy'] = 100*df['accuracy']
    return df

#cur = process(df, "ImageNet", "Image Classification", True)
#print(cur.head())
#cur.to_csv("datatables-processed/imagenet_image_classification.csv", index = False)

"""
df = pd.read_csv("normalized-task-data.csv", index_col= False)
df["accuracy"] = df["accuracy"].astype(float)
df["accuracy_norm"] = (df["accuracy"] - df["accuracy"].min()) / (df["accuracy"].max() - df["accuracy"].min())
print(df)
df.to_csv("normalized-task-data.csv", index=False)
"""
#idx = list(df0.groupby(['Task','Dataset'])['accuracy_norm'].idxmax(skipna=True))
sample_idx = df0.groupby(['Task', 'Dataset'])['accuracy_norm'].idxmax()
sample = df0.loc[sample_idx]

maxima = sample.groupby(['Task'])['accuracy'].max()
sample['max'] = sample['Task'].map(maxima)
minima = sample.groupby(['Task'])['accuracy'].min()
sample['min'] = sample['Task'].map(minima)
sample.loc[sample['accuracy'] == sample['max'], 'difficulty'] = 1
sample.loc[sample['accuracy'] == sample['min'], 'difficulty'] = 0
sample.loc[(sample['accuracy'] != sample['max']) & (sample['accuracy'] != sample['min']), 'difficulty'] = (sample['accuracy'] - sample['min']) / (sample['max'] - sample['min'])

print(sample)
sample.to_csv("normalized-task-data2.csv", index=False)



#print(df0.count())
