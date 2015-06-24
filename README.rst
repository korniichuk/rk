.. contents:: Table of contents
   :depth: 2

Installation
============
Install the rk from PyPI
------------------------
::

    $ sudo pip install rk

Install the rk from GitHub
--------------------------
::

    $ sudo pip install git+git://github.com/korniichuk/rk#egg=rk

Upgrade the rk from PyPI
------------------------
::

    $ sudo pip install -U rk

or::

    $ sudo pip install --upgrade rk

.. important:: The rk set to dafault the `kernels dict`_ ``kernels.json``. Save the current `kernels dict`_ to home dir before upgrade, and replace default `kernels dict`_ file after.

Uninstall the rk
----------------
::

    $ sudo pip uninstall rk

Development installation
========================
::

    $ git clone git://github.com/korniichuk/rk.git
    $ cd rk
    $ sudo pip install .

Quickstart
==========

.. image:: ./img/quickstart_0001_728px.png
  :alt: quickstart [youtube video]
  :target: https://youtu.be/joEIPZJUB94

**First**, make sure that you can login to a remote machine without entering password. The most basic form of the command is::

    $ ssh REMOTE_HOST

If your username is different on a remote machine, you can specify it by using this syntax::

    $ ssh REMOTE_USERNAME@REMOTE_HOST

Example::

    $ ssh albert@192.168.0.1

.. note:: You can `setup SSH for auto login without a password`_ like this: ``$ rk ssh``.

**Second**, install a template of a remote jupyter kernel to `kernels location`_::

    $ rk install-template

**Third**, change the ``kernel.json`` file::

   $ sudo gedit /usr/local/share/jupyter/kernels/template/kernel.json

The ``kernel.json`` file looks like this::

    {
     "argv": [
      "rkscript",
      "python",
      "{connection_file}",
      "remote_username@remote_host"
     ],
     "display_name": "Template",
     "language": "python"
    }

For a python2 remote jupyter kernel just change ``remote_username@remote_host``. For example from ``remote_username@remote_host`` to ``albert@192.168.0.1``.

**Fourth**, launch jupyter notebook and check your new remote juputer kernel::

    $ jupyter notebook

or::

    $ ipython notebook

Choose: ``Files -> New -> Template``.

User guide
==========
Help
----
The standard output for –help::

    $ rk -h

or::

    $ rk --help

For information on using subcommand "SUBCOMMAND", do::

    $ rk SUBCOMMAND -h

or::

    $ rk SUBCOMMAND --help

Example::

    $ rk install -h

Version
-------
The standard output for –version::

    $ rk -v

or::

    $ rk --version

Kernels dict
------------

.. image:: ./img/user_guide-_kernels_dict_0001_728px.png
  :alt: user guide: kernels dict [youtube video]
  :target: https://youtu.be/czh3K4xjVD4

Open ``kernels.json`` file::

    $ sudo gedit /usr/local/lib/python2.7/dist-packages/rk/config/kernels.json

The ``kernels.json`` file looks like this::

    {
     "template": {
      "display_name": "Template",
      "interpreter": "python",
      "language": "python",
      "remote_host": "remote_username@remote_host"
     }
    }

Where:

* ``template`` -- the name of a remote jupyter kernel,

  * ``display_name`` -- a kernel’s name as it should be displayed in the UI. Unlike the kernel name used in the API, this can contain arbitrary unicode characters [1]_,
  * ``interpreter`` -- an entry point or an absolute path to language interpreter on a remote machine,
  * ``language`` -- a name of the language of a kernel. When loading notebooks, if no matching kernelspec key (may differ across machines) is found, a kernel with a matching language will be used. This allows a notebook written on any python or julia kernel to be properly associated with the user's python or julia kernel, even if they aren’t listed under the same name as the author’s [1]_,
  * ``remote_host`` -- just a remote host or, if your username is different on a remote machine, use this syntax: remote username AT remote host. 

.. note:: For checking absolute path to language interpreter on a remote machine use a `which <http://unixhelp.ed.ac.uk/CGI/man-cgi?which>`_ Unix command. For example, for the python3 language on a remote machine: ``$ which python3``.

Change ``kernels.json`` file and add info about your remote jupyter kernels, for example like this::

    {
     "albert2": {
      "display_name": "Albert Python 2",
      "interpreter": "python2",
      "language": "python",
      "remote_host": "albert@192.168.0.1"
     },
     "albert3": {
      "display_name": "Albert Python 3",
      "interpreter": "python3",
      "language": "python",
      "remote_host": "albert@192.168.0.1"
     }
    }

Where:

* ``albert2``, ``albert3`` -- the names of a remote jupyter kernels,

  * ``Albert Python 2``, ``Albert Python 3`` -- the display names for the UI,
  * ``python2``, ``python3`` -- entry points on a remote machine,
  * ``python`` -- the name of the language of a remote jupyter kernel,
  * ``albert`` -- the remote username on a remote machine, not similar with a username on a local machine,
  * ``192.168.0.1`` -- the remote host.

Kernels location
----------------
Jupyter support the system and the user `kernels locations <http://ipython.org/ipython-doc/dev/development/kernels.html#kernel-specs>`_:

