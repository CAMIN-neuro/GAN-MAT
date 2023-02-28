#!/bin/bash

pipeline_dir=$1
input_dir=$2
output_dir=$3
threads=$4
sub_list=$(<$output_dir/sub_list.txt)

for sub in "$input_dir"/*
do
	# making myelin image
	wb_command -volume-math "clamp((T1w / T2w), 0, 100)" $sub/myelin.nii.gz -var T1w $sub/input_T1w.nii.gz -var T2w $sub/output_T2w.nii.gz -fixnan 0

	# making input T1 brain_mask
	$FSL_DIR/bin/bet $sub/input_T1w.nii.gz $sub/input_T1w_brain.nii.gz -f 0.5 -g 0 -n -m

	# making original T1w_brain
	$FSL_DIR/bin/bet $sub/T1w/T1w.nii.gz $sub/T1w/T1w_brain.nii.gz -f 0.5 -g 0

done

# making myelin_brain image
python $pipeline_dir/functions/preprocessing.py --GANMAT=$pipeline_dir --input_dir=$input_dir --output_dir=$output_dir --myelin_brain=True

# myelin_brain registrate to original T1w_brain
{
	parallel -j $threads $FSL_DIR/bin/flirt -in $input_dir/{}/myelin_brain.nii.gz -ref $input_dir/{}/T1w/T1w_brain.nii.gz -out $input_dir/{}/T1w/myelin_brain_regi.nii.gz ::: $sub_list
} || {
	for sub in $sub_list
	do
        	$FSL_DIR/bin/flirt -in $input_dir/$sub/myelin_brain.nii.gz -ref $input_dir/$sub/T1w/T1w_brain.nii.gz -out $input_dir/$sub/T1w/myelin_brain_regi.nii.gz
	done
}

