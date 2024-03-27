import pandas as pd

df = pd.read_csv("mergedtable.csv",delimiter='|')

def tag_edit(x):
    if pd.isna(x):
        return 0
    return x

def replace_val(x):
    if pd.isna(x):
        return 0
    return x
sample = df.tags.str.get_dummies(sep=', ')
sample = sample.drop('\'\'', axis=1)
sample.to_csv("tag_dummies.csv", index=False, encoding='utf-8')

"""
df2 = pd.read_csv("table1.csv", delimiter = "|")
df1 = df2.rename(columns = {'name':'name', 'year':'year', 'accuracy':'accuracy', 'paper':'id'})
#print(df1)
df1 = df1.drop(['accuracy', 'name'], axis =1)
df_m = pd.merge(df, df1, on='id').drop_duplicates()
df_m.insert(0, "Task", "Image Classification", True)
df_m.to_csv("mergedtable.csv", sep='|', index=False, encoding='utf-8')
"""