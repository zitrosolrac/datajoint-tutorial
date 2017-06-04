Querying and fetching data
==========================

Now that we covered how to insert data into the table, you might be wondering "how do we retrieve the
data from the table?" In this section, we will explore not only how to fetch the data, but how to 
narrow down and only fetch the data you want! But first thing first, let's start with the simplest -
let's fetch all the data in the table.

Fetching all data
-----------------

You can fetch all data inside a table by simply calling ``fetch`` method on the table object:

.. code-block:: python
  
  data = mouse.fetch()    # this retrieves all data in the table

By default the data is retrieved as numpy structured array:

.. code-block:: python

  >>> data
  array([(  0, datetime.date(2017, 3, 1), 'M'),
       (  1, datetime.date(2016, 11, 19), 'M'),
       (  2, datetime.date(2016, 11, 20), 'U'),
       (  5, datetime.date(2016, 12, 25), 'F'),
       ( 10, datetime.date(2017, 1, 1), 'F'),
       ( 11, datetime.date(2017, 1, 3), 'F'),
       (100, datetime.date(2017, 5, 12), 'F')],
      dtype=[('mouse_id', '<i8'), ('dob', 'O'), ('gender', 'O')])

Alternatively, you can retrieve the data as a list of dictionaries:

.. code-block:: python

  >>> mouse.fetch(as_dict=True)   # retrieve all data as list of dictionaries
  [OrderedDict([('mouse_id', 0),
              ('dob', datetime.date(2017, 3, 1)),
              ('gender', 'M')]),
 OrderedDict([('mouse_id', 1),
              ('dob', datetime.date(2016, 11, 19)),
              ('gender', 'M')]),

 ...output truncated...

 OrderedDict([('mouse_id', 100),
              ('dob', datetime.date(2017, 5, 12)),
              ('gender', 'F')])]

Fetching specific attributes
----------------------------
If you are only interested in values from a specific attribute (columns) of the table,
you can do so by using ``[]`` notation. Let's try fetching only the date of birth of all mice.

.. code-block:: python

  >>> mouse.fetch['dob']
  array([datetime.date(2017, 3, 1), datetime.date(2016, 11, 19),
         datetime.date(2016, 11, 20), datetime.date(2016, 12, 25),
         datetime.date(2017, 1, 1), datetime.date(2017, 1, 3),
         datetime.date(2017, 5, 12)], dtype=object)

This can also be used to fetch multiple attributes separately:

.. code-block:: python

  >>> gender, ids = mouse.fetch['gender', 'mouse_id']
  >>> gender
  array(['M', 'M', 'U', 'F', 'F', 'F', 'F'], dtype=object)
  >>> dob
  array([  0,   1,   2,   5,  10,  11, 100])

Now that you have learnt how to insert and then fetch data from a table, you could already start to use 
tables at least as your simple storage of your data. However, true power of DataJoint comes about when you 
start combining these operations with DataJoint's simple yet very powerful **query** language.

Querying Data
-------------

The process of **querying** data refers to the searching and narrowing down of the existing data to find
exactly what you need. Rather than retrieving all data and then writing your own parser to just retrieve
data you are interested, you can use DataJoint's query language to narrow down data first and then only
retrieve what you need. Let's take a look, using our ``Mouse`` table as the example.

At the moment, the ``Mouse`` table contains a couple entries:

.. code-block:: python

  >>> mouse
  *mouse_id    dob            gender
  +----------+ +------------+ +--------+
  0            2017-03-01     M
  1            2016-11-19     M
  2            2016-11-20     U
  5            2016-12-25     F
  10           2017-01-01     F
  11           2017-01-03     F
  100          2017-05-12     F
   (7 tuples)

.. note::
  Before moving on, feel free to add more entries into your table using any one of insert methods
  that was covered in :doc:`inserting-data`.

Restricting by attribute value
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Let's start with a very simple query, looking for an entry with a specific value of an attribute. We
can find information about mouse with `mouse_id = 0` as follows:

.. code-block:: python

  >>> mouse & 'mouse_id = 0'
  *mouse_id    dob            gender
  +----------+ +------------+ +--------+
  0            2017-03-01     M
   (1 tuples)

