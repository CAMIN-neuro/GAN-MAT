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
parser.add_argument("--myelin_brain", default=False)
parser.add_argument("--matrix", default=False)
parser.add_argument("--save_matrix", default=False)
parser.add_argument("--gradients", default=False)
parser.add_argument("--save_gradients", default=False)
parser.add_argument("--moment", default=False)
parser.add_argument("--moment_save", default=False)
args = parser.parse_args()

GANMAT = args.GANMAT
input_dir = args.input_dir
output_dir = args.output_dir

make_dir = args.make_dir
make_sub_list = args.make_sub_list
resize = args.resize
myelin_brain = args.myelin_brain
matrix = args.matrix
save_matrix = args.save_matrix
gradients = args.gradients
save_gradients = args.save_gradients
moment = args.moment
moment_save = args.moment_save

sub_list = os.listdir(input_dir)

if make_sub_list:
    f = open(output_dir + "/sub_list.txt", 'w')
    for i in range(0, len(sub_list)):
        f.write(sub_list[i] + " ")
    f.close()

if make_dir:
    for i in range(0, len(sub_list)):
        if not os.path.isdir(output_dir + "/{}".format(sub_list[i])):
            os.mkdir(output_dir + "/{}".format(sub_list[i]))

if resize:
    for sub in sub_list:
        t1 = nib.load(input_dir + '/{}/T1w_regi.nii.gz'.format(sub)).get_fdata()
        t1 = t1[2:-2, 11:304, :-4]
        t1 = transform.resize(t1, (256, 256, 256))
        t1 = t1 / t1.max()

        nib.save(nib.Nifti1Image(t1, None), input_dir + '/{}/input_T1w.nii.gz'.format(sub))    

if myelin_brain:
    for sub in sub_list:
        myelin = nib.load(input_dir + "/{}/myelin.nii.gz".format(sub)).get_fdata()    
        mask = nib.load(input_dir + "/{}/input_T1w_brain_mask.nii.gz".format(sub)).get_fdata()  
    
        myelin = np.array(myelin).reshape(-1)
        mask = np.array(mask).reshape(-1)    
    
        myelin[np.where(mask==0)] = 0
        myelin = myelin.reshape(256, 256, 256)

        nib.save(nib.Nifti1Image(myelin, None), input_dir + "/{}/myelin_brain.nii.gz".format(sub))

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

        print("Make sub-{} matrix".format(sub))

if save_matrix:
    f = open(GANMAT + "/parcellations/atlas_list.txt", 'r')
    atlas_ls = f.read()
    atlas_ls = atlas_ls.split("\n")[:-1]
    
    for sub in sub_list:
        for atlas in atlas_ls:
            atlas = atlas.split('.')[0].split("_")[0]

            shutil.copy(input_dir + "/{}/T1w/{}/anat/surfaces/micro_profiles/{}_MPC_matrix.txt".format(sub, sub, atlas), output_dir + "/{}/{}_MPC_matrix.txt".format(sub, atlas))

        print("Save sub-{} matrix".format(sub))


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

        print("Make sub-{} gradients".format(sub))

if save_gradients:
    f = open(GANMAT + "/parcellations/atlas_list.txt", 'r')
    atlas_ls = f.read()
    atlas_ls = atlas_ls.split("\n")[:-1]

    for sub in sub_list:
        for atlas in atlas_ls:
            atlas = atlas.split('.')[0].split("_")[0]

            shutil.copy(input_dir + "/{}/T1w/{}/anat/surfaces/micro_profiles/{}_MPC_gradients.txt".format(sub, sub, atlas), output_dir + "/{}/{}_MPC_gradients.txt".format(sub, atlas))
            
        print("Save sub-{} gradients".format(sub))
            
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
            
        print("Make sub-{} moment".format(sub))

if moment_save:
    f = open(GANMAT + "/parcellations/atlas_list.txt", 'r')
    atlas_ls = f.read()
    atlas_ls = atlas_ls.split("\n")[:-1]

    for sub in sub_list:
        for atlas in atlas_ls:
            atlas = atlas.split('.')[0].split("_")[0]

            shutil.copy(input_dir + "/{}/T1w/{}/anat/surfaces/micro_profiles/{}_moment.txt".format(sub, sub, atlas), output_dir + "/{}/{}_MPC_moment.txt".format(sub, atlas))
            
        print("Save sub-{} moment".format(sub))