+----------+--------------------------------------------------------------------+
|          |kernels location                                                    |
+==========+====================================================================+
|**system**|``/usr/local/share/jupyter/kernels``; ``/usr/share/jupyter/kernels``|
+----------+--------------------------------------------------------------------+
|**user**  |``~/.ipython/kernels``                                              |
+----------+--------------------------------------------------------------------+

The default kernels location in the rk: ``/usr/local/share/jupyter/kernels``.

Change the default kernels location::

    $ sudo gedit /usr/local/lib/python2.7/dist-packages/rk/config/rk.ini

.. important:: The user kernels location takes priority over the system kernels locations.

Show list of remote jupyter kernels from kernels dict
-----------------------------------------------------
::

    $ rk list

Install a remote jupyter kernel/kernels from kernels dict to kernels location
-----------------------------------------------------------------------------
::

    $ rk install KERNEL_NAME [KERNEL_NAME ...]

Where:

* ``KERNEL_NAME`` -- a name of a remote jupyter kernel in the `kernels dict`_ ``kernels.json``.

Example::

    $ rk install albert2
    $ rk install albert2 albert3

Install a template of a remote jupyter kernel to kernels location
-----------------------------------------------------------------
::

    $ rk install-template

.. important:: After this subcommand open the  ``kernel.json`` file and change values of dict: ``$ sudo gedit /usr/local/share/jupyter/kernels/template/kernel.json``.

Install all remote jupyter kernels from kernels dict to kernels location
------------------------------------------------------------------------
::

    $ rk install-all

Uninstall a remote jupyter kernel/kernels from kernels location
---------------------------------------------------------------
::

    $ rk uninstall KERNEL_NAME [KERNEL_NAME ...]

Where:

* KERNEL_NAME -- a name of installed remote jupyter kernel.

Example::

    $ rk uninstall albert2
    $ rk uninstall albert2 albert3

Uninstall a template of a remote jupyter kernel from kernels location
---------------------------------------------------------------------
::

    $ rk uninstall-template

Uninstall all jupyter kernels from kernels location
---------------------------------------------------
::

    $ rk uninstall-all

Setup SSH for auto login without a password
-------------------------------------------
::

    $ rk ssh

If you are familiar with `ssh-keygen <http://www.openbsd.org/cgi-bin/man.cgi?query=ssh-keygen&sektion=1>`_, `ssh-copy-id <http://linux.die.net/man/1/ssh-copy-id>`_ and `ssh-add <http://www.openbsd.org/cgi-bin/man.cgi?query=ssh-add&sektion=1>`_, this code also setup SSH for auto login without a password [2]_::

    $ ssh-keygen -t rsa -b 4096 -N '' -f ~/.ssh/id_rsa
    $ ssh-copy-id REMOTE_HOST
    $ eval "$(ssh-agent -s)"
    $ ssh-add ~/.ssh/id_rsa

.. note:: If your username is different on a remote machine, you can specify it by using this syntax: ``$ ssh-copy-id REMOTE_USERNAME@REMOTE_HOST``.

Log files
---------
The default log files location in the rk: ``/tmp/rk/log``. The name of rk log file, for working remote jupyter kernel, look like this: ``bree@192.168.0.1_1879-03-14_11.30.00.txt``. And the log file looks like this::

    date: 1879-03-14 Friday
    time: 11:30:00

    usernames: bree<->albert
    remote host: 192.168.0.1

    stdin ports: 37654<->58933
    hb ports: 53538<->59782
    iopub ports: 45330<->51989
    shell ports: 36523<->36107
    control ports: 50090<->53633

    pids: 16965<->20944

.. note:: Change the default log files location: ``$ sudo gedit /usr/local/lib/python2.7/dist-packages/rk/config/rk.ini``.

The paramiko log file is available in a local connection file directory. The name of paramiko log file, for working remote jupyter kernel, look like this: ``paramiko-843664c7-798d-4a9e-979c-22d0dc4a6bd5.txt``.

History
=======
Legend
------

* **added**
* corrected
* *removed*

rk 0.3
------

* bug in the rk and in the rkscript: an initial component of ``~`` or ``~user`` is not replaced in a paths.
* bug in the rk: a superuser (root) privileges required for the user kernels location ``~/.ipython/kernels``.
* **setup SSH for auto login without a password with a "ssh" subcommand.**
* error in the rkscript: list index out of range.
* **info about working remote jupyter kernel in rk log file.**
* **paramiko log file in a local connection file dir.**
* error in the rkscript: no handlers could be found for logger "paramiko.transport".
* local port forwarding in the rkscript via paramiko, not via pexpect.

rk 0.2
------

* **uninstall all jupyter kernels from kernels location with a "uninstall-all" subcommand.**
* **uninstall a remote jupyter kernel/kernels from kernels location with a "uninstall" subcommand.**
* **install a remote jupyter kernel/kernels from kernels dict to kernels location with a "install" subcommand.**
* **install all remote jupyter kernels from kernels dict to kernels location with a "install-all" subcommand.**
* **show list of remote jupyter kernels from kernels dict with a "list" subcommand.**

.. rubric:: Footnotes

.. [1] http://ipython.org/ipython-doc/dev/development/kernels.html#kernel-specs
.. [2] https://help.github.com/articles/generating-ssh-keys/
