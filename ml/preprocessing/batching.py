import torch
from torch.utils.data import Dataset, DataLoader
import numpy as np

class GraphQLDataset(Dataset):
    def __init__(self, features, labels=None):
        self.features = torch.FloatTensor(features)
        self.labels = torch.LongTensor(labels) if labels is not None else None

    def __len__(self):
        return len(self.features)

    def __getitem__(self, idx):
        if self.labels is not None:
            return self.features[idx], self.labels[idx]
        return self.features[idx]

def create_dataloader(features, labels=None, batch_size=32, shuffle=True):
    dataset = GraphQLDataset(features, labels)
    return DataLoader(dataset, batch_size=batch_size, shuffle=shuffle)
