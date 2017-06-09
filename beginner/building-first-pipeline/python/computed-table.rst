Computation in data pipeline
============================

Welcome to the last (but certainly not the least!) section of the tutorial! Now that we
have the recorded neural activties imported into a table (``Neuron``), we are ready to 
perform computations on this data, and store the computation results in to, you guessed 
it, a table! In doing so, we are going to meet two remaining major table tiers:
lookup table (``dj.Lookup``) and computed table (``dj.Computed``).

Computing statistics on neural activities
-----------------------------------------
Now we have the "raw" electric activities from neurons, let's say that we would like to 
detect spikes automatically. Before we tackle this challenge, let's first get a better idea about our data by computing a few statistics on the data such as mean and standard deviation 
of the electric activity.

Computed tables
^^^^^^^^^^^^^^^

A crticial feature of a data pipeline is that not only the raw data (i.e. entered manually 
or imported from external source) but also the processed data and computation results 
reside in the same data pipeline.
A **computed table** is created by subclassing ``dj.Computed`` and
1) defines a computation to be performed on data found in other table(s), and 
2) stores the results of this computation.

Just like the imported tables (``dj.Imported``), computed tables (``dj.Computed``) provide the
``populate`` method and ``_make_tuples`` method, and therefore provides us with a mechanism to
perform computation on every combination of parent/depended tables!

Computing neuron activity statistics
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Let's now define our first computed table that **computes** the statistics
of electric activity **for each neuron in ``Neuron``** and call it``ActivityStatistics``.


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
  :emphasize-lines: 3-9

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

Here each ``ActivityStatistics`` entry **depends** on a ``Neuron``. Because the ``ActivityStatistics``
table does not define any additional primary key attribute (i.e. no other attribute entries above 
``---`` separator), each row in the ``ActivityStatistics`` table is uniquely identified by a 
single neuron in the ``Neuron`` table. Each entry in the ``ActivityStatistics`` table will have
non-primary key attributes ``mean``, ``stdev`` and ``max`` to hold the mean, standard deviation
and maximum value of the electric activity, respectively.

.. code-block:: python
  :emphasize-lines: 12-19

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

As mentioned earlier, computed tables are equipped with ``populate`` method which would call 
the ``_make_tuples`` for every combination of dependent/parent tables. In this case, 
``ActivityStatistics``'s ``_make_tuples`` will be called for every neuron in the 
``Neuron`` table.

Here, for each neuron in the ``Neuron`` table (pointed to by ``key``), we  1) get the value of column 
``activity`` storing the neuron's electric activity as NumPy array, 2) compute various statistics and
store the values into the ``key`` dictionary and 3) insert the dictionary into self (``ActivityStatistics``).
We also print out a message for every completed call to ``_make_tuples``.

.. note::
  ``fetch`` method will always return a list of values even if there is only one element. When you know
  that there is only going to be one entry, you can get the attribute value directly by using
  ``fetch1`` instead, as was done here.

With this computation defined, we can trigger activity statistics to be computed for all entries in
``Neuron`` by simply instantiating and calling ``populate`` method on ``ActivityStatistics``:

.. code-block:: python

  >>> stats = ActivityStatistics()
  >>> stats
  *mouse_id    *session_date  mean     stdev     max
  +----------+ +------------+ +------+ +-------+ +-----+

   (0 tuples)

  >>> stats.populate()  # trigger population
  Computed statistics for mouse_id 0 session_date 2017-05-15
  Computed statistics for mouse_id 0 session_date 2017-05-19
  Computed statistics for mouse_id 5 session_date 2017-01-05
  Computed statistics for mouse_id 100 session_date 2017-05-25
  Computed statistics for mouse_id 100 session_date 2017-06-01

Now let's take a look at the content of the ``ActivityStatistics`` table:

.. code-block:: python

  >>> stats
  *mouse_id    *session_date  mean          stdev        max
  +----------+ +------------+ +-----------+ +----------+ +---------+
  0            2017-05-15     0.207357      0.400867     2.48161
  0            2017-05-19     0.13274       0.291462     1.82805
  5            2017-01-05     0.0891786     0.236412     1.37389
  100          2017-05-25     0.21907       0.328783     1.76383
  100          2017-06-01     0.0873266     0.237858     1.32454
   (5 tuples)

