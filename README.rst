.. contents:: Table of contents
   :depth: 2

Installation
============
Install the rk from PyPI
------------------------
::

    $ sudo pip install rk

Uninstall the rk
----------------
::

    $ sudo pip uninstall rk

Quickstart
==========
**First**, make sure that you can login to a remote machine without entering password. The most basic form of the command is::

    $ ssh REMOTE_HOST

If your username is different on a remote machine, you can specify it by using this syntax::

    $ ssh REMOTE_USERNAME@REMOTE_HOST

Example::

    $ ssh albert@192.168.0.1

**Second**, install a template of a remote jupyter kernel::

    $ rk install-template

The rk created a template of a remote jupyter kernel inside system kernels location ``/usr/local/share/jupyter/kernels``.
A kernel identifies itself to jupyter by creating a directory, the name of which is used as an identifier for the kernel [1]_.

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

* template -- the name of a remote jupyter kernel,

  * display_name -- a kernel’s name as it should be displayed in the UI. Unlike the kernel name used in the API, this can contain arbitrary unicode characters [1]_,
  * interpreter -- an entry point or an absolute path to language interpreter on a remote machine,
  * language -- a name of the language of a kernel. When loading notebooks, if no matching kernelspec key (may differ across machines) is found, a kernel with a matching language will be used. This allows a notebook written on any python or julia kernel to be properly associated with the user's python or julia kernel, even if they aren’t listed under the same name as the author’s [1]_,
  * remote_host -- just a remote host or, if your username is different on a remote machine, use this syntax: remote username AT remote host. 

.. note:: For checking absolute path to language interpreter on a remote machine use a ``which`` Unix command [2]_. For example, for the python3 language on a remote machine: ``$ which python3``.

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
  * ``92.168.0.1`` -- the remote host.

Show list of remote jupyter kernels from kernels dict
-----------------------------------------------------
::

    $ rk list

Install a remote jupyter kernel/kernels
---------------------------------------
::

    $ rk install KERNEL_NAME [KERNEL_NAME ...]

Where:

* KERNEL_NAME -- a name of a remote jupyter kernel in the kernels dict ``kernels.json``.

Example::

    $ rk install albert2
    $ rk install albert2 albert3

Install a template of a remote jupyter kernel
---------------------------------------------
::

    $ rk install-template

.. important:: After this subcommand open the  ``kernel.json`` file and change values of dict: ``$ sudo gedit /usr/local/share/jupyter/kernels/template/kernel.json``.


Install all remote jupyter kernels from kernels dict
----------------------------------------------------
::

    $ rk install-all

Uninstall a remote jupyter kernel/kernels
-----------------------------------------
::

    $ rk uninstall KERNEL_NAME [KERNEL_NAME ...]

Where:

* KERNEL_NAME -- a name of installed remote jupyter kernel.

Example::

    $ rk uninstall albert2
    $ rk uninstall albert2 albert3

Uninstall a template of a remote jupyter kernel
-----------------------------------------------
::

    $ rk uninstall-template

Uninstall all jupyter kernels from kernels location
---------------------------------------------------
::

    $ rk uninstall-all

.. note:: The default `kernels location <http://ipython.org/ipython-doc/dev/development/kernels.html#kernel-specs>`_ in the rk: ``/usr/local/share/jupyter/kernels``. Change the default `kernels location <http://ipython.org/ipython-doc/dev/development/kernels.html#kernel-specs>`_: ``$ sudo gedit /usr/local/lib/python2.7/dist-packages/rk/config/rk.ini``.

History
=======
Legend
------

* **added**
* corrected
* *removed*

rk 0.2
------

* **uninstall all jupyter kernels from kernels location with a "uninstall-all" subcommand.**
* **uninstall remote jupyter kernel/kernels with a "uninstall" subcommand.**
* **install remote jupyter kernel/kernels with a "install" subcommand.**
* **install all remote jupyter kernels from kernels dict with a "install-all" subcommand.**
* **show list of remote jupyter kernels from kernels dict with a "list" subcommand.**

.. rubric:: Footnotes

.. [1] http://ipython.org/ipython-doc/dev/development/kernels.html#kernel-specs
.. [2] http://unixhelp.ed.ac.uk/CGI/man-cgi?which
