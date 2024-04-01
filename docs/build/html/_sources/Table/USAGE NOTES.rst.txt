-----------
USAGE NOTES
-----------

.. note::
   - We recommand to run freesurfer first, becuase all files we need are freesurfer output files.

GAN-MAT structure 
========================

.. code-block::

   GAN-MAT
   ├── docs
   ├── functions
   │   └── model
   ├── parcellations
   ├── template
   ├── folder_setting.ipynb
   ├── gan-mat
   └── README.md

- **functions**: : A folder containing (i) the GAN model (functions/model) to synthesize the T2-weighted MRI from the T1-weighted MRI, and (ii) necessary scripts to calculate myelin-sensitive proxy (T1w/T2w ratio) and (iii) to generate microstructural profile covariance (MPC) matrix, microstructural gradients, and moment features.
- **parcellations**: A folder containing 18 different atlases: aparc, aparc-a2009s, economo, glasser-360, schaefer-100~1000, vosdewael-100~400.
- **template**: A folder containing the MNI 0.8mm T1 template for initial registration. 
- **folder_setting.ipynb**: A file converting input data to an appropriate format to run the pipeline.
- **gan-mat**: A main script to run GAN-MAT.

Run GAN-MAT
===========

**1. Set up the directory with a specific format  using** *folder_setting.ipynb* **as follows:**

.. code-block::

   input_dir
   ├── 105923                                        # Subject ID
   │   └── T1w
   │       └─── 105923                               # Subject ID
   │           ├── anat
   │           │   └── surfaces
   │           │       └── micro_profiles
   │           ├── label                             # freesurfer output
   │           │   ├── lh.cortex.label
   │           │   └── rh.cortex.label
   │           ├── mri                               # freesurfer output
   │           │   └── orig.mgz
   │           └── surf                              # freesurfer output
   │               ├── lh.area
   │               ├── lh.area.pial
   │               ├── lh.pial
   │               ├── lh.sphere.reg
   │               ├── lh.white
   │               ├── rh.area
   │               ├── rh.area.pial
   │               ├── rh.pial
   │               ├── rh.sphere.reg
   │               └── rh.white
   └── ...

**2. Run** *gan-mat*.

.. code-block::

   gan-mat -input_dir /INPUT/DATA/PATH -output_dir /OUTPUT/PATH <Options>

================ =============================================================================
**Options**      **Description**
---------------- -----------------------------------------------------------------------------
batch_size <num> Number of the batch size while synthesizing the T2-weighted MRI (default = 1)
---------------- -----------------------------------------------------------------------------
threads <num>    Number of threads (default = 6)
---------------- -----------------------------------------------------------------------------
T2               Synthesize T2-weight MRI and terminate
---------------- -----------------------------------------------------------------------------
myelin           Compute myelin-sensitive proxy (T1w/T2w ratio) and terminate
---------------- -----------------------------------------------------------------------------
matrix           Calculate microstructural profile covariance (MPC) matrix and terminate
---------------- -----------------------------------------------------------------------------
gradients        Generate microstructural gradient and terminate
================ =============================================================================

.. note::
   - If options of features (T2, myelin, matrix, gradients) are not provided, the pipeline will generate all outputs. 
   - All the outputs will be stored in the individual subject’s folder.

.. warning::
   The 10GB of GPU memory is required. In the case of low GPU capacity, change the **device** variable in the *~/GAN-MAT/functions/model/t2.py*.