Great! We have successfully computed various neuronal activity statistics for all neurons 
in the ``Neuron`` table with a single method call to ``populate``. 
Computation couldn't really be easier than that!


Detecting spikes from neural activity
-------------------------------------

Now we have a better idea of our neuronal activity data, let's try tacking the more challenging
computation - the spike detection. As you may know, spike detection is a very challenging 
(and exciting) subject and is a very active area of research!
However, rather than attempting to implement the state-of-the-art spike detection algorithm,
we are going to implement a very simple algorithm where we register a "spike" 
every time the activity **rises above** a certain **threshold** value.

Importantly, this means that the result of our computation (i.e. detected spikes) will depend
a lot on the chosen value of the **threshold**, and we would like to be able to try a few
different value of threshold to see what works well. In other words, we would like to be able
to run the spike detection algorithm with a few different values of the **threshold** and 
compare the results side-by-side.

Thankfully, this can be achieved rather straightforwardly by preparing a **lookup table**
to store different values of computation paramters (i.e. threshold values), and compute spikes for **every combination of neurons and parameter value set**.

Defining Lookup tables
^^^^^^^^^^^^^^^^^^^^^^

Let's go ahead and define a lookup table called ``SpikeDetectionParam`` to contain the
parameters for spike detection, namely the threshold value.
As you might have guessed, you define a lookup table by subclassing ``dj.Lookup``.
Lookup table is almost identical to a manual table
(``dj.Manual``) but signifies that this table contains values like parameters for computation,
rather than raw data.

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
spike detection and call it ``Spikes``! 

.. note::
  It's usually a good diea to call a computed table
  based on what would be the results of the computation rather than naming it based on the
  computation process (i.e. so ``Spikes`` rather than ``SpikeDetection``). 
  This would make sense if you consider the fact that the table will be housing the 
  results of the computation, here the detected neuronal **spikes**.

.. code-block:: python

  @schema
  class Spikes(dj.Computed):
      definition = """
      -> Neuron
      -> SpikeDetectionParam
      ---
      spikes: longblob     # detected spikes
      count: int           # total number of detected spikes
      """

      def _make_tuples(self, key):
          print('Populating for: ', key)

          activity = (Neuron() & key).fetch1['activity']
          threshold = (SpikeDetectionParam() & key).fetch1['threshold']

          above_thrs = (activity > threshold).astype(np.int)   # find activity above threshold
          rising = (np.diff(above_thrs) > 0).astype(np.int)   # find rising edge of crossing threshold
          spikes = np.hstack((0, rising))    # prepend 0 to account for shortening due to np.diff
          count = spikes.sum()   # compute total spike counts
          print('Detected {} spikes!\n'.format(count))

          # save results and insert
          key['spikes'] = spikes
          key['count'] = count
          self.insert1(key)

Alright, let's go through this code step-by-step, first focusing on the definition!


.. code-block:: python
  :emphasize-lines: 4-5

  @schema
  class Spikes(dj.Computed):
      definition = """
      -> Neuron
      -> SpikeDetectionParam
      ---
      spikes: longblob     # detected spikes
      count: int           # total number of detected spikes
      """

Notice that the ``Spikes`` table **depends on both ``Neuron`` and ``SpikeDetectionParam``**!
What does this mean? This means that each entry (detected spikes) in the ``Spikes`` table
is uniquely identified not only by the identify of a neuron (from ``Neuron``) but by the
combination of the neuron identity and **the particular spike detection parameter**
(from ``SpikeDetectionParam``). As you will see, this allows for this table to house
results of spike detection under more than one values for the parameter (i.e. threshold)!

.. code-block:: python
  :emphasize-lines: 7-8

  @schema
  class Spikes(dj.Computed):
      definition = """
      -> Neuron
      -> SpikeDetectionParam
      ---
      spikes: longblob     # detected spikes
      count: int           # total number of detected spikes
      """

As the non-primary-key attributes, ``Spikes`` will contain both the detected ``spikes``
as an array of 0's and 1's with 1's at the position of a spike, and the total ``count`` 
of detected spikes.

Now let's move onto the mean of the computed table - ``_make_tuples``:

