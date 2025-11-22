Wizards
=======

Fast-gov-uk have some handy tools for building
`GDS Question pages <https://design-system.service.gov.uk/patterns/question-pages/>`_ -
also known as ``Wizard`` on the interwebs.

The following is a simplified implementation of the
`Equality Survey <https://design-system.service.gov.uk/patterns/equality-information/>`_ -

.. code-block:: python
    :linenos:

    @fast.wizard
    def equality(step=0, data=None):
        return forms.Wizard(
            "equality",
            forms.Question(
                ds.Radios(
                    name="permission",
                    label="Do you want to answer the equality questions?",
                    choices={
                        "yes": "Yes, answer the equality questions",
                        "no": "No, skip the equality questions"
                    },
                ),
                cta="Continue",
            ),
            forms.Question(
                ds.Radios(
                    name="health",
                    label=(
                        "Do you have any physical or mental health conditions or illness "
                        "lasting or expected to last 12 months or more?"
                    ),
                    choices={"yes": "Yes", "no": "No", "skip": "Prefer not to say"},
                ),
                predicates={"permission": "yes"},
                cta="Continue",
            ),
            forms.Question(
                ds.Radios(
                    name="ability",
                    label=(
                        "Do any of your conditions or illnesses reduce your ability "
                        "to carry out day to day activities?"
                    ),
                    choices={"alot": "Yes, a lot", "little": "Yes, a little", "not": "Not at all", "skip": "Prefer not to say"},
                    required=False,
                ),
                predicates={"permission": "yes", "health": "yes"},
                cta="Continue",
            ),
            forms.Question(
                ds.Fieldset(
                    ds.Radios(
                        name="sex",
                        label="What is your sex?",
                        choices={"female": "Female", "male": "Male", "skip": "Prefer not to say"},
                    ),
                    ds.Radios(
                        name="gender",
                        label=(
                            "Is the gender you identify with the same as "
                            "your sex registered at birth?"
                        ),
                        choices={"yes": "Yes", "no": "No", "skip": "Prefer not to say"},
                    ),
                    legend="Sex and gender identity",
                    name="sex-and-gender",
                ),
                predicates={"permission": "yes"},
                cta="Continue",
            ),
            backends=[forms.DBBackend(db=fast.db)],
            step=step,
            data=data,
        )

1. The ``wizard`` decorator "registers" this function as a wizard rendered at
``/wizards/equality``. You can easily render this at a different url -
``@fast.wizard("/not-equality")``.

2. The ``equality`` function must return a ``Wizard`` object (see below) and it must accept
``step`` and ``data`` arguments. You can think of Wizards as a series of Forms. The ``step``
argument identifies a form within a ``Wizard``. Each Form can be empty or filled and when
they are filled, the ``data`` argument would contain the values that we can use to populate
our form fields.

3. The ``Wizard`` class is used to define a wizard. A Wizard comprises of one or more
``Question`` objects - which are a subclass of ``Form`` - and so they look like forms and
they work like forms.

25. Except, unlike ``Form`` objects, ``Question`` objects accept an argument called
``predicates``. This is a dictionary that defines the names of fields and the values they must
have if this particular ``Question`` is to be shown to our user. In our example, we are saying
that each ``Question`` following the first "permission" question would render only if the user
clicked "Yes, answer the equality questions".

62. Like ``Form`` objects, ``Wizard`` objects accepts a list of backends that define
what happens when a ``Wizard`` is processed upon submission. These backends are the same
as the ones in ``Form``.
