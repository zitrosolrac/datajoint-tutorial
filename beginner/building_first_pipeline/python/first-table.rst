Defining your first table
=========================

Every pipeline is composed of one or more **tables**. Each table represents a specific set of data. Most commonly
a table is a ``Manual`` table representing manually entered data (either by human or by automated data entry
system). A table always belongs to a **schema** which helps to organize tables into groups. By placing related
tables into one **schema** you can keep your data pipeline well structured.

.. note::

  This tutorial assumes that you already have a database server that you can connect to and that you have installed DataJoint
  for Python. If either of this is not true, be sure to checkout our :doc:`Getting Started Tutorial </setting-up/introduction>`
  first before proceeding with this tutorial!


Creating schema
---------------

Let's get started by import DataJoint and creating a new schema to define tables in. Open up an interactive
Python console and import ``datajoint``:

.. code-block:: python

  import datajoint as dj

Set up your connection to the database server.

.. code-block:: python

  dj.config['database.host'] = 'HOST_ADDRESS'
  dj.config['database.user'] = 'USER_NAME'
  dj.config['databas.password'] = 'PASSWORD'


.. note::
  If you need a review on how to connect to the database from DataJoint, checkout :doc:`/setting-up/datajoint-python`


Let's create our first schema called `tutorial`!


.. code-block:: python

  schema = dj.schema('tutorial', locals())

.. note::
  If you are connected to the tutorial database hosted by `DataJoint.io <https://datajoint.io>`_, you will have to prefix 
  all schema name with ``username_`` substituting in the username for the connection. For example, if your username is 
  ``johndoe``, then you would want to run the following command instead:

  .. code-block:: python
    
    schema = dj.schema('johndoe_tutorial', locals())

And that's it! We have just created a schema in the database, and now we can now begin creating tables inside of this schema!

.. note::
  Passing in ``locals()`` allows ``schema`` object to have access to all tables that you define in the local
  name space (e.g. interative session). This allows tables to refer to each other simply by their name. 


Defining table class
--------------------

Now we will use the ``schema`` object to create a new table. Since every thing about our mouse experiments
revolves around, well, mouse, let's create a table to enter and track all mouse we will work with:

.. code-block:: python

  @schema
  class Mouse(dj.Manual):
        definition = """
        mouse_id: int                  # unique mouse id
        ---
        dob: date                      # mouse date of birth
        gender: enum('M', 'F', 'U')    # gender of mouse - Male, Female, or Unknown/Unclassified
        """

and it turns out that this is enough to define a table! There is a lot going on here, so let's walk through
this code step by step.

Table classes
^^^^^^^^^^^^^
In DataJoint, tables are defined and accessed via **classes** inheriting from one of table superclasses
provided by DataJoint. Since we will be entering data about a new mice manually, we want to create a table
called "Mouse" as a manual table. You do so by defining a class called ``Mouse`` and inheriting from 
``dj.Manual`` super-class.

Table definition
^^^^^^^^^^^^^^^^
In addition to specifying the type or "tier" of the table (e.g. ``dj.Manual``), you need to define the
columns or **attributes** of the table. You do this by setting the ``definition`` to a string with
DataJoint data definition language. Let's take a closer look a the definition string here.

.. code-block:: python
   :emphasize-lines: 2

   definition = """
   # mouse
   mouse_id: int                  # unique mouse id
   ---
   dob: date                      # mouse date of birth
   gender: enum('M', 'F', 'U')    # gender of mouse - Male, Female, or Unknown/Unclassified
   """

Table comment
+++++++++++++

The very first line of the definition starts with a comment that describes what this table is about. Although
this is optional, leaving a meaninful comment here can be really helpful especially when you start defining
increasingly complex tables.

Attribute (column) definition
+++++++++++++++++++++++++++++

.. code-block:: python
   :emphasize-lines: 3

   definition = """
   # mouse
   mouse_id: int                  # unique mouse id
   ---
   dob: date                      # mouse date of birth
   gender: enum('M', 'F', 'U')    # gender of mouse - Male, Female, or Unknown/Unclassified
   """

In the definition string, you define the table's attributes (or columns) one at a time, each in
a separate line. The attribute definition takes the following format:

.. code-block:: python

  attribute_name :  data_type     # comment

As you probably can guess, the ``attribute_name`` is the name of the attribute. Separated by ``:``, you then
specify the **data type** of the attribute. This determines what kind of data can go into that attribute. 

For `mouse_id`, we have chosen type ``int`` which can hold integers between -2147483648 and 2147483647, with
the exact range depending on your database server. Since we don't expect to have that many mice, ``int`` is
a safe choice for holding numerical ID for the mouse. 

At the end of the definition, you can give a comment describing what this attribute stores. Although this is optional, it is strongly recommended that
you add a brief comment to help remind everyone (including yourself!) what that field is about. A good combination
of well thought out attribute name and a good comment can help make your table very readable.

