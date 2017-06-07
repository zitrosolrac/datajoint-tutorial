Importing data into a table
===========================

Now we have tables for organizing mouse and experiment sessions, it's time
for us to load the data recorded during each experimental session!
In this section, we will look at creating an **imported table**, 
a table that will automatically import data from files.

Setting up tables
-----------------
For this section, we will be using mock experimental data to be loaded into the
table. For this to work properly, the content of the ``Session`` table must look
exactly as following for the primary key attributes (``mouse_id`` and ``session_date``)

.. code-block:: python

  *mouse_id    *session_date  experiment_set experimenter
  +----------+ +------------+ +------------+ +------------+
  0            2017-05-15     0              Edgar Walker
  0            2017-05-19     0              Edgar Walker
  5            2017-01-05     1              Fabian Sinz
  100          2017-05-25     1              Jake Reimer
   (4 tuples)

If your ``Session`` table doesn't quite have the same set of primary keys (``mouse_id``
and ``session_date`` combinations) as shown above, make use of the various ``insert`` methods
covered in :doc:`inserting-data` and ``delete`` method covered in :ref:`python-delete-entries`
to adjust your ``Session`` table content until it matches the table shown above.

If you are missing some of the mouse in ``Mouse`` table, you may have to insert the 
appropriate mouse into your ``Mouse`` table before you can insert a session corresponding 
to that mouse into the ``Session`` table.

Getting the data
----------------
You can download the (mock) experimental data for the above sessions packaged into a ZIP file
here:

:download:`Experiment data </_static/data/python-data.zip>`

Go ahead and download the ZIP file and unzip the content. Place the ``data`` directory from the
ZIP file somewhere where you'd remember. You will need the full path to this ``data`` directory
to follow the rest of this section. In what follows, we will be refering to the path to the data
simply as ``/path/to/data/`` so be sure to substitute the full path to the ``data`` folder when trying
out the commands below.

The follow are a few examples demonstrating what your data path might look like:

MacOS
^^^^^

If you extract the ``data`` folder into your ``Desktop``, for example, then the path to the
``data`` folder will be something like ``/home/username/Desktop/data`` where you replace ``username``
with your user name for your machine.

Windows
^^^^^^^

On Windows, if you extracted ``data`` folder onto your ``Desktop``, then the full path to the ``data``
folder will look like ``C:\Users\username\Desktop\data`` where you replace ``username`` with
your user name for your machine.

Linux
^^^^^

If you extracted the ``data`` directory to your home folder, then the full path to the ``data``
directory will be something like ``/home/username/data`` where you replace ``username``
with your user name on the machine.

Data files
----------
In side the ``data`` directory, you will find 4 ``.npy`` (saved NumPy array) files with names like
``data_100_2017-05-25.npy``. As you might have guessed, these are the data for the 4 recording
sessions in the ``Session`` table, and each file are named according to the ``mouse_id`` and
``session_date`` - the attributes of the primary keys - in the format ``data_{mouse_id}_{session_date}.npy``.

Let's take a quick peak at the data content:

.. code-block:: python

  >>> import numpy as np     # import the numpy library
  >>> data = np.load('/path/to/data/data_100_2017-05-25.npy')
  >>> data.shape
  (1000,)

So this particular file contains a NumPy array of length 1000. This represents a recording of 
raw electric activity from a single neuron over 1000 time bins from that particular session!

Other files contain similar looking data in NumPy array format, giving the electric activity
from a neuron recorded from each session.

We would now like to **import** all these data into a table so that we can maintain and manipuate
all data inside DataJoint.

Imported table
--------------

Unlike the ``Manual`` tables like ``Mouse`` and ``Session`` where new data were entered **manually**
(e.g. via ``insert`` methods), we would now like to create a table called ``Neuron`` whose
table data content is imported from the files above, and better yet, automatically! We can 
achieve this in DataJoint by defining an ``Imported`` table. Just like the ``Manual`` table,
we start by specifiying the table definition:

.. code-block:: python

  @schema
  class Neuron(dj.Imported):
      definition = """
      -> Session
      ---
      activity:  longblob    # electric activity of the neuron
      """

