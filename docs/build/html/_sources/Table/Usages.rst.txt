------
Usages
------

Structure of our program
========================

.. code-block::

   GAN-MAT
   ├── functions
   │   └── model
   ├── parcellations
   ├── template
   ├── gan-mat
   └── folder_setting.ipynb

- **functions**: a folder containing files for processing data, especially *model* floder related to synthesizing T2-weighted MRI.
- **parcellations**: a floder containing *.annot* files of each atlas
- **template**: a floder containing MRI image for registration.
- **gan-mat**: main shell script to run program
- **folder_setting.ipynb**: a file that converts input data to specific format

Command
=======

1. Using *folder_setting.ipynb* file, transform input data to specific format. 
2. run *gan-mat*.

.. code-block::

   gan-mat -input_dir "your input data folder path" -output_dir "your output data folder path" <options>

================ ================================================================
**Options**      **Description**
---------------- ----------------------------------------------------------------
batch_size <num> Synthesizing T2-weight MRI, Number of batch size (default is 1).
---------------- ----------------------------------------------------------------
threads <num>    default is 6
---------------- ----------------------------------------------------------------
T2               run to making T2-weight MRI and terminate the program.
---------------- ----------------------------------------------------------------
myelin           run to making T1/T2 ratio and terminate the program.
---------------- ----------------------------------------------------------------
matrix           run to making MPC matrix and terminate the program.
---------------- ----------------------------------------------------------------
gradients        run to making MPC matrix and terminate the program.
================ ================================================================

.. warning::
   When batch size is 1, in out experiments, it required approximately as much GPU memory as 10GB. So if you have GPU but the capacity is not enough, device variable in *functions/model/t2.py* changes to cpu

3. The Results are stored in each subject folders of output_dir path.








