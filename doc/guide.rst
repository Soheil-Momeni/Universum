Getting started
===============

This guide will provide an example step-by-step tutorial on setting up CI for a GitHub project, using Jenkins server,
GitHub application and Pylint analyzer. These are the steps to take:

1. Create a project on GitHub (add link to actual example project)
2. Set up or get access to Jenkins server to perform CI checks
3. Create a GitHub Application to report CI results to GitHub using :doc:`GitHub Handler <github_handler>`
4. :doc:`Install Universum <install>` on Jenkins node that will perform the CI checks
   and run the :doc:`GitHub Handler <github_handler>`

   * Use ``{python} -m universum --help`` to make sure the installation
     was successful, and also to get the list of available :doc:`parameters <args>`

5. :ref:`Initialize Universum <additional_commandst#init>` in project sources by creating a default :doc:`configuration
   file <configuring>` and modifying it according to the project needs
6. Use ``{python} -m universum run`` to :ref:`check the provided configuration locally <additional_commandst#run>`
7. Submit a working configuration file to a GitHub along with project sources