.. note::
  Go ahead and define the above class, thus defining the table inside the database. However,
  keep your class definition around as we will be coming back and addming more content to
  it shortly!

Notice that we have subclassed ``dj.Imported`` instead of ``dj.Manual``, indicating that this is
going to be an "imported" table. Since we record from one neuron in each session, the neuron
can be uniquely identified by knowing which session it was recorded in. Thus the primary key
simply consists of the dependency on ``Session`` (for review on table dependency, take a look
at :doc:`child-table`).

The next bit is interesting. For each neuron, we want to store the recorded electric activity
which is a NumPy array. The table data type ``longblob`` allows us to store an arbitrary array
data (i.e. NumPy array) into the table!

So far the ``Neuron`` doesn't seem to be too much different from a manual table like ``Session``.
One big difference between an imported table (``dj.Imported``) and a manual table (``dj.Manual``)
is the fact imported table comes with a special method called ``populate``.

``populate`` method
-------------------

A key feature that makes imported feature special (and very cool!) is the existence of the
``populate`` method. Let's go ahead and 1) instantiate our new table and 2) call ``populate``
method on it.

.. code-block:: python
  
  >>> neuron = Neuron()
  >>> neuron        # view the content - should be empty
  *mouse_id    *session_date  activity
  +----------+ +------------+ +----------+
  

   (0 tuples)
  >>> neuron.populate()     # call populate method
  ---------------------------------------------------------------------------
  NotImplementedError                       Traceback (most recent call last)
  <ipython-input-211-196e0eb3db4d> in <module>()
  ----> 1 neuron.populate()

  (...message truncated...)

  NotImplementedError: Subclasses of AutoPopulate must implement the method "_make_tuples"

Notice how calling the ``populate`` method triggered a ``NoteImplementedError`` compaining that
the method ``_make_tuples`` is not defined. To get a better sense of what's going on, let's go
back to our class definition and add a very basic ``_make_tuples`` method:

.. code-block:: python
   :emphasize-lines: 9,10

  @schema
  class Neuron(dj.Imported):
      definition = """
      -> Session
      ---
      activity:  longblob    # electric activity of the neuron
      """

      def _make_tuples(self, key):    # _make_tuples takes a single argument key
          print(key)  # let's look a the key content

Here we have added a very basic ``_make_tuples`` method to the class ``Neuron``. It turns out
that ``_make_tuples`` takes in a single argument ``key``, so we go ahead and let ``_make_tuples``
print out the content of the ``key`` argument. Let's now create a new instance and call ``populate``
again:

.. code-block:: python

  >>> neuron = Neuron()
  >>> neuron.populate()
  {'mouse_id': 0, 'session_date': datetime.date(2017, 5, 15)}
  {'mouse_id': 0, 'session_date': datetime.date(2017, 5, 19)}
  {'mouse_id': 5, 'session_date': datetime.date(2017, 1, 5)}
  {'mouse_id': 100, 'session_date': datetime.date(2017, 5, 25)}

This time the call to ``populate`` did not thrown an error but rather printed out four dictionaries.
Staring at these four dictionaries, you might have noticed that these are the primary key values
(``mouse_id`` and ``session_date``) of the four entries from the ``Session`` table!

.. code-block:: python
  
  >>> session
  *mouse_id    *session_date  experiment_set experimenter
  +----------+ +------------+ +------------+ +------------+
  0            2017-05-15     0              Edgar Walker
  0            2017-05-19     0              Edgar Walker
  5            2017-01-05     1              Fabian Sinz
  100          2017-05-25     1              Jake Reimer
   (4 tuples)

So what's going on here? When you call ``populate`` method of a table, this triggers DataJoint to
lookup all the tables that the target table depends on (i.e. ``Session`` table for ``Neuron``),
and for each possible combination of entries in the dependent (or parent) tables, ``populate``
extracts the primary key values and call the ``_make_tuples`` method.

In the case of the ``Neuron`` table, the ``Neuron`` table depends only on ``Session`` table,
and therefore ``populate`` method went through all entries of ``Session`` and called the ``_make_tuples``
for each entry in ``Session``, passing in the primary key values as ``key`` argument!

