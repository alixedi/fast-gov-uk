Cookies
=======

All GDS services are required to tell users about the cookies they are setting on the user's device and
let them accept or reject different types of non-essential cookies.

Fast-gov-uk uses session cookies to track user's journey through question pages (or wizards).

In view of the above, fast-gov-uk comes out of the box with 2 cookie features -

Cookie Banner
-------------

A GDS-style cookie banner to tell users that we are using essential cookies -

.. image:: https://raw.githubusercontent.com/alixedi/fast-gov-uk/refs/heads/main/docs/_static/start.png
   :alt: Screenshot of the simple example

The default cookie banner is served on the URL - ``/cookie-banner``. If you want to override the
default cookie banner, you can define your banner in ``app.py`` and wire it up to the same URL.


Cookie page
-----------

A GDS-style cookies page to tell users details about the cookies being set on their devices
including name and purpose of each cookie used by the service -

.. image:: https://raw.githubusercontent.com/alixedi/fast-gov-uk/refs/heads/main/docs/_static/cookies.png
   :alt: Screenshot of the cookies page


If you would like to modify the default cookies page, you can do that easily like so -

.. code-block:: python

    # add this to your app.py
    @fast.page
    def cookies():
        return ds.Cookies(
            ds.P("Extra content that I would like to add to the cookies page.")
        )
