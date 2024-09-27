#!/bin/bash

pipeline_dir=$1
input_dir=$2
output_dir=$3
threads=$4
task=$5
sub_list=$(<$output_dir/sub_list.txt)

if [ $task == fs ]; then
	if command -v parallel > /dev/null 2>&1; then
		# raw data
		parallel -j $threads mri_convert $input_dir/{}/T1w/{}/mri/orig.mgz $input_dir/{}/raw.nii.gz ::: $sub_list

		# deoblique 
		parallel -j $threads 3dresample -orient LPI -prefix $input_dir/{}/T1w_fsnative.nii.gz -inset $input_dir/{}/raw.nii.gz ::: $sub_list

		# Reorient to standard
		parallel -j $threads fslreorient2std $input_dir/{}/T1w_fsnative.nii.gz $input_dir/{}/T1w_fsnative.nii.gz ::: $sub_list

		# bias-field correction & brain extraction
		for sub in $sub_list
		do
			N4BiasFieldCorrection -d 3 -i $input_dir/$sub/T1w_fsnative.nii.gz -r -o $input_dir/$sub/T1w_fsnative.nii.gz -v
			mri_synthstrip -i $input_dir/$sub/T1w_fsnative.nii.gz -o $input_dir/$sub/T1w_fsnative_brain.nii.gz
			rm -rf $input_dir/$sub/raw.nii.gz
			rm -rf $input_dir/$sub/T1w_fsnative.nii.gz
		done
	else
		for sub in $sub_list
		do
			mri_convert $input_dir/$sub/T1w/$sub/mri/orig.mgz $input_dir/$sub/raw.nii.gz
			3dresample -orient LPI -prefix $input_dir/$sub/T1w_fsnative.nii.gz -inset $input_dir/$sub/raw.nii.gz
			fslreorient2std $input_dir/$sub/T1w_fsnative.nii.gz $input_dir/$sub/T1w_fsnative.nii.gz
			N4BiasFieldCorrection -d 3 -i $input_dir/$sub/T1w_fsnative.nii.gz -r -o $input_dir/$sub/T1w_fsnative.nii.gz -v
			mri_synthstrip -i $input_dir/$sub/T1w_fsnative.nii.gz -o $input_dir/$sub/T1w_fsnative_brain.nii.gz
                        rm -rf $input_dir/$sub/raw.nii.gz			
			rm -rf $input_dir/$sub/T1w_fsnative.nii.gz
		done
	fi
fi
	
if [ $task == t1 ]; then
	echo "Registration native T1w to MNI ..."
	echo " "
	for sub in $sub_list
	do	
		antsRegistrationSyN.sh -d 3 -f $input_dir/$sub/T1w_fsnative_brain.nii.gz -m $GANMAT/template/MNI152_T1_0.8mm_brain.nii.gz -o $input_dir/$sub/from-template_to-native -t a -n $threads -p d
                antsApplyTransforms -d 3 -i $input_dir/$sub/T1w_fsnative_brain.nii.gz -r $GANMAT/template/MNI152_T1_0.8mm_brain.nii.gz -t [$input_dir/$sub/from-template_to-native0GenericAffine.mat ,1] -o $input_dir/$sub/T1w_MNI.nii.gz -v 
	done

	# brain_segmentation
	echo "tissue segmentation using FSL FAST"

	if command -v parallel > /dev/null 2>&1; then
		parallel -j $threads $FSL_DIR/bin/fast -N $input_dir/{}/T1w_MNI.nii.gz ::: $sub_list
	else
		for sub in $sub_list
        	do
			$FSL_DIR/bin/fast -N $input_dir/$sub/T1w_MNI.nii.gz
		done
	fi

	for sub in $sub_list
	do
		rm -rf rm -rf $input_dir/$sub/from-template_to-nativeInverseWarped.nii.gz
		rm -rf rm -rf $input_dir/$sub/from-template_to-nativeWarped.nii.gz
		rm -rf rm -rf $input_dir/$sub/T1w_MNI_mixeltype.nii.gz
		rm -rf rm -rf $input_dir/$sub/T1w_MNI_pve_0.nii.gz
		rm -rf rm -rf $input_dir/$sub/T1w_MNI_pve_1.nii.gz
		rm -rf rm -rf $input_dir/$sub/T1w_MNI_pve_2.nii.gz
		rm -rf rm -rf $input_dir/$sub/T1w_MNI_seg.nii.gz
	done
fi

if [ $task == t2 ]; then
	echo "Registration output T2w to native ..."
	echo " "
	
	for sub in $sub_list
	do	
		antsApplyTransforms -d 3 -i $input_dir/$sub/output_MNI.nii.gz -r $input_dir/$sub/T1w_fsnative_brain.nii.gz -t $input_dir/$sub/from-template_to-native0GenericAffine.mat -o $input_dir/$sub/T2w_fsnative_brain.nii.gz -v

		antsApplyTransforms -d 3 -i $input_dir/$sub/output_MNI.nii.gz -r $input_dir/$sub/T1w_fsnative_brain.nii.gz -t $input_dir/$sub/from-template_to-native0GenericAffine.mat -o $output_dir/$sub/T2w_fsnative_brain.nii.gz -v
	done
fi

if [ $task == myelin ]; then
	for sub in $sub_list
	do
		# intensity min-max for T1w
	        max_val=$(fslstats $input_dir/$sub/T1w_fsnative_brain.nii.gz -R | awk '{print $2}')
        	min_val=$(fslstats $input_dir/$sub/T1w_fsnative_brain.nii.gz -R | awk '{print $1}')
	        fslmaths $input_dir/$sub/T1w_fsnative_brain.nii.gz -sub $min_val -div $(bc <<< "$max_val - $min_val") $input_dir/$sub/T1w/T1w_nor.nii.gz

		# intensity min-max for T2w
	        max_val=$(fslstats $input_dir/$sub/T2w_fsnative_brain.nii.gz -R | awk '{print $2}')
        	min_val=$(fslstats $input_dir/$sub/T2w_fsnative_brain.nii.gz -R | awk '{print $1}')
	        fslmaths $input_dir/$sub/T2w_fsnative_brain.nii.gz -sub $min_val -div $(bc <<< "$max_val - $min_val") $input_dir/$sub/T1w/T2w_nor.nii.gz

		# calculate T1w/T2w ratio
		wb_command -volume-math "clamp((T1w / T2w), 0, 100)" $input_dir/$sub/T1w/myelin.nii.gz -var T1w $input_dir/$sub/T1w/T1w_nor.nii.gz -var T2w $input_dir/$sub/T1w/T2w_nor.nii.gz -fixnan 0

		# copy output directory
		cp -v $input_dir/$sub/T1w/myelin.nii.gz $output_dir/$sub/myelin.nii.gz
	done
fi

if [ $task == MPC ]; then
	if command -v parallel > /dev/null 2>&1; then
		parallel -j $threads $GANMAT/functions/MPC.sh {} $input_dir ::: $sub_list
	else
		for sub in $sub_list
		do
		        source $GANMAT/functions/MPC.sh $sub $input_dir
		done
	fi
fi
