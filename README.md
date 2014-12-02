# SAMBUCA Python and AGDC Project
*Note:* Temporarily creating this repo in my (Daniel's) personal Stash
project. We can move or clone it later when there is a better location.

*Todo:* Insert actual description of Sambuca here.

*Todo:* Insert description of Python modules/packages here.

## Development on Bragg-l
Note that Sambuca development is using virtual environments to facilitate 
testing and development of the Sambuca package. To enable use of the optimised
numpy and scipy packages, the virtual environment is created with
--system-site-packages. However, for testing the package installation and
dependencies, a clean virtual environment should be used. The goal is to
create a Sambuca package that will install cleanly using standard Python tools
and have it "just work".

### Once only
1.  load the git module :

        $ module load git

2.  Setup virtualenvwrapper by adding the following 2 lines to your
    .bashrc (substituting your own desired locations) :

        export WORKON_HOME=$HOME/.virtualenvs
        export PROJECT_HOME=~/projects

3.  If they don't already exist, create the .virtualenvs and projects
    directories.
4.  Clone the Git repository :

        $ cd ~/projects
        $ git clone https://col52j@stash.csiro.au/scm/~col52j/sambuca.git

5.  Load the Python version used for development :

        $ module load python/2.7.6

6.  Activate the virtualenvwrapper scripts :

        $ source /apps/python/2.7.6/bin/virtualenvwrapper_lazy.sh

7.  Change to the sambuca directory :

        $ cd ~/projects/sambuca

8.  Make the virtual environment for Sambuca, associate it with the
    project directory created by the git clone operation, and allow the
    virtual environment to access the system site packages :

        $ mkvirtualenv -a . --system-site-packages sambuca

### Every time
1.  Load the Python version used for development :

        $ module load python/2.7.6

2.  Activate the virtualenvwrapper scripts: :

        $ source /apps/python/2.7.6/bin/virtualenvwrapper_lazy.sh

3.  Activate the sambuca virtual environment: :

        $ workon sambuca

4.  You can now work on the sambuca python code. Any Python packages you
    install with pip will be installed into the virtual environment.
    System packages are still available.
5.  To deactivate the virtual environment, simply use the
    virtualenvwrapper command (or simply close the terminal window) :

        $ deactivate

## Documentation
*Todo:* Link to documentation (ReadTheDocs?)

## Quickstart
*Todo*

## Description of Reference Folders
-   IDL: Original IDL code
    -   amoeba\_clw7.pro: Amoeba minimisation function
    -   sambuca\_2009.pro: current *gold standard* for core SAMBUCA.
    -   sambuca\_2009\_wid.pro: IDL widgets/GUI code for the *gold
        standard* SAMBUCA.
    -   SAMBUCA.zip: Luke Domanski's code from a previous eRCP.
        -   Runs on Linux with GDL
        -   Removed dependencies on ENVI software
        -   Requires Linux?
        -   Parallel execution on a Linux cluster via Luke's Parallel
            Execution Framework
        -   Not utilised by the team due to Linux requirement and other
            usability issues (what were they? I want to avoid them this
            time around).
-   Matlab: Stephen Sagar's lightweight Matlab implementation of
    SAMBUCA. See the matlab readme for more detail.
    -   fSambuca.m: forward model
    -   SinglePixSpecMCMC.m: sampling algorithm

