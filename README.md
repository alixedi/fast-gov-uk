# fast-gov-uk

Fast-gov-uk is a new toolkit for **rapid development of simple gov.uk services**.

Fast-gov-uk is three things -

1) an implementation of [gov.uk design system](https://design-system.service.gov.uk) in Python using [FastHTML](https://www.fastht.ml)
2) lightweight scaffolding for common service patterns e.g. forms
3) designed from the ground-up for AI agents to help with rapid development


## Installation

```
$ pip install fast-gov-uk
```


## A Simple Example

```python
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
```

```
$ python app.py
```

Point your browser to: `http://localhost:5001` -

![Screenshot of the simple example](https://raw.githubusercontent.com/alixedi/fast-gov-uk/refs/heads/main/docs/_static/start.png)


## Resources

* [Documentation](https://fast-gov-uk.readthedocs.io/en/latest/)
