Cookies
=======

All GDS services are required to tell users about the cookies they are setting on the user's device and
let them accept or reject different types of non-essential cookies.

Fast-gov-uk uses session cookies to track user's journey through question pages (or wizards).

In view of the above, fast-gov-uk comes out of the box with 2 features -

Cookie Banner
-------------

A GDS-style cookie banner to tell users that we are using essential cookies -

.. image:: https://raw.githubusercontent.com/alixedi/fast-gov-uk/refs/heads/main/docs/_static/start.png
   :alt: Screenshot of the simple example

If you would like to modify the cookie banner, you can do so by looking at the code for the ``cookie_banner```
function in ``fast_gov_uk/core.py`` module and writing your own.


Cookie page
-----------

A GDS-style cookies page to tell users details such as name and purpose of the cookies used by the
service -

.. image:: https://raw.githubusercontent.com/alixedi/fast-gov-uk/refs/heads/main/docs/_static/cookies.png
   :alt: Screenshot of the cookies page


If you would like to modify the cookies page, you can do that easily like so -

.. code-block:: python

    # add this to your app.py
    @fast.page
    def cookies():
        return ds.Cookies(
            ds.P("Extra content that I would like to add to the cookies page.")
        )