Let's take a closer look at what just happened. Using the table instance ``mouse``, we used the ``&`` (restriction)
operation to **restrict** down to entries that matches the **restriction** ``mouse_id = 0``. Sincere there is only
one mouse with ``mouse_id = 0`` (recall that ``mouse_id`` is the primary key), we get back only one entry.

Now, let's say we want to list only male mice. This is easily achieved with:

.. code-block:: python

  >>> mouse & 'gender = "M"'
  *mouse_id    dob            gender
  +----------+ +------------+ +--------+
  0            2017-03-01     M
  1            2016-11-19     M
   (2 tuples)

Notice that ``"M"`` was surrounded by double quotes (``"``) because the value was non-numeric.

Using inequality in restriction
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

We can also use inequality in our query, for eample to serach all mouse born after Jan 1, 2017:

.. code-block:: python

  >>> mouse & 'dob > "2017-01-01"'
  *mouse_id    dob            gender
  +----------+ +------------+ +--------+
  0            2017-03-01     M
  11           2017-01-03     F
  100          2017-05-12     F
   (3 tuples)

Or you can find all mouse that are **not** male:

.. code-block:: python
  
  >>> mouse & 'gender != "M"'
  *mouse_id    dob            gender
  +----------+ +------------+ +--------+
  2            2016-11-20     U
  5            2016-12-25     F
  10           2017-01-01     F
  11           2017-01-03     F
  100          2017-05-12     F
   (5 tuples)

Combining restrictions
^^^^^^^^^^^^^^^^^^^^^^

You can also *combine* multiple restrictions to form more complex query:

.. code-block:: python

  >>> mouse & 'dob > "2017-01-01"' & 'gender = "M"'  # all male mice born after Jan 1, 2017
   *mouse_id    dob            gender
  +----------+ +------------+ +--------+
  0            2017-03-01     M
   (1 tuples)

Restricting by a dictionary
^^^^^^^^^^^^^^^^^^^^^^^^^^^
If you are only looking for equivalence of attribute values (i.e. only use ``=`` in restriction),
you can also use dictionary in restriction.

For example, the earlier query looking of

.. code-block:: python

  >>> mouse & 'gender = "M"'
  *mouse_id    dob            gender
  +----------+ +------------+ +--------+
  0            2017-03-01     M
  1            2016-11-19     M
   (2 tuples)
 
can also be achieved using dictionary as follows:

.. code-block:: python

  >>> r = {
        'gender': 'M'
      }
  >>> mouse & r
  *mouse_id    dob            gender
  +----------+ +------------+ +--------+
  0            2017-03-01     M
  1            2016-11-19     M
   (2 tuples)

Restricting with dictionary come in particulary handy when restricting by multiple attribute values.

Fetching query result
---------------------

Once you are happy with your query, you can fetch only the matching entries by calling fetch on the query
result:

.. code-block:: python

  >>> (mouse & 'dob > "2017-01-01"' & 'gender = "M"').fetch()
  array([(0, datetime.date(2017, 3, 1), 'M')],
      dtype=[('mouse_id', '<i8'), ('dob', 'O'), ('gender', 'O')]) 

Not only does querying with DataJoint makes retrieving certain subsets of data easier, it also helps you
but avoiding unnecessary data transfer between the database server and your computer. While you are
forming and previewing queries, the query processing is actually performed by the database server, 
and only minimal data (if any) is transferred between the database server and your computer.

When you call ``fetch`` on the query result, only the relevant data is transfered, thus potentially cutting down
the amount of data that has to be transferred out of database server to your local machine. Not only does
it save space on your machine, but can also significantly reduce data transfer speed and also help to reduce
load on the database server.

What's next?
------------
In this section, we learned how to fetch data from the table using the ``fetch`` method. We also met our
first query operation, ``&`` (restriction) and learned how it can be used to narrow down your query
results. As you progress through the tutorials and create more tables, you will learn additiona query
operations and how to combine them into more powerful yet intuitive query.

In the :doc:`next section <child-table>`, we will move forward in our data pipeline creation by creating and **linking** addition
tables together.
