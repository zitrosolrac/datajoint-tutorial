Building Your First Pipeline
============================

**Author**: Edgar Y. Walker
**Updated**: 2017-06-03

There is no better way to learn about a tool than to just start using it! In this tutorial, we will learn
DataJoint by building our very first data pipeline! To motivate the process of data pipeline designs and 
usages, we are going to assume the role of *a neuroscientist working with mouse* and build a data pipeline
to collect and process data from mouse experiment sessions!

.. note::
  This tutorial assumes that you already have installed DataJoint library for Python or MATLAB and have
  already configured a database server where you can create new database schemas and tables. If you don't
  have either of this, be sure to checkout :doc:`/setting-up/introduction` before moving on!



What's covered in this tutorial?
--------------------------------
In this tutorial, we will walk through the process of designing, creating, and populating data pipelines
step-by-step. In particular, we will cover the following conecepts among others:

- How to define a new table in DataJoint
- Difference between different table types or *tiers*
- How to insert data into a table manually
- How to query and fetch data from the tables
- How to import data from files into a table automatically
- How to define computed tables whose entries are computed from other tables
- General tips on designing functional and extensible data pipelines.

Designing data pipelines for mouse experiments
----------------------------------------------
Designing good data pipelines starts with understanding your data and data collection procedure very well.
Let's start by describing how you as a mouse neuroscientist might want to collect data about your experiments:

- You perform electrophysiology experiment from mouse, collecting data about their brain activities.
- Your lab houses many mice, and each mouse is identified by a unique ID. You also want to keep track of information
  about each mouse such as their date of birth, gender, and genetic background.
- As a hard working neuroscientist, you perform experiments with mouse every day, sometimes working with more
  than one mise in a day! For each experiment **session**, you would like to record what mouse you worked
  with and when you have performed the experiment. You would also like to keep track of other helpful information
  such as the experiment setup you have worked with, etc.
- In each such experiment **session**, you record activities from one or more neurons. You use recording equipment
  that produces data files for each neuron recorded at the end of the experiment session.

Notice how there is a lot of **information** that are related to but not necessary a direct part of your
mouse experiments. For example, the gender and genetic background of the mouse you record from may not be
directly relevant to your experiments, but they are certainly important pieces of information that you would
like to keep available somewhere.

Similarly, information such as the setup (i.e. experiment equipment) with 
which you performed the experiment might be irrelevant for your final data analysis of mouse brain activities, 
but may come in handy if you ever run into situation where you found a problem in a setup and have to 
recompute analysis on all data collected from that particular setup.i

As you will see shortly, with DataJoint, it is not only easy but very natural to create a data pipelines
that can include all of the above information! Now choose your language and move on with the tutorial!

Building in Python
------------------

Ready to start building your data pipeline in Python? Proceed to :doc:`building_first_pipeline/python/first-table` now!

.. note::
  To complete this, you must have a properly configured database server and a computer with Python 3.4 or above
  with DataJoint package already installed and configured to connect to the database. If you don't have this
  setup up, refer to :doc:`/setting-up/introduction` to configure your development environment before proceeding.

.. toctree::
   :maxdepth: 2
   :hidden:
   :includehidden:
   :caption: Getting Started

   building_first_pipeline/python/first-table
   building_first_pipeline/python/inserting-data
   building_first_pipeline/python/querying-data
   building_first_pipeline/python/child-table


Building in MATLAB
------------------

Ready to start building your data pipeline in MATLAB? Proceed to :doc:`building_first_pipeline/matlab/first-table` now!

.. note::
  To complete this, you must have a properly configured database server and a computer with MATLAB 2015b or newer
  with DataJoint toolbox already installed and configured to connect to the database. If you don't have this
  setup up, refer to :doc:`/setting-up/introduction` to configure your development environment before proceeding.

.. toctree::
   :maxdepth: 2
   :hidden:
   :includehidden:
   :caption: Getting Started

   building_first_pipeline/matlab/first-table

