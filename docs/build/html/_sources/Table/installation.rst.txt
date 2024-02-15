------------
INSTALLATION
------------

GAN-MAT was developed on Python 3.9.
  
Dependencies & Python packages
==============================

.. code-block::

   FSL v.6.0
   FreeSurfer v.6.0.0
   Workbench v.1.5.0
   GNU Parallel
   brainspace == 0.1.4
   numpy >= 1.18.5 & numpy <= 1.25.0
   scipy >= 1.4.1 & scipy <= 1.9.1
   nibabel == 4.0.2
   torch == 1.12
   torchvision == 0.13.1
   scikit-image == 0.19.3
   tqdm

Installation
============

**1. Download the code from our GitHub page:**

.. code-block::
   
   git clone https://github.com/CAMIN-neuro/GAN-MAT.git

**2. Download the model at the link below:**
   
`link`_

**3. Move the downloaded model to the GAN-MAT folder:**
   
.. code-block::

   mv /DOWNLOAD/DIRECTORY/model.pth /GAN-MAT/DIRECTORY/GAN-MAT/functions/model 
   # Change  the path to your directories!

**4. Set the environment:**

.. code-block::
   
   export GANMAT=/Your/GAN-MAT/Directory
   PATH=${PATH}:${GANMAT}:${GANMAT}/functions
   export PATH



