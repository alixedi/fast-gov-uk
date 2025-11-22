Design System in Python
=======================

At its core, `fast-gov-uk` is an implementation of the
`GOV.UK Design System <https://design-system.service.gov.uk>`_ in Python.

We do this using the excellent `FastHTML <https://www.fastht.ml>`_ library, which
provides a simple way to create interactive HTML components using pure Python.

Here is an example of a FastHTML component -

.. code-block:: python

   def H1(text, size="l", caption="", **kwargs) -> fh.FT:
      return fh.H1(
         text,
         fh.Span(caption, cls=f"govuk-caption-{size}") if caption else "",
         cls=f"govuk-heading-{size}",
         **kwargs,
      )

Like **H1** above, we have implemented all the components from the GOV.UK Design System
in pure Python.

In addition, we have created some higher-level components like **Page** -
that help you build complete GDS-style pages quickly and easily.

Finally, we have also created some components that are not part of the GOV.UK
Design System, but are commonly used in GOV.UK services e.g. **EmailInput**
and other components in the **contrib** module.

These components are organised into modules according to their type -

.. toctree::
   :maxdepth: 1

   pages
   typography
   components
   navigation
   inputs
   contrib
   utils
