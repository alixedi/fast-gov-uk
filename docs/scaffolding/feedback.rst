Feedback
========

User feedback is an `important part <https://www.gov.uk/service-manual/service-assessments/get-feedback-page>`_
of every GDS service. In view of this, fast-gov-uk comes out of the box with a basic feedback form.

Lets take it for a spin -

.. code-block:: bash

   python app.py

Point your browser to: ``http://localhost:5001/forms/feedback``

.. image:: https://raw.githubusercontent.com/alixedi/fast-gov-uk/refs/heads/main/docs/_static/feedback.png
   :alt: Screenshot of the simple example

If you want to modify the built-in feedback form, you can do by defining your own
feedback form in ``app.py``, which should override the default.

In the following example, we are removing the ``comments`` field and replacing the ``LogBackend``
with ``EmailBackend`` - which uses GOV.UK Notify to send the contents of your form to a given
email address -

.. code-block:: python

    # add this to your app.py
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
            backends=[
                forms.EmailBackend(
                    fast.notify("<template_id>", "recepient@mail.com")
                )
            ],
            success_url="/",
            data=data,
            cta="Send feedback",
        )