So what is this all good for? We can use the fact that the ``populate`` calls ``_make_tuples`` for
every combination of parent tables for ``Neuron`` to automatically visit all ``Session`` and load
the neuron data for each session and insert the loaded data into the table! Let's take a look
at what that implementation might be like.

Implementing ``_make_tuples``
-----------------------------
Recall that we wanted to load the neuron activity data from each recorded ``Session`` into the
``Neuron`` table. We can now achieve that by implementing ``_make_tuples`` method like the following!

.. code-block:: python

  @schema
  class Neuron(dj.Imported):
      definition = """
      -> Session
      ---
      activity:  longblob    # electric activity of the neuron
      """

      def _make_tuples(self, key):
         # use key dictionary to determine the data file path
         data_file = "/path/to/data/data_{mouse_id}_{session_date}.npy".format(**key)

         # load the data
         data = np.load(data_file)

         # add the loaded data as the "activity" column
         key['activity'] = data

         # insert the key into self
         self.insert1(key)

Let's now take a look a the content of ``_make_tuples`` one step at a time.

.. code-block:: python
   :emphasize-lines: 2,3

      def _make_tuples(self, key):
         # use key dictionary to determine the data file path
         data_file = "/path/to/data/data_{mouse_id}_{session_date}.npy".format(**key)

         # load the data
         data = np.load(data_file)

         # add the loaded data as the "activity" column
         key['activity'] = data

         # insert the key into self
         self.insert1(key)

First of all, we use the passed in ``key`` dictionary containing the ``mouse_id`` and ``session_date``
of a single session to determine the path to the neuron data file recorded in that particular session.
We use the fact that each recoding files are named as ``data_{mouse_id}_{session_date}.npy``,
and substitute in the specific session's values to get the file name.

.. note::
  If you are working on Windows, note that you would have to use backslashes ``\`` in place
  of the forward slashes to separete folder names.

.. code-block:: python
   :emphasize-lines: 5,6

      def _make_tuples(self, key):
         # use key dictionary to determine the data file path
         data_file = "/path/to/data/data_{mouse_id}_{session_date}.npy".format(**key)

         # load the data
         data = np.load(data_file)

         # add the loaded data as the "activity" column
         key['activity'] = data

         # insert the key into self
         self.insert1(key)

We then load the data from the ``.npy`` data file, getting a NumPy array that contains the
recorded neuron's activity from that session.


.. code-block:: python
   :emphasize-lines: 8,9

      def _make_tuples(self, key):
         # use key dictionary to determine the data file path
         data_file = "/path/to/data/data_{mouse_id}_{session_date}.npy".format(**key)

         # load the data
         data = np.load(data_file)

         # add the loaded data as the "activity" column
         key['activity'] = data

         # insert the key into self
         self.insert1(key)

The loaded NumPy array data is then assigned to the ``key`` dictionary under attribute name
``activity``. Recall that this is the non-primary key ``longblob`` field that we added to
the ``Neuron`` table to store the recorded neuron's electric activity. After adding this 
attribute, the ``key`` dictionary should now contain three attributes: ``mouse_id``, ``session_date``,
and ``activity``, with values of the first two specifying a specific ``Neuron`` entry and the
value of the ``activity`` holding the recorded activity for that neuron.


.. code-block:: python
   :emphasize-lines: 11,12

      def _make_tuples(self, key):
         # use key dictionary to determine the data file path
         data_file = "/path/to/data/data_{mouse_id}_{session_date}.npy".format(**key)

         # load the data
         data = np.load(data_file)

         # add the loaded data as the "activity" column
         key['activity'] = data

         # insert the key into self
         self.insert1(key)

We then finally insert this dictionary containing a single neuron's activity into ``self``, which
of course points to ``Neuron``! With this implementation of ``_make_tuples``, when the ``populate``
method is called, ``Neuron`` will be **populated** with recorded neuron's activity from each 
recording session, one a time as desired!

Populating ``Neuron`` table
---------------------------

Go ahead and redefine the ``Neuron`` class with the updated ``_make_tuples`` method as given
above. And now let's call the ``populate`` method on a new instance of ``Neuron`` again!

.. code


Go ahead redefine your 
