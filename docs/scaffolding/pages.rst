Pages
======

You can easily and quickly add web pages to your service using the `@page` decorator with a function
that returns a FastHTML component.

In addition, we have the `Page` component that implements the `GDS Page Template <https://design-system.service.gov.uk/styles/page-template/>`_ -
including the header, the phase banner and the footer etc.

Lets start with a simple example -

.. code-block:: python

    # add this to your app.py
    @fast.page
    def faqs():
        return ds.Page(
            ds.H1("Frequently asked questions"),
            ds.Detail("First question", "Answer to the first question"),
            ds.Detail("Second question", "Answer to the second question"),
            ds.Detail("Third question", "Answer to the third question"),
        )

To run the example:

.. code-block:: bash

   python app.py

Point your browser to: ``http://localhost:5001/faqs``

.. image:: https://raw.githubusercontent.com/alixedi/fast-gov-uk/refs/heads/main/docs/_static/faqs.png
   :alt: Screenshot of the FAQs


Note that the `@page` decorator picks up the URL for your page - `/faqs` here - from the name of your
function. Sometimes, you might want to serve the page on a different URL. A good example for this is
the home page -

.. code-block:: python

    # add this to your app.py
    @fast.page("/")
    def home():
        return ds.Page(
            # A single Paragraph
            ds.P("Welcome to Fast Gov UK.")
        )

Point your browser to: ``http://localhost:5001/`` -

.. image:: https://raw.githubusercontent.com/alixedi/fast-gov-uk/refs/heads/main/docs/_static/home.png
   :alt: Screenshot of the home page
