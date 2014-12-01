# SAMBUCA Python and AGDC Project
*Note:* Temporarily creating this repo in my (Daniel's) personal Stash project. We can
move or clone it later when there is a better location.

*Todo:* Insert actual description of Sambuca here.
*Todo:* Insert description of Python modules/packages here.
---

## Description of Reference Folders
* IDL: Original IDL code
    * amoeba_clw7.pro: Amoeba minimisation function
    * sambuca_2009.pro: current *gold standard* for core SAMBUCA.
    * sambuca_2009_wid.pro: IDL widgets/GUI code for the *gold standard* SAMBUCA.
    * SAMBUCA.zip: Luke Domanski's code from a previous eRCP.
        * Runs on Linux with GDL
        * Removed dependencies on ENVI software
        * Requires Linux?
        * Parallel execution on a Linux cluster via Luke's Parallel Execution
          Framework
        * Not utilised by the team due to Linux requirement and other usability
          issues (what were they? I want to avoid them this time around).
* Matlab: Stephen Sagar's lightweight Matlab implementation of SAMBUCA. See the
  matlab readme for more detail.
    * fSambuca.m: forward model
    * SinglePixSpecMCMC.m: sampling algorithm
