# fast-gov-uk

Fast-gov-uk is three things -

1) an implementation of [gov.uk design system](https://design-system.service.gov.uk) in Python using [FastHTML](https://www.fastht.ml)
2) lightweight scaffolding for common service patterns e.g. forms
3) designed from the ground-up for AI agents to help with rapid development

## Setting up your computer

You will need 3 things to get started with fast-gov-uk -

1) `Git` version control system (get it [here](https://git-scm.com/downloads/mac))
2) `uv` Python package manager (get it [here](https://docs.astral.sh/uv/getting-started/installation/))
3) `VSCode` editor (get it [here](https://code.visualstudio.com/download))

## Getting started

At the moment, fast-gov-uk is a service template and not a Python package. As a result,
the best way to get started is the following -

1) [fork the repository on GitHub](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo)

2) [Clone the repository](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo#cloning-your-forked-repository), forked from fast-gov-uk, to your computer

3) [Run the service](#first-page) on your computer and start noodling

## Building your first page

Fast-gov-uk comes with a few common pages built-in. Firstly, lets explore these -

Open VSCode editor - File > Open Folder > Choose the cloned `fast-gov-uk` repository.

Now, hit the play button on the top-left corner. This will run the development server which
will let you see your service running in your local browser.

Open up your browser and type the following URL - `127.0.0.1:5001`. You should see the `fast-gov-uk`
home page.

Now in your VSCode editor, open the file called `app.py`. Take a look at the function called `home`. Note that it returns a `Page` with a single `P` (paragraph) with the text - "Welcome to Fast Gov UK". Change the text to something else. Save the file. Go back to the browser and hit refresh. You should be able to see the new text in the browser.

If you wanted to create a fresh page, you can do so by defining a function that returns a `Page` with whatever content you want to put in it and decorating it with `@fast.page` decorator. E.g. -

```
@fast.page
def faqs():
    return ds.Page(
        # Heading -
        ds.H1("Frequently Asked Questions")
        ds.Detail("First question", ds.P("Answer to first question."))
        ds.Detail("Second question", ds.P("Answer to second question."))
        ds.Detail("Third question", ds.P("Answer to third question."))
        # Etc.
    )
```

Hit the save button, go to your browser and type `127.0.0.1:5001/faqs`. You should see a brand
new FAQs page on your service.

## Building your first form

I feel that gov.uk services have 2 very common interaction patterns - (1) giving information to users and (2) getting information from users.

`fast-gov-uk` have some lightweight scaffolding for both. We have covered the former through `Page`. The latter is covered through forms. Lets take a peek -

Make sure the development server is runnine. Go to your browser and type `127.0.0.1:5001/form/feedback`. You should see a standard gov.uk feedback form.

Try filling it in and hit Submit. This should take you to the home page. This means that the form was submitted and processed without errors. We will come back to this later.

Also try breaking the form - leave it blank and hit submit, leave some fields blank and hit submit etc. You will note that the form has basic validation logic that helps ensure that the users cannot submit this form witohut filling the required fields with the right information.

Try changing the form. E.g. you can change the `label` of the `CharacterCount` field to "Tell us how we are doing". Hit the save button. Go to your browser. Hit refresh. The `CharacterCount` field should have the new label.

Finally, just like `Pages`, you can also create your own new `Forms` -

```
@fast.form
def email(data=None):
    return forms.DBForm(
        fields=[
            ds.EmailInput(
                name="email",
                label="Please type your email address",
            ),
        ],
        data=data,
        success_url="/demo",
        cta="Submit",
    )
```

Hit save. Go to your browser and type `127.0.0.1:5001/form/email`. You should see your brand new form.

Try to break this - submit without an email address. Submit with something that is not a valid email address etc.

Now put in a proper email address and submit the form. You should be redirected to the `demo` page. This means the form was submitted successfully.

Lets go a little deeper into `fast-gov-uk` and see what comes out of the box -

## An Implementation of the gov.uk design system in Python

If you have completed a Programming 101 course, chances are that you learned Python. If you work in gov.uk, the preferred application platform is the Web. With `fast-gov-uk`, my ambition is to enable new/junior developers who just know Python to build `gov.uk` services with confidence.

The foundation for this is an implementation of gov.uk design system in Python. You can see the code for this in the [design_system](https://github.com/alixedi/fast-gov-uk/tree/main/fast_gov_uk/design_system) directory in this project.

P.S. Note that all the components have type hints and are well-documented. This should help with (1) readability (2) autocomplete in VSCode and more excitingly (3) AI code agents.

## Lightweight scafoolding for common gov.uk patterns

Most obvious example for this is that `fast-gov-uk` comes with a feedback form out of the box.

More interestingly, it lets you write functions that return a `Page` or a `Form` and these pop up as real pages and forms in your browsers without having to do anything else.

Finally, this "scaffolding" is fairly lightweight. If you do need to roll up your sleeves and e.g. start writing your endpoints, you can!

## Designed from the ground up for AI

Watch this [demo](https://youtu.be/r6OBRBT7aBU).
