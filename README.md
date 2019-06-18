# act-blue-knack

Synchronization of ActBlue donation data with a Knack data store

## Details

This project sets up an endpoint to process ActBlue donation webhooks,
as documented [here](https://secure.actblue.com/docs/webhooks). The
details mapping what ActBlue fields should go to which Knack fields
are kept under `/sync_data/actblue_mappings/`. The desired fields as
well as their mappings to Knack were provided by Sister District.

## Development and Deploying

This project is primarily written in Django and setup to be deployed
to Heroku. If you're unfamiliar with Django, the
[tutorial](https://docs.djangoproject.com/en/1.11/intro/tutorial01/)
is quite good and provides all of the basics that you'll need. The
bulk of the webhook handling view is found at `/sync/views.py`, while
the module to load data into Knack is found under `/knackload/`.

When testing locally or on a dev machine, you'll want to make sure to
set the `DJANGO_SETTINGS_MODULE` variable in your local environment to
`sync_data.test_settings`. This will ensure that test data goes to
the test Knack database rather than the production database, as well
as setting `DEBUG` to `True` which will print logs to stdout as well
as causing the endpoint to return stacktraces on error. When the app
is deployed to production, you will also need to set
`KNACK_ENVIRONMENT` variable to `production` to ensure that data is
written to the production database. If any settings need to be updated
or added, settings shared between environments belong in
`/sync_data/base_settings.py`, while settings for specific
environments can be put in `/sync_data/settings.py` and
`sync_data/test_settings.py` respectively. By default, the app will use
`sync_data.settings.py` -- to change this when the app is deployed to
Heroku, you can update `/sync_data/wsgi.py`.

You can copy `sample.env` to `.env` in your local copy to set these
environment variables to sensible defaults for local development.
Running `pipenv shell` will automatically load them into your shell.

## Build status

[![CircleCI](https://circleci.com/gh/RagtagOpen/act-blue-knack/tree/master.svg?style=svg)](https://circleci.com/gh/RagtagOpen/act-blue-knack/tree/master)
