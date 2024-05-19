from vit_pytorch import ViT
from datasets import load_dataset, Image

import glob
from itertools import chain
import os
import random
import zipfile

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

from PIL import Image
from sklearn.model_selection import train_test_split
from torch.optim.lr_scheduler import StepLR
from torch.utils.data import DataLoader, Dataset
from torchvision import datasets, transforms
from tqdm import tqdm

batch_size = 64
epochs = 20
lr = 3e-5
gamma = 0.7
seed = 42

dataset = load_dataset("mnist")

train = dataset['train']
train_image = [x['image'] for x in train]

test = dataset['test']
test_image = [y['image'] for y in test]
test_label = [y['label'] for y in test]

labels = [x['label'] for x in train]

train_data, valid_data, train_label, valid_label = train_test_split(train_image, labels, test_size=0.2, stratify=labels, random_state=seed)

print(f"Train Data: {len(train_data)}")
print(f"Validation Data: {len(valid_data)}")
print(f"Test Data: {len(test_image)}")

transform_image = transforms.Compose([transforms.RandomHorizontalFlip(), transforms.ToTensor()])

class CatsDogsDataset(Dataset):
    def __init__(self, data, labels, transform=None):
        self.data = data
        self.labels = labels
        self.transform = transform

    def __len__(self):
        self.filelength = len(self.data)
        return self.filelength

    def __getitem__(self, idx):
        img = self.data[idx]
        img_transformed = self.transform(img)

        label = int(self.labels[idx])
        return img_transformed, label

train_list = CatsDogsDataset(train_data, train_label, transform=transform_image)
valid_list = CatsDogsDataset(valid_data, valid_label, transform=transform_image)
test_list = CatsDogsDataset(test_image, test_label, transform=transform_image)

train_loader = DataLoader(dataset = train_list, batch_size=batch_size, shuffle=True )
valid_loader = DataLoader(dataset = valid_list, batch_size=batch_size, shuffle=True)
test_loader = DataLoader(dataset = test_list, batch_size=batch_size, shuffle=True)

print(len(train_data), len(train_loader))
print(len(valid_data), len(valid_loader))

v = ViT(
    image_size = 28,
    patch_size = 7,
    num_classes = 10,
    dim = 1024,
    depth = 6,
    heads = 8,
    mlp_dim = 2048,
    dropout = 0.2,
    emb_dropout = 0.1
)


# loss function
criterion = nn.CrossEntropyLoss()
# optimizer
optimizer = optim.Adam(v.parameters(), lr=lr)
# scheduler
scheduler = StepLR(optimizer, step_size=1, gamma=gamma)

for epoch in range(epochs):
    epoch_loss = 0
    epoch_accuracy = 0

    for data, label in tqdm(train_loader):
        output = v(data)
        loss = criterion(output, label)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        acc = (output.argmax(dim=1) == label).float().mean()
        epoch_accuracy += acc / len(train_loader)
        epoch_loss += loss / len(train_loader)

    with torch.no_grad():
        epoch_val_accuracy = 0
        epoch_val_loss = 0
        for data, label in valid_loader:

            val_output = v(data)
            val_loss = criterion(val_output, label)

            acc = (val_output.argmax(dim=1) == label).float().mean()
            epoch_val_accuracy += acc / len(valid_loader)
            epoch_val_loss += val_loss / len(valid_loader)

    print(
        f"Epoch : {epoch+1} - loss : {epoch_loss:.4f} - acc: {epoch_accuracy:.4f} - val_loss : {epoch_val_loss:.4f} - val_acc: {epoch_val_accuracy:.4f}\n"
    )

