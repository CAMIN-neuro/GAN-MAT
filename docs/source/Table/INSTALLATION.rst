------------
INSTALLATION
------------

GAN-MAT was developed on Python 3.9.
  
Dependencies & Python packages
==============================

.. code-block::

   FSL v.6.0
   FreeSurfer v.7.3.2
   AFNI v.22.1.14
   ANTs v.2.3.5
   Workbench v.1.5.0
   GNU Parallel
   brainspace == 0.1.10
   numpy == 1.24.4
   scipy == 1.9.3
   nibabel == 5.2.0
   torch == 2.1.2
   tqdm

Installation
============

**1. Download the code from our GitHub page:**

.. code-block::
   
   git clone https://github.com/CAMIN-neuro/GAN-MAT.git

**2. Download the model at the link below:**
   
`<https://www.dropbox.com/sh/nnzayieuizd012y/AACLSwUY9BBTCdf66_nWqK02a?dl=0>`_


**3. Move the downloaded model to the GAN-MAT folder:**
   
.. code-block::

   mv /DOWNLOAD/DIRECTORY/model.pth /GAN-MAT/DIRECTORY/GAN-MAT/functions/model 
   # Change  the path to your directories!

**4. Set the environment:**

.. code-block::
   
   export GANMAT=/Your/GAN-MAT/Directory
   PATH=${PATH}:${GANMAT}:${GANMAT}/functions
   export PATH



