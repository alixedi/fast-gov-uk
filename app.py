from os import environ as env

from fast_gov_uk import Fast, serve
import fast_gov_uk.design_system as ds

# This is your settings. They are set for development on your
# own computer by default. When you are deploying your service,
# you can override them by setting environment variables.
SETTINGS = {
    "SERVICE_NAME": env.get("SERVICE_NAME", "Fast Gov UK"),
    "DATABASE_URL": env.get("DATABASE_URL", "data/service.db"),
    "DEV_MODE": env.get("DEV_MODE", True),
    "NOTIFY_API_KEY": env.get("NOTIFY_API_KEY", None),
}

# This creates the Fast object that encapsulates everything
# in your service
fast = Fast(SETTINGS)


# If I do @fast.page() instead, this page will be available
# on /home i.e. the name of the function
@fast.page("/")
def home():
    return ds.Page(
        # A single Paragraph
        ds.P("Welcome to Fast Gov UK.")
    )


# Serves the app
serve(app="fast")
