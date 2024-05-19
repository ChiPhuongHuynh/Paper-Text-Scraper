import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("complete.csv", delimiter=',', index_col=False)
sample = df[['Task', 'Dataset','accuracy','accuracy_norm']]

sample.set_index('accuracy', inplace=True)
sample.groupby(['Task', 'Dataset'])['accuracy_norm'].plot(legend=True)
#
plt.title("Performance Normalization accross Tasks and Datasets")
plt.xlabel("Performance")
plt.ylabel("Normalized Performance")

plt.legend(loc='center right', bbox_to_anchor=(1.75, 0.5))

plt.savefig('normalization.png', bbox_inches='tight')
plt.close()
#plt.show()