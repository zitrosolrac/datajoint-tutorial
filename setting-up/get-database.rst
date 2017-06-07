Getting connected to a database
===============================

In this section we will explore various options on how we can get connected to a database server
for use throughout the tutorial and beyond. We will review three major options, from the easiet (and 
most recommended) to the more involved but highly customizable.

Connect to DataJoint.io_ (Recommended)
---------------------------------------------------------------

.. _DataJoint.io: https://datajoint.io

If you want to get started trying out DataJoint as quickly as possible with minimal setup, we are
happy to offer a free tutorial database server via `DataJoint.io <https://datajoint.io>`_.


Follow these simple instructions to sign up and receive a username and password to the tutorial database
server hosted by DataJoint.io.


Signing up for a free tutorial database server
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Visit https://datajoint.io and click on the Sign Up button. 
2. Fill out your email and association.
3. Check "I want to sign up for tutorial database access"
4. Choose and enter a username. If available, this will be your database username.
5. Hit submit. You request will be reviewed and you will receive an email with database connection 
   information typically within 48 hours.

And that's it! 

.. note::
  When you create a new schema, your schema must start with ``username_`` substituting in your username. For
  an example, if you sign up with user name ``johndoe``, your schema name must start with ``johndoe_`` for you to have
  full control over tables defined in the schema. More details on this will be covered in the next section.

DataJoint.io_ also offers a general database hosting service to host entire data pipelines for yourself, your lab, or large multi-lab collaborations. If
you are interested in finding out more, be sure to visit us at https://datajoint.io!

Setting up a local database server (Intermediate)
-----------------------------------------------

Alternatively you can install and set up a database server to run on your local machine. This offers a very
portable solution, but it requires some additional steps to deploy the server. If you
decide to go this route, we strongly recommend you use `Docker <https://www.docker.com>`_ to download
and launch a pre-configured database server we have provided as a Docker image.

You can find a step-by-step instructions on setting up a local database server using Docker in our 
:doc:`local-database` tutorial!


.. toctree::
   :maxdepth: 2
   :hidden:
   :includehidden:

   local-database

Setting up a database server on another machine (Advanced)
----------------------------------------------------

Finally, you might want to set up a database server on dedicated server hardware. 
Properly setting up and maintaing a database server can require significant IT expertise and
infrastructure, depending on the desired scale. If you are interested in pursuing this option, you can find useful
configuration information at `our MySQL Docker image project <https://github.com/datajoint/mysql-docker>`_.

What's next?
------------
Once you have decided on your database server option and acquired access credentials, you are ready to move onto
setting up DataJoint library in Python or MATLAB! Pick your favorite language for
step-by-step instruction on installing and setting up DataJoint library.

* :doc:`datajoint-python`
* :doc:`datajoint-matlab`

