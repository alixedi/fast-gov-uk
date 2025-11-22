Forms
=====

Fast-gov-uk have some handy features to build GDS forms.


An Example
----------

Let's start with a familiar example. User feedback is an
`important part <https://www.gov.uk/service-manual/service-assessments/get-feedback-page>`_
of every GDS service -

.. image:: https://raw.githubusercontent.com/alixedi/fast-gov-uk/refs/heads/main/docs/_static/feedback.png
   :alt: Screenshot of the simple example

The following is how you would build this feedback form in fast-gov-uk -

.. code-block:: python
    :linenos:

    @fast.form
    def feedback(data=None):
        return forms.Form(
            "feedback",
            ds.H1("Give feedback on Fast GOV UK"),
            ds.H2("Satisfaction survey"),
            ds.Radios(
                name="satisfaction",
                label="Overall, how satisfied did you feel about Fast Gov UK?",
                choices={
                    "very-satisfied": "Very Satisfied",
                    "satisfied": "Satisfied",
                    "neutral": "Neither satisfied not dissatisfied",
                    "dissatisfied": "Dissatisfied",
                    "very-dissatisfied": "Very dissatisfied",
                },
                heading="s",
            ),
            ds.CharacterCount(
                name="comments",
                label="How could we improve this service?",
                maxchars=1200,
                required=False,
                hint=(
                    "Do not include any personal or financial information, "
                    "for example your national insurance number."
                ),
                heading="s",
            ),
            backends=[forms.LogBackend()],
            success_url="/",
            data=data,
            cta="Send feedback",
        )


1. The ``form`` decorator "registers" feedback function as a form rendered at
``/forms/feeback``. You can easily render this form at a different url -
``@fast.form("/not-feedback")``.

2. The ``feedback`` function must return a ``Form`` object (see below) and it must accept
a ``data`` argument because forms can be empty or filled and when they are filled, the
``data`` argument would contain the values to populate the fields in our form.

3. The ``Form`` class is used to define a form. A Form can have any number of fast-gov-uk
components but it is expected that at least some of these would be ``Field`` components
as defined in ``fast_gov_uk.design_system.inputs.py`` module. Here we have a ``Radios``
field and a ``CharacterCount`` field.

30. The ``Backend`` class defines what happens when a form is processed upon submission.
Here we are using the ``LogBackend`` which - as the name suggests - logs the values that
were submitted in our form.

31. The ``success_url`` parameter defines the URL that we redirect to after a form is
processed.

Form Backends
-------------

Fast-gov-uk comes out-of-the-box with the following form backends -

.. autoclass:: fast_gov_uk.forms.LogBackend

.. autoclass:: fast_gov_uk.forms.DBBackend

.. autoclass:: fast_gov_uk.forms.EmailBackend

.. autoclass:: fast_gov_uk.forms.APIBackend

.. autoclass:: fast_gov_uk.forms.SessionBackend
