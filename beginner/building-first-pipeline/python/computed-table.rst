Computation in data pipeline
============================

Welcome to the last (but certainly not the least!) section of the tutorial! Now that we
have some recorded neural data imported into a table (``Neuron``), we are going to perform
some computations and processing, and look at how we can store these results naturally into
tables. In doing so, we are going to meet two remaining major table tiers:
lookup table (``dj.Lookup``) and computed table (``dj.Computed``).

Performing computation on data
------------------------------
Now we have the "raw" electric activities from neurons, we would like to detect spikes automatically.
Before we tackle this challenge, let's first get a better idea about our data by computing a few
statistics on the data such as mean and standard deviation of the electric activity.

Defining computed tables
^^^^^^^^^^^^^^^^^^^^^^^^

A crticial feature of a data pipeline is that not only the raw data (i.e. entered manually or imported
from external source) but also the processed data and computation results reside in the same data
pipeline. A **computed table** is defined by specifying the computation to be performed on data
found in other table(s), and the results are stored inside the table itself.

Just like the imported tables (``dj.Imported``), computed tables (``dj.Computed``) provide the
``populate`` method and ``_make_tuples`` method, and therefore provides us with a mechanism to
perform computation on every combination of parent/depended tables!

Let's now define our first computed table ``ActivityStatistics`` that **computes** the statistics
of electric activity **for each neuron in ``Neuron``**.


.. code-block:: python

  @schema
  class ActivityStatistics(dj.Computed):
      definition = """
      -> Neuron
      ---
      mean: float    # mean activity
      stdev: float   # standard deviation of activity
      max: float     # maximum activity
      """

      def _make_tuples(self, key):
          activity = (Neuron() & key).fetch1['activity']    # fetch activity as NumPy array

          # compute various statistics on activity
          key['mean'] = activity.mean()   # compute mean 
          key['stdev'] = activity.std()   # compute standard deviation
          key['max'] = activity.max()     # compute max
          self.insert1(key)
          print('Computed statistics for mouse_id {mouse_id} session_date {session_date}'.format(**key))

As usual, let's take a look at it step by step!

.. code-block:: python
  :emphasize-lines: 2

  @schema
  class ActivityStatistics(dj.Computed):
      definition = """
      -> Neuron
      ---
      mean: float    # mean activity
      stdev: float   # standard deviation of activity
      max: float     # maximum activity
      """

      def _make_tuples(self, key):
          activity = (Neuron() & key).fetch1['activity']    # fetch activity as NumPy array

          # compute various statistics on activity
          key['mean'] = activity.mean()   # compute mean 
          key['stdev'] = activity.std()   # compute standard deviation
          key['max'] = activity.max()     # compute max
          self.insert1(key)
          print('Computed statistics for mouse_id {mouse_id} session_date {session_date}'.format(**key))

As you might have guessed, you subclass from ``dj.Computed`` to defined a computed table in DataJoint.

.. code-block:: python
  :emphasize-lines: 2

  @schema
  class ActivityStatistics(dj.Computed):
      definition = """
      -> Neuron
      ---
      mean: float    # mean activity
      stdev: float   # standard deviation of activity
      max: float     # maximum activity
      """

      def _make_tuples(self, key):
          activity = (Neuron() & key).fetch1['activity']    # fetch activity as NumPy array

          # compute various statistics on activity
          key['mean'] = activity.mean()   # compute mean 
          key['stdev'] = activity.std()   # compute standard deviation
          key['max'] = activity.max()     # compute max
          self.insert1(key)
          print('Computed statistics for mouse_id {mouse_id} session_date {session_date}'.format(**key))

.. code-block:: python
  :emphasize-lines: 3-7

Here each ``ActivityStatistics`` entry **depends** on ``Neuron``. Because the ``ActivityStatistics``
table does not define any additional primary key attribute (i.e. no other attribute entries above 
``---`` separator), each row in the ``ActivityStatistics`` table is uniquely identified by a 
single neuron in the ``Neuron`` table. Each entry in the ``ActivityStatistics`` table has 
non-primary key attributes ``mean``, ``stdev`` and ``max`` to hold the mean, standard deviation
and maximum value of the electric activity, respectively.

.. code-block:: python
  :emphasize-lines: 2

  @schema
  class ActivityStatistics(dj.Computed):
      definition = """
      -> Neuron
      ---
      mean: float    # mean activity
      stdev: float   # standard deviation of activity
      max: float     # maximum activity
      """

      def _make_tuples(self, key):
          activity = (Neuron() & key).fetch1['activity']    # fetch activity as NumPy array

          # compute various statistics on activity
          key['mean'] = activity.mean()   # compute mean 
          key['stdev'] = activity.std()   # compute standard deviation
          key['max'] = activity.max()     # compute max
          self.insert1(key)
          print('Computed statistics for mouse_id {mouse_id} session_date {session_date}'.format(**key))

Just like imported table (``dj.Imported``), computed tables are equipped with ``populate`` method
which would call the ``_make_tuples`` for every combination of dependent/parent tables. In this case,
``ActivityStatistics``'s ``_make_tuples`` will be called for every neuron in the ``Neuron`` table. 

Here, for each neuron in the ``Neuron`` table (pointed to by ``key``), we  1) get the value of column 
``activity`` storing the neuron's electric activity as NumPy array, 2) compute various statistics and
store the values into the ``key`` dictionary and 3) insert the dictionary into self (``ActivityStatistics``).

.. note::
  ``fetch`` method will always return a list of values even if there is only one element. When you know
  that there is only going to be one entry, you can get the attribute value directly by using
  ``fetch1`` instead, as was done here.

With this computation defined, we can trigger activity statistics to be computed for all entries in
``Neuron`` by simply instantiating and calling ``populate`` method on ``ActivityStatistics``:

.. code-block:: python

  >>> avg = ActivityStatistics()
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

Great! We just successfully computed various neuronal activity statistics for all neurons in the
``Neuron`` table with a single method call to ``populate``. Computation couldn't really be 
easier than that!

Detecting spikes from neural activity
-------------------------------------

Now we have a better idea of our neuronal activity data, let's try performing the more challenging
computation - the spike detection. As you may know, spike detection is a very challenging (and 
exciting) subject and is a very active area of research!
However, Rather than attempting to implement the state-of-the-art spike detection,
we are going to implement a very simple algorithm where we register a "spike" 
every time the activity **rises above** a certain **threshold** value.

Importantly, this means that the result of our computation (i.e. detected spikes) will depend
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

Now that we have defined ``SpikeDetectionParam``, let's go ahead and define the computed table for
spike detection and call it ``SpikeDetection``!

.. code-block:: python

  @schema
  class SpikeDetection(dj.Computed):
      definition = """
      -> Neuron
      -> SpikeDetectionParam
      ---
      spikes: longblob     # detected spikes
      count: int           # total number of detected spikes
      """

      def _make_tuples(self, key):
          activity = (Neuron() & key).fetch1['activity']
          threshold = (SpikeDetectionParam() & key).fetch1['threshold']

          above_thrs = (activity > threshold).astype(np.int)   # find activity above threshold
          rising = (np.diff(above_thrs) > 0).astype(np.int)   # find rising edge of crossing threshold
          spikes = p.hstack((0, rising))    # prepend 0 to account for shortening due to np.diff
          count = spikes.sum()   # compute total spike counts

          # save results and insert
          key['spikes'] = spikes
          key['count'] = count
          self.insert1(key)

          print('Detected {} spikes for mouse_id {} session_date {} using threshold={:0.2f}'.format(
                count, key['mouse_id'], key['session_date'], threshold)
