Computation in data pipeline
============================

Welcome to the last (but certainly not the least exciting) section of the tutorial! Now that we
have some recorded neural data imported into a table (``Neuron``), we are going to look at defining
a table that will automatically perform and store results of data processing/computation on
data from other tables. In doing so, we are going to meet two remaining major table tiers:
lookup table (``dj.Lookup``) and computed table (``dj.Computed``).

Detecting spikes in electric activity
-------------------------------------
Now we have the "raw" electric activities from neurons, we would like to detect spikes in the activity
automatically. To do this, we are going implement a very simple-mided threshold based spike detection
algorithm. But before we delve far into the implementation, let's step back and think about **how**
this computation should take place and **where** the results would be stored. The answer lies in
understanding "computed" tables.

Defining computed tables
------------------------

A crticial feature of a data pipeline is that not only the raw data (i.e. entered manually or imported
from external source) but also the processed data and computation results reside in the same data
pipeline. A **computed tables** are defined by specifying the computation to be performed on data
found in other table(s), and the results are stored inside the table itself.

Interestingly a computed table (``dj.Computed``) makes use of the same ``populate`` and ``_make_tuples``
logic that were used in imported tables (``dj.Imported``). Before tackling the spike detection algorithm,
let's first try a simpler computation where we calculate the average activity of **each ``Neuron``**,
and store the results in a table called ``AverageActivity``.

.. code-block:: python

  @schema
  class AverageActivity(dj.Computed):
      definition = """
      -> Neuron
      ---
      avg_activity: float    # average electric activity
      """

      def _make_tuples(self, key):
          activity = (Neuron() & key).fetch1['activity']    # fetch activity as NumPy array
          key['avg_activity'] = activity.mean()
          self.insert1(key)
          print('Average activity computed for mouse_id {mouse_id} \
                 session_date {session_date}'.format(**key))

As usual, let's take a look at it step by step!

.. code-block:: python
  :emphasize-lines: 2

  @schema
  class AverageActivity(dj.Computed):
      definition = """
      -> Neuron
      ---
      avg_activity: float    # average electric activity
      """

      def _make_tuples(self, key):
          activity = (Neuron() & key).fetch1['activity']    # fetch activity as NumPy array
          key['avg_activity'] = activity.mean()
          self.insert1(key)
          print('Average activity computed for mouse_id {mouse_id} \
                 session_date {session_date}'.format(**key))

As you might have guessed, you subclass from ``dj.Computed`` to defined a computed table in DataJoint.

.. code-block:: python
  :emphasize-lines: 3,4,5

  @schema
  class AverageActivity(dj.Computed):
      definition = """
      -> Neuron
      ---
      avg_activity: float    # average electric activity
      """

      def _make_tuples(self, key):
          activity = (Neuron() & key).fetch1['activity']    # fetch activity as NumPy array
          key['avg_activity'] = activity.mean()
          self.insert1(key)
          print('Average activity computed for mouse_id {mouse_id} \
                 session_date {session_date}'.format(**key))

Here each ``AverageActivity`` entry **depends** on ``Neuron``. Because ``AverageActivity`` defines
no additional primary key attribute (no other attribute entries above ``---`` separator), each
``AverageActivity`` is uniquely identified by a single ``Neuron``. Each entry of ``AverageActivity``
then defines a float value ``avg_activity`` which will store the computed averate activity of the
neuron.


.. code-block:: python
  :emphasize-lines: 7,8,9,10

  @schema
  class AverageActivity(dj.Computed):
      definition = """
      -> Neuron
      ---
      avg_activity: float    # average electric activity
      """

      def _make_tuples(self, key):
          activity = (Neuron() & key).fetch1['activity']    # fetch activity as NumPy array
          key['avg_activity'] = activity.mean()    # compute mean activity
          self.insert1(key)   # insert result into self
          print('Average activity computed for mouse_id {mouse_id} \
                 session_date {session_date}'.format(**key))

Just like imported table (``dj.Imported``), computed tables are equipped with ``populate`` method
which would call the ``_make_tuples`` for every combination of dependent/parent tables. In this case,
``AverageActivity``'s ``_make_tuples`` will be called for every entry in the ``Neuron`` table. 

Here, for each ``Neuron`` (as pointed to by ``key``), we  1) get the value of column ``activity`` storing
the neuron's electric activity as NumPy array, 2) compute the mean and store as ``avg_activity`` field
in the ``key`` dictionary, and 3) insert the dictionary into self (``AverageActivity``).

.. note::
  ``fetch`` method will always return a list of values even if there is only one element. When you know
  that there is only going to be one entry, you can get the attribute value directly by using
  ``fetch1`` instead, as was done here.

With this computation defined, we can trigger average activity to be computed for all entries in
``Neuron`` by simply instantiating and calling ``populate`` method on ``AverageActivity``:

.. code-block:: python

  >>> avg = AverageActivity()
  >>> avg
  *mouse_id    *session_date  avg_activity
  +----------+ +------------+ +------------+

   (0 tuples)

  >>> avg.populate()   # trigger populate
  Average activity computed for mouse_id 0 session_date 2017-05-15
  Average activity computed for mouse_id 0 session_date 2017-05-19
  Average activity computed for mouse_id 5 session_date 2017-01-05
  Average activity computed for mouse_id 100 session_date 2017-05-25
  Average activity computed for mouse_id 100 session_date 2017-06-01

  >>> avg
  *mouse_id    *session_date  avg_activity
  +----------+ +------------+ +------------+
  0            2017-05-15     0.363763
  0            2017-05-19     0.365316
  5            2017-01-05     0.479287
  100          2017-05-25     0.531464
  100          2017-06-01     0.352429
   (5 tuples)

Great! We were able to the average activity computed for each neuron with a single method call!

Detecting spikes from neural activity
-------------------------------------

Now let's try performing somewhat more challenging computation and detect spikes from the 
electric activities of neurons. It turns out that this is a very challenging and exciting topic
with a lot of research done on it. However, we are going to implement a very simple algorithm
where we register a "spike" to be where the activity **rises above** a certain **threshold**.

Notice that this means that the result of our computation (i.e. detected spikes) could depend
a lot on the chosen value of the threshold, and we would like to be able to try a few
different value of threshold to see what works well. In other words, we would like to be able
to run the spike detection algorithm with few different values of **threshold** and compare
the results side-by-side.

This can actually be achieve rather easily by preparing a **lookup table** to store different
values of computation paramters (i.e. threshold values), and compute spikes for **every
combination of neurons and parameter value set**.

Defining Lookup tables
^^^^^^^^^^^^^^^^^^^^^^

Let's go ahead and define a lookup table called ``SpikeDetectionParam`` to contain the
parameters for spike detection, namely the threshold value.
As you might have guessed, you can define a lookup
table by subclassing ``dj.Lookup``. Lookup table is almost identical to a manual table
(``dj.Manual``) but signifies that this table contains values like parameters for computation.

.. code-block:: python

  @schema
  class SpikeDetectionParam(dj.Lookup):
      definition = """
      sdp_id: int      # unique id for spike detection parameter set
      ---
      threshold: float   # threshold for spike detection
      """

.. note::
  Notice that we used a field ``sdp_id`` to serve as the primary key for the ``SpikeDetectionParam``
  rathern than using ``threshold`` is the primary key, despite the fact that ``threshold`` is the
  only attribute of interset in this table. This is because ``threshold`` is of data type float
  and exact comparison is difficult for float values. In general, it is recommended that you avoid 
  using float data type attribute in your primary key.

Defining ``SpikeDetection`` table
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Now that we have defined ``SpikeDetectionParam``, let's go ahead and define the computed table






