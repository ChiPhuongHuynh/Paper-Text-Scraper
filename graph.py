import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

"""
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
"""

df = pd.read_csv("task/task-based.csv", index_col=False)

df = df.dropna(subset=['accuracy_norm'])

unique_combinations_count = df[['Task', 'Dataset']].drop_duplicates().count()

# Group by 'Task' and count the number of unique 'Dataset' values in each group
unique_datasets_per_task = df.groupby('Task')['Dataset'].nunique()

# Plotting
plt.figure(figsize=(8, 6))  # Adjust size of the plot if needed
unique_datasets_per_task.plot(kind='barh', color='skyblue')
plt.xlabel('Number of Unique Datasets')
plt.ylabel('Task')
plt.title('Number of Unique Datasets in Each Task Group')
plt.grid(axis='x', linestyle='--', alpha=0.7)  # Add grid lines for better readability
plt.savefig('unique_datasets_per_task.png', bbox_inches='tight')  # Adjust file name and format as needed
plt.close()