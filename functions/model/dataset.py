import os
import torch
import numpy as np
import nibabel as nib

class Dataset(torch.utils.data.Dataset):
    def __init__(self, input_dir, output_dir, transform=None, opts=None):
        self.input_dir = input_dir
        self.to_tensor = ToTensor()
        self.output_dir = output_dir

        with open(self.output_dir + "/sub_list.txt", 'r') as file:
            sub_ls = file.read().split()
        self.lst_sub = np.array(sub_ls)

    def __len__(self):
        return len(self.lst_sub)

    def __getitem__(self, index):
        input = np.load(self.input_dir + "/" + self.lst_sub[index] + "/T1w_MNI_pveseg.npy")

        # normalization each pve
        for i in range(input.shape[-1]):
            input[:, :, :, i] = (input[:, :, :, i] - input[:, :, :, i].mean()) / input[:, :, :, i].std()

        data = {'input': input}
        data = self.to_tensor(data)

        return data


class ToTensor(object):
    def __call__(self, data):
        for key, value in data.items():
            value = value.transpose((3, 0, 1, 2)).astype(np.float32)
            data[key] = torch.from_numpy(value)

        return data



