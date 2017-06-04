Installing DataJoint for Python
===============================

Here we will cover installing DataJoint library for Python and configuring it to connect to a database server. If you don't have a database server configured yet, be sure to checkout :doc:`local_database`!

System requirements
-------------------
DataJoint for Python requires **Python 3.4 or above** to function properly. To check whether you have the 
right Python version, run the following in terminal/command prompt:

.. code-block:: bash

    $ python3 -V

If the above command runs without an error and the version is at least `3.4` (e.g.`3.6.0`),
then you are good to go!

Installing DataJoint Package
----------------------------

The entire source code for DataJoint Python is made available at `datajoint/datajoint-python <https://github.com/datajoint/datajoint-python>`_ 
GitHub repository. Although you certainly can install DataJoint directly from the source, it will be much 
easier to use `pip` - Python's package manager. The latest stable DataJoint releases are made available as
a package at `PyPI <https://pypi.python.org/pypi/datajoint/>`_. With this you can install DataJoint for Python
by just running the following in the terminal:

.. code-block:: bash

    $ pip3 install --upgrade datajoint


and that's it! This should trigger the installation of the latest DataJoint and all of its dependencies. 
Depending on how your Python environment is configured, you may have to add `sudo` to the above command.

Verify that the package was properly installed by starting a Python 3 console, and try importing the 
`datajoint` package:

.. code-block:: python

  >>> import datajoint as dj

Make sure you have DataJoint package installed successfully before moving on.

Configuring DataJoint
---------------------

Now you have DataJoint installed, let's configure the library to connect to the database server. 
Here we are going to assume that you have a database server running locally on your machine as would be 
the case if you followed the instructions from :doc:`local_database`. 
Start an interactive Python 3 console and type in the following commands:

.. code-block:: python

  >>> import datajoint as dj
  >>> dj.config['database.host'] = '127.0.0.1'
  >>> dj.config['database.user'] = 'root'
  >>> dj.config['database.password'] = 'tutorial'

Here, we are using the ``dj.config`` object to update configurations for DataJoint. Namely, we are specifing 
the address of the database (``database.host``), and the user name (``database.user``) and the password 
(``database.password``). To connect to your local database, we set the database address to be ``'127.0.0.1'``.
Here, we are using the username and password configured from the :doc:`last section <local_database>` (`'root'` and `'tutorial'`). 

.. note::
  If you would like to connect to a different database server from the one configured in :doc:`local_database`,
  simpley use the host address, username and password for the target database server. These information are typically provided by your database administrator.

Now we have updated the connection configuration, let's check the connection status by calling `dj.conn()`:

.. code-block:: python

  >>> dj.conn()
  Connecting root@localhost:3306
  DataJoint connection (connected) root@localhost:3306

If you get a message that looks like above, then congratulations! You have just successfully accessed your (local) database server using DataJoint!

What's next
-----------

If everything went well, you now have a fully functional developement environment for DataJoint with Python,
with a database server running locally on your machine. You can now move onto :doc:`/beginner/first_pipeline`
to start learning how to use DataJoint to design and build data pipelines, or explore any other tutorials in this site to learn specific features of DataJoint.
