import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("normalized-task-data.csv", delimiter=',', index_col=False)

colors = []
legends ={}


for task, dataset in zip(df['Task'], df['Dataset']):
    if task == 'Image Classification' and dataset == "CIFAR-10":
        colors.append("blue")
        legends['blue'] = {"Classification on CIFAR-10"}
    elif task == 'Image Classification' and dataset == "CIFAR-100":
        colors.append("yellow")
        legends['yellow'] = {"Classification on CIFAR-100"}
    elif task == 'Image Classification' and dataset == "ImageNet":
        colors.append("red")
        legends['red'] = {"Classification on ImageNet"}
    elif task == 'Image Classification' and dataset == "MNIST":
        colors.append("green")
        legends['green'] = {"Classification on MNIST"}
    elif task == 'Image Classification' and dataset == "SVHN":
        colors.append("orange")
        legends['orange'] = {"Classification on SVHN"}
    elif task == 'Image Generation' and dataset == "ImageNet 256x256":
        colors.append("pink")
        legends['pink'] = {"Generation on ImageNet 256"}
    elif task == 'Object Detection' and dataset == "COCO minivar":
        colors.append("grey")
        legends['grey'] = {"Detection on COCO minivar"}

sns.scatterplot(x='accuracy_norm', y='accuracy', data=df, hue=colors,
                 palette={'blue': 'blue', 'yellow': 'yellow', 'green': 'green','orange':'orange','red':'red', 'pink':'pink','grey':'grey'})



plt.legend(title='Legend', labels=legends.values(), bbox_to_anchor=(1, 1), loc='upper left')
plt.tight_layout()
plt.show()