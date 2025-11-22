Fast-gov-uk
===========

Fast-gov-uk is a new toolkit for **rapid development of simple gov.uk services**.

Fast-gov-uk is three things:

- an implementation of the `GOV.UK Design System <https://design-system.service.gov.uk>`_ in Python using `FastHTML <https://www.fastht.ml>`_,
- lightweight scaffolding for common service patterns (for example, forms),
- designed from the ground-up for AI agents to help with rapid development.

Installation
------------

.. code-block:: bash

   pip install fast-gov-uk


A Simple Example
----------------

.. code-block:: python

   # save this as app.py
   from fast_gov_uk import Fast, serve
   from fast_gov_uk import design_system as ds

   fast = Fast()

   @fast.page("/")
   def get_started():
       return ds.Page(
           ds.Warning("This is a demo and not a real service"),
           ds.H1("Welcome to the service"),
           ds.P("You will need the following information handy:"),
           ds.Ul(
               ds.Li("NI Number"),
               ds.Li("Date of birth"),
               ds.Li("Email"),
               bullet=True,
           ),
           ds.StartButton("I am ready", "/forms/"),
       )

   serve(app="fast")

To run the example:

.. code-block:: bash

   python app.py

Point your browser to: ``http://localhost:5001``

.. image:: https://raw.githubusercontent.com/alixedi/fast-gov-uk/refs/heads/main/docs/_static/start.png
   :alt: Screenshot of the simple example


Next Steps
----------

.. toctree::
   :maxdepth: 2

   design_system/index
   scaffolding/index
   ai
