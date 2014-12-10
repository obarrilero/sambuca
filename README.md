# SAMBUCA Python and AGDC Project
*Note:* Temporarily creating this repo in my (Daniel's) personal Stash
project. We can move or clone it later when there is a better location.

*Todo:* Insert actual description of Sambuca here.

*Todo:* Insert description of Python modules/packages here.

## Development
*Tested on Bragg-l, but should also work on other enviroments*
Note that Sambuca development is using virtual environments to facilitate
testing and development. To enable use of the optimised numpy and scipy
packages, the virtual environment is created with --system-site-packages.
However, for testing the package installation and dependencies, a clean virtual
environment should be used. The goal is to create a Sambuca package that will
install cleanly using standard Python tools and have it "just work".

### Once only
1.  load the git module :

        $ module load git
2.  Setup virtualenvwrapper by adding the following 2 lines to your
    .bashrc (substituting your own desired locations) :

        export WORKON_HOME=$HOME/.virtualenvs
        export PROJECT_HOME=~/projects

3.  If they don't already exist, create the .virtualenvs and projects
    directories specified in the previous step.

3.  Create a directory in projects to act as the top level sambuca directory :

        $ cd ~/projects/
        $ mkdir sambuca_project

4.  Clone the Git repositories for sambuca and sambuca_agdc into the
    sambuca_project directory :

        $ cd ~/projects/sambuca_project/
        $ git clone https://col52j@stash.csiro.au/scm/~col52j/sambuca.git
        $ git clone https://col52j@stash.csiro.au/scm/~col52j/sambuca_agdc.git

5.  Load the Python version used for development :

        $ module load python/2.7.6

6.  Activate the virtualenvwrapper scripts :

        $ source /apps/python/2.7.6/bin/virtualenvwrapper_lazy.sh

7.  Change to the top-level sambuca project directory :

        $ cd ~/projects/sambuca_project/

8.  Make a virtual environment called sambuca that will be shared by sambuca and
    sambuca_agdc, associate it with the project directory, and allow the virtual
    environment to access the system site packages (required for access to
    site-optimised packages like numpy and scipy). :

        $ mkvirtualenv -a . --system-site-packages sambuca

9.  Install the sambuca and sambuca_agdc packages into your virtual environment
    in development mode. This makes the packages available via symlinks to your
    development code, so that code changes are reflected in the package without
    reinstallation (although you need to restart your python environment, or use
    the IPython %autoreload extension) :

        $ workon sambuca
        $ cdproject
        $ python setup.py develop

10. Install additional packages specified in the setup.py script :
        $ cd sambuca
        $ pip install --upgrade -e.[dev,test]
        $ cd ../sambuca_agdc
        $ pip install --upgrade -e.[dev,test]

### Every time
1.  Load the Python version used for development :

        $ module load python/2.7.6

2.  Activate the virtualenvwrapper scripts :

        $ source /apps/python/2.7.6/bin/virtualenvwrapper_lazy.sh

3.  Activate the sambuca virtual environment :

        $ workon sambuca

4.  You can now work on the sambuca python code. Any Python packages you
    install with pip will be installed into the virtual environment.
    System packages are still available.

5.  To deactivate the virtual environment, simply use the
    virtualenvwrapper command (or simply close the terminal window) :

        $ deactivate

## Testing
- Tests are implemented with pytest, with integration into the setup.py script :

        $ python setup.py tests

- The tox framework was tested, as it provides automated testing against
  multiple Python versions (2 & 3). However, tox did not work correctly with the
  system-site-packages setting. The system-site-packages setting is required to
  access the system packages numpy and scipy. Compiling these packages is
  difficult and makes the use of fully encapsulated virtual enviroments
  problematic.
    - A workaround is to create separate virtual environments based on Python
      2.7 and Python 3.4, and then run the tests within both environments.
      A helper script makes this easier.
## Documentation
*Todo:* Link to documentation (ReadTheDocs?)

## Packaging Sambuca
1. Generate the README.rst file :

        $ module load pandoc
        $ pandoc -o README.rst README.md

2. Todo

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

