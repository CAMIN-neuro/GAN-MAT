#!/bin/bash

pipeline_dir=$1
threads=$2
sub_list=$(<$pipeline_dir/results/sub_list.txt)

parallel -j $threads $FSL_DIR/bin/flirt -in $pipeline_dir/results/{}/T1w/T1w.nii.gz -ref $pipeline_dir/template/MNI152_T1_0.7mm.nii.gz -out $pipeline_dir/results/{}/T1w_regi.nii.gz ::: $sub_list


