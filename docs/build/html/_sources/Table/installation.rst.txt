------------
Installation
------------

Download
========

Deu to the size of the model, we separately uploaded the code and model.

1. Download the code from Github as follow:

.. code-block::
   
   git clone """site"""
   "..."

2. Download the model at follow link: 
   
   `https://www.dropbox.com/sh/nnzayieuizd012y/AACLSwUY9BBTCdf66_nWqK02a?dl=0 <https://www.dropbox.com/sh/nnzayieuizd012y/AACLSwUY9BBTCdf66_nWqK02a?dl=0>`_

3. Move model to GAN-MAT folder
   
   Move **model.pth** file to **../GAN-MAT/functions/model** folder

4. Set up environment variables in your desktop

.. code-block::
   
   export GANMAT="your GAN-MAT diractory path"
   PATH=${PATH}:${GANMAT}:${GANMAT}/functions
   export PATH
  
Dependencies
============

our program needs four progams and python packages.

Programs
~~~~~~~~

- FSL
- Workbench
- Freesurfer
- GNU Parallel

Python packages
~~~~~~~~~~~~~~~

- numpy
- scipy 
- nibabel
- brainspace
- torch
- torchvision
- scikit-image
- tqdm


