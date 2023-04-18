#!/bin/bash

pipeline_dir=$1
input_dir=$2
output_dir=$3
threads=$4
task=$5
sub_list=$(<$output_dir/sub_list.txt)

if [ $task == bias ]; then
	for sub in "$input_dir"/*
	do
		N4BiasFieldCorrection -d 3 -i $sub/T1w/T1w.nii.gz -o $sub/BF_T1w.nii.gz -r -v
	done
fi

if [ $task == input ]; then
	{
		# making mat file
		parallel -j $threads $FSL_DIR/bin/flirt -in $input_dir/{}/BF_T1w.nii.gz -ref $GANMAT/template/MNI152_T1_0.7mm.nii.gz -out $input_dir/{}/temp.nii.gz -omat $input_dir/{}/nat2tem ::: $sub_list

		# registration using mat file
		parallel -j $threads $FSL_DIR/bin/flirt -in $input_dir/{}/T1w/T1w.nii.gz -ref $GANMAT/template/MNI152_T1_0.7mm.nii.gz -out $input_dir/{}/T1w_regi.nii.gz -applyxfm -init $input_dir/{}/nat2tem ::: $sub_list
	} || {
		for sub in $sub_list
        	do
        		$FSL_DIR/bin/flirt -in $input_dir/$sub/BF_T1w.nii.gz -ref $GANMAT/template/MNI152_T1_0.7mm.nii.gz -out $input_dir/$sub/temp.nii.gz -omat $input_dir/$sub/nat2tem
			$FSL_DIR/bin/flirt -in $input_dir/$sub/T1w/T1w.nii.gz -ref $GANMAT/template/MNI152_T1_0.7mm.nii.gz -out $input_dir/$sub/T1w_regi.nii.gz -applyxfm -init $input_dir/$sub/nat2tem
		done
	}
fi

if [ $task == t2 ]; then
	{
		# making mat file
        	parallel -j $threads $FSL_DIR/bin/flirt -in $input_dir/{}/output_T2w.nii.gz -ref $input_dir/{}/BF_T1w.nii.gz -out $input_dir/{}/temp.nii.gz -omat $input_dir/{}/t22t1 ::: $sub_list

       		# registration using mat file
        	parallel -j $threads $FSL_DIR/bin/flirt -in $input_dir/{}/output_T2w.nii.gz -ref $input_dir/{}/temp.nii.gz -out $output_dir/{}/T2w.nii.gz -applyxfm -init $input_dir/{}/t22t1 ::: $sub_list
	} || {
		for sub in $sub_list
                do
	                $FSL_DIR/bin/flirt -in $input_dir/$sub/output_T2w.nii.gz -ref $input_dir/$sub/BF_T1w.nii.gz -out $input_dir/$sub/temp.nii.gz -omat $input_dir/$sub/t22t1
			$FSL_DIR/bin/flirt -in $input_dir/$sub/output_T2w.nii.gz -ref $input_dir/$sub/temp.nii.gz -out $output_dir/$sub/T2w.nii.gz -applyxfm -init $input_dir/$sub/t22t1
		done
	}
fi

if [ $task == myelin ]; then
	{
		# making mat file
        	parallel -j $threads $FSL_DIR/bin/flirt -in $input_dir/{}/myelin_brain.nii.gz -ref $input_dir/{}/BF_T1w.nii.gz -out $input_dir/{}/temp.nii.gz -omat $input_dir/{}/mye2t1 ::: $sub_list

        	# registration using mat file
        	parallel -j $threads $FSL_DIR/bin/flirt -in $input_dir/{}/myelin_brain.nii.gz -ref $input_dir/{}/temp.nii.gz -out $input_dir/{}/T1w/myelin_brain_regi.nii.gz -applyxfm -init $input_dir/{}/mye2t1 ::: $sub_list
	} || {
		for sub in $sub_list
		do
			$FSL_DIR/bin/flirt -in $input_dir/$sub/myelin_brain.nii.gz -ref $input_dir/$sub/BF_T1w.nii.gz -out $input_dir/$sub/temp.nii.gz -omat $input_dir/$sub/mye2t1
			$FSL_DIR/bin/flirt -in $input_dir/$sub/myelin_brain.nii.gz -ref $input_dir/$sub/temp.nii.gz -out $input_dir/$sub/T1w/myelin_brain_regi.nii.gz -applyxfm -init $input_dir/$sub/mye2t1
		done
	}
	
	for sub in $sub_list
	do 
		rm $input_dir/$sub/temp.nii.gz
		rm $input_dir/$sub/BF_T1w.nii.gz
		rm $input_dir/$sub/mye2t1
		rm $input_dir/$sub/t22t1
		rm $input_dir/$sub/nat2tem
	done
fi


