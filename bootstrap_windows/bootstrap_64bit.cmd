@echo off
setlocal EnableDelayedExpansion

REM Set CONDA_ENV to the name of the environment you wish to create.
REM TODO: this could be passed in as a command line arg
set CONDA_ENV=sam

echo ---- Creating Conda environment %CONDA_ENV%
conda create --yes --name %CONDA_ENV% --file conda_reqs_64.txt

echo ---- Activating Conda environment
call activate %CONDA_ENV%
conda info --envs

echo ---- Installing third-party pip packages
REM pip install --requirement ./pip_reqs_64.txt

REM echo ---- Installing Sambuca Core in develop mode
REM cd ..\..\sambuca_core
REM python setup.py develop

REM echo ---- Installing Sambuca in develop mode
REM cd ..\sambuca
REM python setup.py develop

REM echo ---- Installing Bioopti in develop mode
REM cd ..\bioopti
REM python setup.py develop

REM echo ---- Done!
