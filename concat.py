import pandas as pd
import os
import csv

dir_path = "/isis/home/huynhc1/Paper-Text-Scraper/task"

res = []
for file_path in os.listdir(dir_path):
    # check if current file_path is a file
    if os.path.isfile(os.path.join(dir_path, file_path)) and file_path != "complete.csv":
        # add filename to list
        res.append(file_path)
#print(res)
def concat(f1):
    f1 = "task/"+f1
    df = pd.read_csv(f1, delimiter=",", index_col=False)
    df1 = pd.read_csv("task/task-based.csv",delimiter=",",index_col=False)
    frames = [df, df1]
    result = pd.concat(frames, ignore_index=True)
    result.drop_duplicates()
    print("DF size: " + str(result.shape[0]))
    result.to_csv("task/task-based.csv", index=False, mode='w')


for f in res:
    concat(f)

#df = pd.read_csv("datatables-processed/complete.csv", delimiter=",", index_col=False)

#u1 = df[['Task','Dataset']].value_counts().reset_index(name='count')
"""
df = pd.read_csv("complete2.csv",delimiter=",",index_col=False)
u2 = df[df['Dataset'].isin(['ImageNet'])]
u2 = (u2[['Task', 'Dataset']].value_counts().reset_index(name='count'))
fields = ["Task", "Dataset", 'count']
u2.to_csv("counter.csv", index=False)
"""
#u1 = u1[['Task', 'Dataset']]
#u2 = u2[['Task', 'Dataset']]

#frames = [u1, u2]
#result = pd.concat(frames).drop_duplicates()
#un = set(result[['Task', 'Dataset']]) - set(u2[['Task', 'Dataset']])
#print(un)

