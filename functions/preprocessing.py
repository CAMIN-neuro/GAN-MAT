import os
import shutil
import argparse
import numpy as np
import nibabel as nib
from scipy.stats import skew, kurtosis

from brainspace.gradient import GradientMaps
from skimage import transform

parser = argparse.ArgumentParser()
parser.add_argument("--GANMAT")
parser.add_argument("--input_dir")
parser.add_argument("--output_dir")

parser.add_argument("--make_dir", default=False)
parser.add_argument("--make_sub_list", default=False)
parser.add_argument("--resize", default=False)
parser.add_argument("--resize_inv", default=False)
parser.add_argument("--matrix", default=False)
parser.add_argument("--gradients", default=False)
parser.add_argument("--moment", default=False)
args = parser.parse_args()

GANMAT = args.GANMAT
input_dir = args.input_dir
output_dir = args.output_dir

make_dir = args.make_dir
make_sub_list = args.make_sub_list
resize = args.resize
resize_inv = args.resize_inv
matrix = args.matrix
gradients = args.gradients
moment = args.moment

if make_sub_list:
    sub_list = os.listdir(input_dir)
    f = open(output_dir + "/sub_list.txt", 'w')
    for i in range(0, len(sub_list)):
        f.write(sub_list[i] + " ")
    f.close()

f = open(output_dir + "/sub_list.txt", mode='r')
sub_list = f.readlines()[0].split()

if make_dir:
    for i in range(0, len(sub_list)):
        if not os.path.isdir(output_dir + "/{}".format(sub_list[i])):
            os.mkdir(output_dir + "/{}".format(sub_list[i]))

if resize:
    for sub in sub_list:
        img = np.zeros((256, 256, 256, 3))
        temp = np.zeros((227, 272, 227, 3))

        t1 = nib.load(input_dir + "/{}/T1w_MNI.nii.gz".format(sub)).get_fdata()
        pve = nib.load(input_dir + "/{}/T1w_MNI_pveseg.nii.gz".format(sub)).get_fdata()

        for i in range(1, 4):
            x, y, z = np.where(pve == i); temp[x, y, z, i-1] = t1[x, y, z]

        img[14:-15, : ,14:-15, :] = temp[:, 8:-8, :, :]
        np.save(input_dir + '/{}/T1w_MNI_pveseg.npy'.format(sub), img)

if resize_inv:
    for sub in sub_list:
        MNI_header = nib.load(GANMAT+ "/template/MNI152_T1_0.8mm_brain.nii.gz").header
        img = np.zeros((227, 272, 227))

        t2 = np.load(input_dir + '/{}/output_T2w.npy'.format(sub))
        t2 = (t2 - t2.min()) / (t2.max() - t2.min())

        img[:, 8:-8, :] = t2[14:-15, :, 14:-15]
        nifti_img = nib.Nifti1Image(img, affine=None, header=MNI_header)

        nib.save(nifti_img, input_dir + '/{}/output_MNI.nii.gz'.format(sub))

if matrix:
    f = open(GANMAT + "/parcellations/atlas_list.txt", 'r')
    atlas_ls = f.read()
    atlas_ls = atlas_ls.split("\n")[:-1]
    
    for sub in sub_list:
        for atlas in atlas_ls:
            atlas = atlas.split('.')[0].split("_")[0]
            
            temp = np.loadtxt(input_dir + "/{}/T1w/{}/anat/surfaces/micro_profiles/{}_space-fsaverage5_atlas-{}_desc-MPC.txt".format(sub, sub, sub, atlas), dtype=np.float64, delimiter=' ')
            MPC = np.triu(temp, 1) + temp.T
            
            if atlas == "aparc-a2009s":
                idx = [41, 116]
            else:
                idx = [0, int(len(MPC) / 2)]
            
            MPC = np.delete(np.delete(MPC, idx, axis=0), idx, axis=1)

            np.savetxt(input_dir + "/{}/T1w/{}/anat/surfaces/micro_profiles/{}_MPC_matrix.txt".format(sub, sub, atlas), MPC)
            shutil.copy(input_dir + "/{}/T1w/{}/anat/surfaces/micro_profiles/{}_MPC_matrix.txt".format(sub, sub, atlas), output_dir + "/{}/{}_MPC_matrix.txt".format(sub, atlas))

        print("Make sub-{} matrix".format(sub))

if gradients:
    f = open(GANMAT + "/parcellations/atlas_list.txt", 'r')
    atlas_ls = f.read()
    atlas_ls = atlas_ls.split("\n")[:-1]

    for sub in sub_list:
        for atlas in atlas_ls:
            atlas = atlas.split('.')[0].split("_")[0]
            
            ## load MPC matrix
            temp = np.loadtxt(input_dir + "/{}/T1w/{}/anat/surfaces/micro_profiles/{}_MPC_matrix.txt".format(sub, sub, atlas), dtype=np.float64, delimiter=' ')
            
            ## delete all 0 rows
            del_ls = np.where(temp.sum(0)==0)[0]
            temp = np.delete(np.delete(temp, del_ls, axis=0), del_ls, axis=1)

            ## make gradients
            grad_map = GradientMaps(n_components=10, random_state=None, approach='dm', kernel='normalized_angle')
            grad_map.fit(temp, sparsity=0.9)

            ## insert 0 in delete position
            grads = grad_map.gradients_.copy()
            for idx in del_ls:
               grads = np.insert(grads, idx, 0, axis=0)
            
            ## save gradients
            np.savetxt(input_dir + "/{}/T1w/{}/anat/surfaces/micro_profiles/{}_MPC_gradients.txt".format(sub, sub, atlas), grads)
            shutil.copy(input_dir + "/{}/T1w/{}/anat/surfaces/micro_profiles/{}_MPC_gradients.txt".format(sub, sub, atlas), output_dir + "/{}/{}_MPC_gradients.txt".format(sub, atlas))

        print("Make sub-{} gradients".format(sub))
            
if moment:
    f = open(GANMAT + "/parcellations/atlas_list.txt", 'r')
    atlas_ls = f.read()
    atlas_ls = atlas_ls.split("\n")[:-1]

    for sub in sub_list:
        for atlas in atlas_ls:
            atlas = atlas.split('.')[0].split("_")[0]
            
            # load intensity
            temp = np.loadtxt(input_dir + "/{}/T1w/{}/anat/surfaces/micro_profiles/{}_space-fsaverage5_atlas-{}_desc-intensity_profiles.txt".format(sub, sub, sub, atlas), dtype=np.float64, delimiter=' ')

            # delete nan
            nan_ls = np.unique(np.where(np.isnan(temp))[1])
            inten = np.delete(temp, nan_ls, axis=1)

            # momnet
            mean = inten.mean(0)
            std = inten.std(0)
            skew_ = skew(inten)
            kurto_ = kurtosis(inten)

            moment = np.vstack((mean, std, skew_, kurto_))

            # save momnet
            np.savetxt(input_dir + "/{}/T1w/{}/anat/surfaces/micro_profiles/{}_moment.txt".format(sub, sub, atlas), moment)
            shutil.copy(input_dir + "/{}/T1w/{}/anat/surfaces/micro_profiles/{}_moment.txt".format(sub, sub, atlas), output_dir + "/{}/{}_MPC_moment.txt".format(sub, atlas))
            
        print("Make sub-{} moment".format(sub))


