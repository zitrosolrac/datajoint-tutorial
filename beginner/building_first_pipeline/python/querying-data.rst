Querying and fetching data
==========================

Now that we covered how to insert data into the table, you might be wondering how to retreive it. In this section, we will explore not only how to fetch the data, but how to 
narrow down and only fetch the data you want. But first let's start with the simplest case -
let's fetch all the data in the table.

Fetching all the data
---------------------

You can fetch all the data stored in a table by simply calling the ``fetch`` method on the table object:

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

Now that you have seen how to insert and then fetch data from a table, you could already start to use 
tables to store simple data. However, the true power of DataJoint comes about when you 
start combining these operations with DataJoint's simple yet very powerful **query** language.

Querying Data
-------------

The process of **querying** data refers to the searching and narrowing down of the existing data to find
exactly what you need. Rather than retrieving all data and then writing your own parsing function to extract the data you want, you can use DataJoint's query language to narrow things down first and then only
retrieve what you need. Let's take a look, using our ``Mouse`` table as the example.

At the moment, the ``Mouse`` table contains several entries:

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
can find information about the mouse with `mouse_id = 0` as follows:

.. code-block:: python

  >>> mouse & 'mouse_id = 0'
  *mouse_id    dob            gender
  +----------+ +------------+ +--------+
  0            2017-03-01     M
   (1 tuples)

Let's take a closer look at what just happened. Using the table instance ``mouse``, we used the ``&`` (restriction)
operation to **restrict** down to entries that matches the **restriction** ``mouse_id = 0``. Since there is only
one mouse with ``mouse_id = 0`` (recall that ``mouse_id`` is the primary key), we get back only one entry.

Now, let's say we want to list only male mice. This is easily done by:

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

We can also use inequalities in our query, for eample to search for all mice born after Jan 1, 2017:

.. code-block:: python

  >>> mouse & 'dob > "2017-01-01"'
  *mouse_id    dob            gender
  +----------+ +------------+ +--------+
  0            2017-03-01     M
  11           2017-01-03     F
  100          2017-05-12     F
   (3 tuples)

Or you can find all mice that are **not** male:

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

You can also *combine* multiple restrictions to form more complex queries:

.. code-block:: python

  >>> mouse & 'dob > "2017-01-01"' & 'gender = "M"'  # all male mice born after Jan 1, 2017
   *mouse_id    dob            gender
  +----------+ +------------+ +--------+
  0            2017-03-01     M
   (1 tuples)

Restricting by a dictionary
^^^^^^^^^^^^^^^^^^^^^^^^^^^
If you are only looking for an equivalence of attribute values (i.e. you only need to use ``=`` in the restriction),
you can also use a dictionary to restrict.

For example, the earlier query:

.. code-block:: python

  >>> mouse & 'gender = "M"'
  *mouse_id    dob            gender
  +----------+ +------------+ +--------+
  0            2017-03-01     M
  1            2016-11-19     M
   (2 tuples)
 
can also be achieved using a dictionary as follows:

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

Restricting with a dictionary comes in handy when you want to restrict by multiple attribute values.

Fetching query results
----------------------

Once you are happy with your query, you can fetch only the matching entries by calling fetch on the query
result:

.. code-block:: python

  >>> (mouse & 'dob > "2017-01-01"' & 'gender = "M"').fetch()
  array([(0, datetime.date(2017, 3, 1), 'M')],
      dtype=[('mouse_id', '<i8'), ('dob', 'O'), ('gender', 'O')]) 

Not only does querying with DataJoint makes retrieving certain subsets of data easier, it also helps you
avoid unnecessary data transfers between the database server and your computer. While you are
forming and previewing queries, the query processing is actually performed by the database server, 
and only minimal data (if any) is transferred between the database server and your computer.

When you call ``fetch`` on the query result, only the relevant data is transfered, thus potentially cutting down
the amount of data that has to be transferred out of the database server to your local machine. Not only does
it save space on your machine, but can also significantly reduce data transfer speed and also help to reduce
load on the database server.

What's next?
------------
In this section, we learned how to fetch data from the table using the ``fetch`` method. We also met our
first query operation, ``&`` (restriction) and learned how it can be used to narrow down your query
results. As you progress through the tutorials and create more tables, you will learn additional 
operations and how to combine them into more powerful yet intuitive queries.

In the :doc:`next section <child-table>`, we will move forward in our data pipeline creation by creating and **linking** additional
tables together.
