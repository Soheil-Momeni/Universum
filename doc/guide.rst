Getting started
===============

This guide will provide an example step-by-step tutorial on setting up CI for a GitHub project, using Jenkins server,
GitHub application and Pylint analyzer. These are the steps to take:

1. :ref:`Install Universum <guide#install>`
2. :ref:`Load project to VCS <guide#vcs>`
3. :ref:`Initialize Unviersum <guide#init>`
4. :ref:`Configure project <guide#configure>`
5. :ref:`Add static analyzer <guide#analyzer>`


.. _guide#install:

Install Universum
-----------------

First, before setting up Continious Integration, let's implement and test Universum support locally.

1. Make sure your system meets Universum :doc:`prerequisites <install>`
2. Install Univesrum using ``{pip} install -U universum`` command from command line
3. Run ``{python} -m universum --help`` to make sure the installation was successful

If nothing went wrong, you should get a list of available :doc:`command line parameters <args>`.


.. _guide#vcs:

Load project to VCS
-------------------

Using `a series of tutorials on creating new projects
 <https://docs.github.com/en/free-pro-team@latest/github/getting-started-with-github/quickstart>`__, let's
`create a repo <https://docs.github.com/en/free-pro-team@latest/github/getting-started-with-github/create-a-repo>`__
on GitHub. Presume we named it ``universum-test-project``. After creating a repo online, clone it locally::

    git clone https://github.com/user/universum-test-project.git
    cd universum-test-project
    ls -la

From now on we will refer to this directory as a project root.
Depending on how the project was initialized, project root directory might already contain a ``README.md`` file,
a ``.gitignore`` file or/and a license file (but no actual project sources yet).


.. _guide#init:

Initialize Universum
--------------------

After previous step, we should still be in project root directory.
Let's :ref:`initialize Universum <additional_commandst#init>` in that directory::

    {python} -m universum init

That will create a new file ``.universum.py`` and print a command to use it::

    {python} -m universum run

The default :doc:`configuration file <configuring>`, created by this command, looks like this::

    #!/usr/bin/env python3.7

    from universum.configuration_support import Configuration

    configs = Configuration([Step(name='Show directory contents', command=['ls', '-la']),
                             Step(name='Print a line', command=['bash', '-c', 'echo Hello world'])])

    if __name__ == '__main__':
        print(configs.dump())

Running suggested command ``{python} -m universum run`` should result in launching Universum and
getting an output like this::

    ==> Universum 1.0.0 started execution
    ==> Cleaning artifacts...
    1. Processing project configs
     |   ==> Adding file /home/user/universum-test-project/artifacts/CONFIGS_DUMP.txt to artifacts...
     └ [Success]

    2. Preprocessing artifact lists
     └ [Success]

    3. Executing build steps
     |   3.1.  [ 1/2 ] Show directory contents
     |      |   $ /usr/bin/ls -a
     |      |   .  ..  artifacts  .git	README.md  .universum.py
     |      └ [Success]
     |
     |   3.2.  [ 2/2 ] Print a line
     |      |   $ /usr/bin/bash -c 'echo Hello world'
     |      |   Hello world
     |      └ [Success]
     |
     └ [Success]

    4. Reporting build result
     |   ==> Here is the summarized build result:
     |   ==> 3. Executing build steps
     |   ==>   3.1.  [ 1/2 ] Show directory contents - Success
     |   ==>   3.2.  [ 2/2 ] Print a line - Success
     |   ==> Nowhere to report. Skipping...
     └ [Success]

    5. Collecting artifacts
     └ [Success]

    ==> Universum 1.0.0 finished execution


.. _guide#configure:

Configure project
-----------------

Let's add some actual sources to project directory. For example, a simple script ``run.sh``::

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

    configs = Configuration([Step(name='Run script', command=['run.sh', 'pass'])])

After this change, running ``{python} -m universum run`` should result in the following output::

    ==> Universum 1.0.0 started execution
    ==> Cleaning artifacts...
    1. Processing project configs
     |   ==> Adding file/home/user/universum-test-project/artifacts/CONFIGS_DUMP.txt to artifacts...
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

    ==> Universum 1.0.0 finished execution


.. _guide#analyzer:

Add static analyzer
-------------------

Say, instead of writing a script in `bash` we used `python`, and have the following script ``run.py``::

    import sys

    if len(sys.argv) < 2:
        print("Unknown outcome")
        sys.exit(2)
    if sys.argv[1] == "pass":
        print("Script succeeded")
        sys.exit(0)
    print("Script failed")
    sys.exit(1)

To use this script, we'd have to modify ``configs`` to this::

    configs = Configuration([Step(name='Run script', command=['python', 'run.py', 'pass'])])

which will get the same result as the previous one.

But, let's presume we want to make sure our Python code style
corresponds to PEP-8 from the very beginning. We might install `Pylint <https://www.pylint.org/>`__ via
``{pip} install -U pylint``, and then add the code style check::

    configs = Configuration([
        Step(name='Run script', command=['python', 'run.py', 'pass']),
        Step(name='Pylint check', code_report=True, command=[
            'python', '-m', 'universum.analyzers.pylint', '--python-version', '3.7',
            '--result-file', '${CODE_REPORT_FILE}', '--files', '*.py'
        ])
    ])

Running Universum with this config will produce the following output::

    ==> Universum 1.0.0 started execution
    ==> Cleaning artifacts...
    1. Processing project configs
     |   ==> Adding file /home/user/universum-test-project/artifacts/CONFIGS_DUMP.txt to artifacts...
     └ [Success]

    2. Preprocessing artifact lists
     └ [Success]

    3. Executing build steps
     |   3.1.  [ 1/2 ] Run script
     |      |   $ /usr/bin/python run.py pass
     |      └ [Success]
     |
     |   3.2.  [ 2/2 ] Pylint check
     |      |   $ /usr/bin/python -m universum.analyzers.pylint --python-version 3.7 --result-file /home/user/universum-test-project/code_report_results/Pylint_check.json --files '*.py'
     |      |   Error: Module sh got exit code 1
     |      └ [Failed]
     |
     └ [Success]

    4. Reporting build result
     |   ==> Here is the summarized build result:
     |   ==> 3. Executing build steps
     |   ==>   3.1.  [ 1/2 ] Run script - Success
     |   ==>   3.2.  [ 2/2 ] Pylint check - Failed
     |   ==> Nowhere to report. Skipping...
     └ [Success]

    5. Collecting artifacts
     └ [Success]

    ==> Universum 1.0.0 finished execution

Which means we already have some code style issues in the project sources. Open the ``Pylint_check.json`` file
with code style check results::

    [
        {
            "type": "convention",
            "module": "run",
            "obj": "",
            "line": 1,
            "column": 0,
            "path": "run.py",
            "symbol": "missing-module-docstring",
            "message": "Missing module docstring",
            "message-id": "C0114"
        }
    ]

Let's presume we do not indend to add docstrings to every module. Then this check failure can be fixed by simply
putting a ``pylintrc`` file in project root with following content::

    [MESSAGES CONTROL]
    disable = missing-docstring

Leading to `Universum` successful execution.
