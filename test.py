from scipy.spatial.distance import euclidean, pdist, squareform
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

data = {'Model': ['ResNet', 'VGG', 'DenseNet', 'EfficientNet', 'MobileNet', 'YOLO', 'ViT', 'Deeplab', 'SENet', 'NASNet', 'DeiT', 'RegNet', 'EfficientPose', 'DETR', 'CrossViT', 'CaiT'],
        'Task': [1, 1, 1, 1, 1, 2, 1, 1, 3, 1, 1, 1, 4, 2, 1, 1],
        'Dataset': [1, 1, 2, 1, 1, 4, 1, 1, 1, 1, 1, 1, 3, 3, 1, 1],
        'Accuracy': [96.43, 75.2, 96.54, 84.3, 70.6, 59.2, 88.55, 79.7, 40.37, 82.7, 83.1, 92.7, 97.35, 52.3, 83.8, 86.5],
        'Architecture': [1, 1, 1, 1, 1, 3, 2, 1, 1, 1, 2, 1, 3, 1, 2, 2]}

df = pd.DataFrame(data)
df = df.set_index("Model")

def similarity_func(u, v):
    return 1/(1+euclidean(u,v))
dists = pdist(df, similarity_func)
similarity_matrix = pd.DataFrame(squareform(dists), columns=df.index, index=df.index)


fig, ax = plt.subplots(figsize=(10,10))
sns.heatmap(similarity_matrix, annot=True, cmap='YlGnBu', linewidths=.5, ax=ax)
plt.show()