.. code-block:: python
  :emphasize-lines: 4-5

  def _make_tuples(self, key):
      print('Populating for: ', key)

      activity = (Neuron() & key).fetch1['activity']
      threshold = (SpikeDetectionParam() & key).fetch1['threshold']

      above_thrs = (activity > threshold).astype(np.int)   # find activity above threshold
      rising = (np.diff(above_thrs) > 0).astype(np.int)   # find rising edge of crossing threshold
      spikes = np.hstack((0, rising))    # prepend 0 to account for shortening due to np.diff

      count = spikes.sum()   # compute total spike counts
      print('Detected {} spikes!\n'.format(count))

      # save results and insert
      key['spikes'] = spikes
      key['count'] = count
      self.insert1(key)

One of the first thing we do in ``_make_tuples`` is to fetch relevant data from other tables.
This is a very standard practice when defining ``_make_tuples`` in computed tables, as was
also performed in the ``ActivityStatistics`` table. Here we fetch the neuron's electric
``activity`` NumPy array from the ``Neuron`` table, and the value of the ``threshold`` from
the ``SpikeDetectionParam`` table.


.. code-block:: python
  :emphasize-lines: 7-9

  def _make_tuples(self, key):
      print('Populating for: ', key)

      activity = (Neuron() & key).fetch1['activity']
      threshold = (SpikeDetectionParam() & key).fetch1['threshold']

      above_thrs = (activity > threshold).astype(np.int)   # find activity above threshold
      rising = (np.diff(above_thrs) > 0).astype(np.int)   # find rising edge of crossing threshold
      spikes = np.hstack((0, rising))    # prepend 0 to account for shortening due to np.diff
      
      count = spikes.sum()   # compute total spike counts
      print('Detected {} spikes!\n'.format(count))

      # save results and insert
      key['spikes'] = spikes
      key['count'] = count
      self.insert1(key)

Using ``activity`` and ``threshold``, we first find and label where ``activity`` value is
above the threshold. This returns an array of 0's and 1's where 1's corresponds to time bins
where neuron's activity was above the threshold, storing this as ``above_thrs``.

We then find out all the timebins at which the activity goes from 0 to 1, signifying times
at which the neuron's activity **raised above the threshold**, storing this into ``rising``! 
We then adjust this array so that it has the same length as the original ``activity``,
and store the result as our detected ``spikes``!


.. code-block:: python
  :emphasize-lines: 12

  def _make_tuples(self, key):
      print('Populating for: ', key)

      activity = (Neuron() & key).fetch1['activity']
      threshold = (SpikeDetectionParam() & key).fetch1['threshold']

      above_thrs = (activity > threshold).astype(np.int)   # find activity above threshold
      rising = (np.diff(above_thrs) > 0).astype(np.int)   # find rising edge of crossing threshold
      spikes = np.hstack((0, rising))    # prepend 0 to account for shortening due to np.diff

      count = spikes.sum()   # compute total spike counts
      print('Detected {} spikes!\n'.format(count))

      # save results and insert
      key['spikes'] = spikes
      key['count'] = count
      self.insert1(key)

We then compute the total detected spikes and print it out to the screen.

.. code-block:: python
  :emphasize-lines: 15-17

  def _make_tuples(self, key):
      print('Populating for: ', key)

      activity = (Neuron() & key).fetch1['activity']
      threshold = (SpikeDetectionParam() & key).fetch1['threshold']

      above_thrs = (activity > threshold).astype(np.int)   # find activity above threshold
      rising = (np.diff(above_thrs) > 0).astype(np.int)   # find rising edge of crossing threshold
      spikes = np.hstack((0, rising))    # prepend 0 to account for shortening due to np.diff

      count = spikes.sum()   # compute total spike counts
      print('Detected {} spikes!\n'.format(count))

      # save results and insert
      key['spikes'] = spikes
      key['count'] = count
      self.insert1(key)

Finally, we store the computed ``spikes`` and ``count`` by inserting into this (``Spieks``)
table!!

Populating ``Spikes``
^^^^^^^^^^^^^^^^^^^^^

Alright after our hard work putting implemeting the spike detection algorithm, it's time for
us to run it! Let's instantiate the ``Spikes`` table and ``populate`` it away!

.. code-block:: python

  >>> spikes = Spikes()
  >>> spikes     # preview the table
  *mouse_id    *session_date  *sdp_id    count     spikes
  +----------+ +------------+ +--------+ +-------+ +--------+

   (0 tuples)

  >>> spikes.populate()    # populate it away!
 
Sadly nothing seems to be happening. Why could this be the case? The answer lies in the
``SpikeDetectionParam`` table:

.. 


