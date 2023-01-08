#!/bin/bash

idBIDS=$1 
subject_dir=$2 
parc_annot=$3

SUBJECTS_DIR="${subject_dir}/${idBIDS}/T1w"
dir_freesurfer="${subject_dir}/${idBIDS}/T1w/${idBIDS}"

outDir="${dir_freesurfer}/anat/surfaces/micro_profiles"

num_surfs=14
tmp="/tmp/${RANDOM}_micapipe_post-MPC_${idBIDS}"
mkdir -p "$tmp"

### Create MPC connectomes and Intensity profiles per parcellations
out=$outDir
SES="SINGLE"
id=$idBIDS

python $GANMAT/functions/surf2mpc.py "$out" "$id" "$SES" "$num_surfs" "$parc_annot" "$dir_freesurfer" "$GANMAT"

