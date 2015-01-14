============
Contributing
============

**Note:** This contributing document is in two sections. The first describes
in-house development during the pre-release stage, and this should be removed
before the project is published. The second section is a placeholder template
that can be updated to form the post-release documentation.

In-house Development
--------------------
*Tested on Bragg-l, but should also work in other environments*
Note that Sambuca development is using virtual environments to facilitate
testing and development. To enable use of the optimised numpy and scipy
packages, the virtual environment is created with --system-site-packages.
However, for testing the package installation and dependencies, a clean virtual
environment should be used. The goal is to create a Sambuca package that will
install cleanly using standard Python tools and have it "just work".

Once only
^^^^^^^^^
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

Every time
^^^^^^^^^^
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

Testing
-------
- Tests are implemented with pytest, with integration into the setup.py script.
  The simplest way to run the tests is to call py.test from the project
  directory :

        $ py.test

- The tox framework was tested, as it provides automated testing against
  multiple Python versions (2 & 3). However, tox did not work correctly with the
  system-site-packages setting. The system-site-packages setting is required to
  access the system packages numpy and scipy. Compiling these packages is
  difficult and makes the use of fully encapsulated virtual enviroments
  problematic.
    - A workaround is to create separate virtual environments based on Python
      2.7 and Python 3.4, and then run the tests within both environments.
      A helper script makes this easier.

============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given.

Bug reports
-----------

When `reporting a bug <https://jira.csiro.au/sambuca>`_ please include:

    * Your operating system name and version.
    * Any details about your local setup that might be helpful in troubleshooting.
    * The Sambuca package version.
    * Detailed steps to reproduce the bug.

Documentation improvements
--------------------------

Sambuca could always use more documentation, whether as part of the
official Sambuca docs, in docstrings, or even on the web in blog posts,
articles, and such.

Feature requests and feedback
-----------------------------

The best way to send feedback is to file an issue at https://jira.csiro.au/sambuca.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions are welcome :)

Or, implement the feature yourself and submit a pull request.

Development
===========

To set up `sambuca` for local development:


*To Do*: Once Sambuca is on GitHub (or somewhere similar), the following
instructions may make a useful template.

1. `Fork Sambuca on GitHub <https://github.com/...>`_.
2. Clone your fork locally::

    git clone git@github.com:your_name_here/sambuca.git

3. Create a branch for local development::

    git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

4. When you're done making changes, run all the tests, doc builder and pylint
   checks:

    py.test
    todo: docs
    pylint sambuca

5. Commit your changes and push your branch to GitHub::

    git add .
    git commit -m "Your detailed description of your changes."
    git push origin name-of-your-bugfix-or-feature

6. Submit a pull request through the GitHub website.

Pull Request Guidelines
-----------------------

If you need some code review or feedback while you're developing the code just make the pull request.

For merging, you should:

1. Include passing tests (run ``py.test``) [1]_.
2. Update documentation when there's new API, functionality etc.
3. Add a note to ``CHANGELOG.rst`` about the changes.
4. Add yourself to ``AUTHORS.rst``.

.. [1] If you don't have all the necessary python versions available locally you can rely on Travis - it will
       `run the tests <https://travis-ci.org/dc23/python-nameless/pull_requests>`_ for each change you add in the pull request.

       It will be slower though ...
