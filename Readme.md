# MIPLIB

Microscope Image Processing Library (*MIPLIB*) is a Python 2.7 based software package, created especially for processing and analysis of fluorescece microscopy images. It contains functions for example for:

- image registration 2D/3D
- image deconvolution and fusion (2D/3D), based on efficient CUDA GPU accelerated algorithms
- Fourier Ring/Shell Correlation (FRC/FSC) based image resolution analysis -- and several blind image restoration methods based on FRC/FSC.
- Image quality analysis
- ...

The library is distributed under the following FreeBSD open source license

## How do I install it?

I would recommend going with the *Anaconda* Python distribution, as it removes all the hassle from installing the necessary packages. 

###Here's how to setup your machine for development:

  1. There are some C extensions in *miplib* that need to be compiled. Therefore, iff you are on a *Mac*, you will also need to install XCode command line tools. In order to do this, Open *Terminal* and write `xcode-select --install`. In addition, if you already upgraded to MacOS Mojave, you will also have to install the following: `open /Library/Developer/CommandLineTools/Packages/macOS_SDK_headers_for_macOS_10.14.pkg`. If you are on *Windows*, you will need the [C++ compiler](https://www.microsoft.com/en-us/download/details.aspx?id=44266)


3. Open *Terminal* and Clone the *MIBLIB* repository from Bitbucket: `git clone git@github.com:sakoho81/miplib.git`. The code will go to a sub-directory called *miplib* of the current directory. Put the code somewhere where it can stay for a while.
4. Go to the *miplib* directory and create a new Python virtual environment `conda env create -f environment.yml`. 
5. Activate the created virtual environment by writing `source activate miplib`
6. Now, install the *miplib* package to the new environment by executing the following in the *miplib* directory `python setup.py develop`. This will only create a link to the source code, so don't delete the *miplib* directory afterwards. 

### And if you are not a developer

Skip all the hassle above and install the *miplib* package through the Anaconda with ```conda install …``` (coming up)

## Contribute?

*MIPLIB* was born as a combination of several previously separate libraries. The code and structure, although working, might (does) not in all places make sense. Any suggestions for improvements, new features etc. are welcome. 

# Regarding Python versions

MIPLIB was developed in Python 2.7, which sadly, appears to approach its end of life. For that reason, I am currently working on migrating the library to Python 3. I am planning to move exclusively to Python 3, as soon as I get the library tested, and rewrite some parts of the code that don't seem to migrate well. 

## Publications

Here are some works that have been made possible by the MIPLIB (and its predecessors):


**Koho, S. *et al.* Fourier ring correlation simplifies image restoration in fluorescence microscopy. Nat. Commun. 10 3103 (2019).**

Koho, S. V. *et al.* Easy Two-Photon Image Scanning Microscopy with SPAD Array and Blind Image Reconstruction. *biorxiv* doi:10.1101/563288

Koho, S., T. Deguchi, and P. E. E. Hänninen. 2015. “A Software Tool for Tomographic Axial Superresolution in STED Microscopy.” Journal of Microscopy 260 (2): 208–18.

Koho, Sami, Elnaz Fazeli, John E. Eriksson, and Pekka E. Hänninen. 2016. “Image Quality Ranking Method for Microscopy.” Scientific Reports 6 (July): 28962.

Prabhakar, Neeraj, Markus Peurla, Sami Koho, Takahiro Deguchi, Tuomas Näreoja, H-C Huan-Cheng Chang, Jessica M. J. M. Rosenholm, and Pekka E. P. E. Hänninen. 2017. “STED-TEM Correlative Microscopy Leveraging Nanodiamonds as Intracellular Dual-Contrast Markers.” Small  1701807 (December): 1701807.

Deguchi, Takahiro, Sami Koho, Tuomas Näreoja, and Pekka Hänninen. 2014. “Axial Super-Resolution by Mirror-Reflected Stimulated Emission Depletion Microscopy.” Optical Review 21 (3): 389–94.

Deguchi, Takahiro, Sami V. Koho, Tuomas Näreoja, Juha Peltonen, and Pekka Hänninen. 2015. “Tomographic STED Microscopy to Study Bone Resorption.” In Proceedings of the SPIE, 9330:93301M – 93301M – 6.

