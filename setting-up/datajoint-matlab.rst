Installing DataJoint for MATLAB
===============================

Here we will cover installing DataJoint library for MATLAB and configuring it to connect to a database server. If you don't have a database server configured yet, be sure to checkout :doc:`local_database`!

System requirements
-------------------
DataJoint for MATLAB requires **MATLAB R2015b** or later to function properly. Verify that you have the right MATLAB version before proceeding with the tutorial.

Installing DataJoint Toolbox
----------------------------

The entire source code for DataJoint MATLAB is made available at `datajoint/datajoint-matlab <https://github.com/datajoint/datajoint-matlab>`_ GitHub repository. Although you certainly can download and use DataJoint directly from source, DataJoint is available as a custom toolbox that you can download from `MATLAB File Exchange <https://www.mathworks.com/matlabcentral/fileexchange/63218-datajoint>`_. Follow this simple instruction to install DataJoint toolbox:

1. Navitage to `DataJoint toolbox <https://www.mathworks.com/matlabcentral/fileexchange/63218-datajoint>`_ on MATLAB File Exchange.
2. Click on ``Download`` button and select ``Toolbox`` to start downloading the toolbox.
3. Once download completes, click on the downloaded ``DataJoint.mltbx``. This will launch MATLAB automatically and bring up a pop up dialog showing details about the toolbox.
4. Clock on ``Install`` button and follow the instructions ont he screen to install the DataJoint toolbox.

And that's it! To verify that the toolbox was properly installed, run the following command in MATLAB:

.. code-block:: matlab

  >> dj.version

If that prints out DataJoint version without an error, you are good to go!

Configuring DataJoint
---------------------

Now you have DataJoint installed, let's configure the library to connect to the database server. Here we are going to assume that you have a database server running locally on your machine as would be the case if you followed the instructions from :doc:`local_database`. Start MATLAB and type in the following commands:

.. code-block:: matlab

  >> setenv('DJ_HOST', '127.0.0.1')
  >> setenv('DJ_USER', 'root')
  >> setenv('DJ_PASS', 'tutorial')

Here, we are setting environmental variables with ``setenv`` to update configurations for DataJoint connection.
Namely, we are specifing the address of the database (`DJ_HOST`), and the user name (`DJ_USER`) and the 
password (`DJ_PASS`). To connect to your local database, we set the database address to `'127.0.0.1'`. 
We are also using the username and password configured in the :doc:`last section <local_database>` (`'root'` and `'tutorial'`). 

.. note::
  If you would like to connect to a different database server from the one configured in :doc:`local_database`, 
  simpley use the host address, username and password for the target database server. These information are typically provided by your database administrator.

Now we have updated the connection configuration, let's check the connection status by calling `dj.conn()`:


.. code-block:: matlab

  >> dj.conn()

When you call it for the very first time after the installation, the above command will trigger downloading a few extra libraries needed for DataJoint and thus may take some time. If everything works, you should get a prompt like the following:

.. code-block:: matlab

  >> dj.conn()

   0:  127.0.0.1 via TCP/IP             Server version 5.7.17

   connection_id() 
   +---------------+
   10              


   ans = 

   Connection with properties:

               host: '127.0.0.1'
               user: 'root'
          initQuery: ''
      inTransaction: 0
             connId: 0
           packages: [0×1 containers.Map]
        foreignKeys: [0×0 struct]
        isConnected: 1

If you get a message that looks like above, then congratulations! You have just successfully accessed your (local) database server using DataJoint!

What's next
-----------

If everything went well, you now have a fully functional developement environment for DataJoint with MATLAB,
with a database server running locally on your machine. You can now move onto :doc:`/beginner/first_pipeline`
to start learning how to use DataJoint to design and build data pipelines, or explore any other tutorials in this site to learn specific features of DataJoint.
t
