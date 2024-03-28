import pandas as pd

df = pd.read_csv("mergedtable.csv",delimiter='|')


##This file takes in 2 tables that has an ID column and combine them, as well as
##make the tables cleaner looking and more consistent
def tag_edit(x):
    if pd.isna(x):
        return 0
    return x

def replace_val(x):
    if pd.isna(x):
        return 0
    return x

## generate a map of values of features existing within which samples
sample = df.tags.str.get_dummies(sep=', ')

sample = sample.drop('\'\'', axis=1)
sample.to_csv("tag_dummies.csv", index=False, encoding='utf-8')