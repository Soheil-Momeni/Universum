Getting started
===============

This guide will provide an example step-by-step tutorial on setting up CI for a GitHub project, using Jenkins server,
GitHub application and Pylint analyzer. These are the steps to take:

1. :ref:`Install Universum <guide#install>`
2. :ref:`Initialize Unviersum <guide#init>`
3. Set up or get access to Jenkins server to perform CI checks
4. Create a GitHub Application to report CI results to GitHub using :doc:`GitHub Handler <github_handler>`
5. :doc:`Install Universum <install>` on Jenkins node that will perform the CI checks
   and run the :doc:`GitHub Handler <github_handler>`
6. :ref:`Initialize Universum <additional_commandst#init>` in project sources by creating a default :doc:`configuration
   file <configuring>` and modifying it according to the project needs
7. Use ``{python} -m universum run`` to :ref:`check the provided configuration locally <additional_commandst#run>`
8. Submit a working configuration file to a GitHub along with project sources


.. _guide#install:

Install Universum
-----------------

First, before setting up Continious Integration, let's implement and test Universum support locally.

1. Make sure your system meets Universum :doc:`prerequisites <install>`
2. Install Univesrum using ``{pip} install -U universum`` command from command line
3. Run ``{python} -m universum --help`` to make sure the installation was successful

If nothing went wrong, you should get a list of available :doc:`command line parameters <args>`.


.. _guide#init:

Initialize Universum
--------------------

Create a directory for project sources to be stored::

    mkdir universum-test-project
    cd universum-test-project

Then, :ref:`initialize Universum <additional_commandst#init>` in that directory::

    {python} -m universum init

That will create a new file ``.universum.py`` and print a command to use it::

    {python} -m universum run

The default :doc:`configuration file <configuring>`, created by this command, looks like this::

    #!/usr/bin/env python3.7

    from universum.configuration_support import Configuration

    configs = Configuration([dict(name='Show directory contents', command=['ls', '-la']),
                          dict(name='Print a line', command=['bash', '-c', 'echo Hello world'])])

    if __name__ == '__main__':
        print(configs.dump())

This build scenario does pretty much nothing, so let's add some actual sources to project directory.
For example, a simple script ``run.sh``::

    #!/usr/bin/env bash

    if [ "$1" = "pass" ]
    then
        echo "Script succeeded"
        exit 0
    elif [ "$1" = "fail" ]
    then
        echo "Script failed"
        exit 1
    else
        echo "Unknown outcome"
        exit 2
    fi

Then, in configuration file we can refer to this script::

    configs = Configuration([dict(name='Run script', command=['run.sh', 'pass'])])

After this change, running ``{python} -m universum run`` should result in the following output::

    ==> Universum 0.19.3 started execution
    ==> Cleaning artifacts...
    1. Processing project configs
     |   ==> Adding file /home/user/work/artifacts/CONFIGS_DUMP.txt to artifacts...
     └ [Success]

    2. Preprocessing artifact lists
     └ [Success]

    3. Executing build steps
     |   3.1.  [ 1/1 ] Run script
     |      |   $ /home/user/work/run.sh pass
     |      |   Script succeeded
     |      └ [Success]
     |
     └ [Success]

    4. Reporting build result
     |   ==> Here is the summarized build result:
     |   ==> 3. Executing build steps
     |   ==>   3.1.  [ 1/1 ] Run script - Success
     |   ==> Nowhere to report. Skipping...
     └ [Success]

    5. Collecting artifacts
     └ [Success]

    ==> Universum 0.19.3 finished execution

.. Try adding colored highlighting
