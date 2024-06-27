import pandas as pd
import csv

df = pd.read_csv("normalized-task-data2.csv", index_col=False)

sample = df[df["Dataset"].isin(['ImageNet', 'CIFAR-10','CIFAR-100','MNIST', 'SVHN', 'Fashion MNIST', 'STL-10', 'KMNIST'])]

sample.to_csv("counter.csv")