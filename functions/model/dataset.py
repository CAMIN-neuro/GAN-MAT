import os
import torch
import numpy as np
import nibabel as nib

class Dataset(torch.utils.data.Dataset):
    def __init__(self, input_dir, transform=None, opts=None):
        self.input_dir = input_dir
        self.transform = transform
        self.opts = opts
        self.to_tensor = ToTensor()

        lst_sub = os.listdir(self.input_dir)
        lst_sub.sort()

        self.lst_sub = lst_sub

    def __len__(self):
        return len(self.lst_sub)

    def __getitem__(self, index):
        input = np.array(nib.load(self.input_dir + "/" + self.lst_sub[index] + "/input_T1w.nii.gz").get_fdata())

        if input.ndim == 3:
            input = input[:, :, :, np.newaxis]

        data = {'input': input}

        if self.transform:
            data = self.transform(data)

        data = self.to_tensor(data)

        return data


class ToTensor(object):
    def __call__(self, data):
        for key, value in data.items():
            value = value.transpose((3, 0, 1, 2)).astype(np.float32)
            data[key] = torch.from_numpy(value)

        return data


class Normalization(object):
    def __init__(self, mean=0.5, std=0.5):
        self.mean = mean
        self.std = std

    def __call__(self, data):
        for key, value in data.items():
            data[key] = (value - self.mean) / self.std

        return data