Primary vs non-primary key attributes
+++++++++++++++++++++++++++++++++++++

.. code-block:: python
   :emphasize-lines: 4

   definition = """
   # mouse
   mouse_id: int                  # unique mouse id
   ---
   dob: date                      # mouse date of birth
   gender: enum('M', 'F', 'U')    # gender of mouse - Male, Female, or Unknown/Unclassified
   """

The ``---`` separator separates two types of attributes in the table. Above the line are your **primary-key
attributes**. These attributes are used to **uniquely identify** entries in the table. Within a table, the
combination of the primary-key attributes values **must be unique**. In this case, we only have on attribute
in the primary key (``mouse_id``) and thus every entry in the table must have distinct ``mouse_id``,
corresponding to actual mouse.

Below the ``---`` separator are **non primary-key attributes**. As you would guess, these are attributes
that are **not** used to identify the mouse. Typically, these attributes hold values that describe the entry
(in this case a mouse) identified by the primary-key (``mouse_id``).

Defining table in a schema
^^^^^^^^^^^^^^^^^^^^^^^^^^

Going back to the class ``Mouse`` definition, 

.. code-block:: python
  :emphasize-lines: 1

  @schema
  class Mouse(dj.Manual):
        definition = """
        mouse_id: int                  # unique mouse id
        ---
        dob: date                      # mouse date of birth
        gender: enum('M', 'F', 'U')    # gender of mouse - Male, Female, or Unknown/Unclassified
        """

Notice that we **decorate** the class ``Mouse`` with the ``schema`` object we created earlier. This decoration
tells DataJoint to create the table specified by the class (``Mouse``) inside the schema pointed to by the
``schema`` object (``dj_tutorial``).


Creating the table in the data pipeline
---------------------------------------

Now we have gone through the table class definition in some detail, let's actually create the table in the
database server, thus defining the first node in our data pipeline! You do so by simply creating an instance
of the table class:

.. code-block:: python

  mouse = Mouse()

Congratulations! You have just created your first table in your data pipeline. To verify that something actually
happened, enter the table object by itself:

.. code-block:: python

  >>> mouse
  *mouse_id    dob     gender
  +----------+ +-----+ +--------+

 (0 tuples)

You should get a print out displaying the table content, verifying that you indeed have defined a table in
the pipeline!

.. note::
  If this is not the fist time going through this section of the tutorial, chances are you already have
  the table ``Mouse`` defined in the schema ``dj_tutorial``. This is completely fine! If you define the
  class ``Mouse`` and instantiate it, the ``mouse`` instance will point to the same table you defined
  the first time you went through this tutorial! 

What if I make a mistake?
-------------------------
As you work through this tutorial, you might occasionally define and create a table with some errors.
Most commonly, you might create a table before you are completely done with the table ``definition``.
Although there are ways to update the table definition, it is usually best to simply delete or **drop**
the table with error and redefine the table after correcting your mistakes.

For example, you might have made a spelling error in your definition:

.. code-block:: python

  @schema
  class Mouse(dj.Manual):
        definition = """
        mose_id: int                   # unique mouse id
        ---
        dob: date                      # mouse date of birth
        gend: enum('M', 'F', 'U')    # gender of mouse - Male, Female, or Unknown/Unclassified
        """

Notice that both ``mouse_id`` and ``gender`` attributes are spelled incorrectly! If you don't notice such
error before you instantiated your table class:

.. code-block:: python
  
  mouse = Mouse()   # instantiating table with errors in definition

Then your table will be defined in the data pipeline containing these mistaked:

.. code-block:: python

  >>> mouse    # view the table
  *mose_id    dob     gend
  +---------+ +-----+ +------+

   (0 tuples)

Unfortunately, changing the table definition (the ``definition`` property) of the class after the table
has been created in the data pipeline does **not** change the definition of the already existing table.

The best way to deal with this error, especially this early in the design process, is to drop the table
all together. You can do so as follows:

.. code-block:: python
  
  >>> mouse.drop()
  `dj_tutorial`.`mouse` (0 tuples)
  Proceed? [yes, No]: 

Notice that the ``drop`` method prompts you to confirm the deletion, typing anything other than ``yes`` will
either result in a reprompt or cancellation. Type in ``yes`` at the prompt to confirm the drop:

.. code-block:: python
  
  >>> mouse.drop()
  `dj_tutorial`.`mouse` (0 tuples)
  Proceed? [yes, No]: yes
  Tables dropped. Restart kernel.

Now the table is dropped, you can fix errors in your class ``definition`` and recreate the table!

.. note::
  As the prompt for the ``drop`` method suggestion, you might want to restart your Python kernel after dropping
  tables. This can be important when rendering diagrams to show table connections.

What's next?
------------
Congratulations again! You have successfully created your first table in your data pipeline. In the 
:doc:`next section <inserting-data>`, we will giving the table some meat by inserting data into it!
