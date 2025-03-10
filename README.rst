Language Acts and Worldmaking
=============

.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
    :target: https://opensource.org/licenses/MIT
    :alt: MIT
.. image:: https://travis-ci.org/kingsdigitallab/language_acts.svg?branch=master
    :target: https://travis-ci.org/kingsdigitallab/language_acts
.. image:: https://coveralls.io/repos/github/kingsdigitallab/language_acts/badge.svg?branch=master
    :target: https://coveralls.io/github/kingsdigitallab/language_acts?branch=master
.. image:: https://readthedocs.org/projects/radical-translations/badge/?version=latest
    :target: https://language_acts.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status
.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg
    :target: https://github.com/kingsdigitallab/cookiecutter-django/
    :alt: Built with Cookiecutter Django
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/ambv/black
    :alt: Black code style

Overview
-----------

This is the repository for the Language Acts and Worldmaking, currently maintained by [King's Digital Lab](https://github.com/kingsdigitallab/).

This project has been redesigned to run in a Docker container, aimed at an Openstack deployment.

Containers:
-----------

- [nginx-proxy](https://hub.docker.com/r/nginxproxy/nginx-proxy): This is the primary entry point for the stack, running on 80.  It automatically builds a proxy to other containers.
- [django 3.2](https://hub.docker.com/layers/library/python/3.6-slim-buster/images/sha256-5dd134d6d97c67dd02e4642ab24ecbb9d23059ea018a8b5185784d29dce2f37a?context=explore): The main container for the project (see more detailed description below.)
- [nginx](https://hub.docker.com/_/nginx): This is the static data container, serving Django's static content.
- db ([Postgres 12.3](https://www.postgresql.org/docs/12/index.html)): The database container for Django above.
- elasticsearch [7.10](https://hub.docker.com/_/elasticsearch): The indexing container, used by Haystack 3.2.1. (Pre-migration, Haystack 2 was using Solr 6.)

ENV file
-----------

The compose file will look for deployment variables in a compose/.env file.  Below is a sample file::


    # Django
    DJANGO_READ_DOT_ENV_FILE=True
    DJANGO_SETTINGS_MODULE=config.settings.production
    DJANGO_ALLOWED_HOSTS=
    DJANGO_SECRET_KEY=
    DJANGO_ADMIN_URL=


    # Security
    # ------------------------------------------------------------------------------
    # TIP: better off using DNS, however, redirect is OK too
    DJANGO_SECURE_SSL_REDIRECT=False

    # Email
    # ------------------------------------------------------------------------------
    MAILGUN_API_KEY=
    DJANGO_SERVER_EMAIL=
    MAILGUN_DOMAIN=

    # django-allauth
    # ------------------------------------------------------------------------------
    DJANGO_ACCOUNT_ALLOW_REGISTRATION=True



    # Elasticsearch
    # ------------------------------------------------------------------------------
    discovery.type=single-node

    # Database
    # ------------------------------------------------------------------------------
    # PostgreSQL
    # ------------------------------------------------------------------------------
    POSTGRES_HOST=db
    POSTGRES_PORT=5432
    POSTGRES_DB=
    POSTGRES_USER=
    POSTGRES_PASSWORD=
    DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}



    # django-allauth
    # ------------------------------------------------------------------------------
    DJANGO_ACCOUNT_ALLOW_REGISTRATION=True

    # django-compressor
    # ------------------------------------------------------------------------------
    COMPRESS_ENABLED=False
    COMPRESS_OFFLINE=True

    # Gunicorn
    # ------------------------------------------------------------------------------
    WEB_CONCURRENCY=4


    # Redis
    # ------------------------------------------------------------------------------
    REDIS_URL=redis://redis:6379/0

    # https://django-auth-ldap.readthedocs.io/
    # ------------------------------------------------------------------------------
    LDAP_SERVER_URI=
    LDAP_BIND_DN=
    LDAP_BIND_PASSWORD=

    LDAP_BASE_DC=
    LDAP_BASE_GROUP=

    LDAP_FIRST_NAME_FIELD=givenName
    LDAP_LAST_NAME_FIELD=sn
    LDAP_EMAIL_FIELD=mail


Fill in the database credentials and Django variables.  If deploying via a CI pipeline such as Gitlab, this file will need to be included in its variables (in the KDL setup, we encode this in base64 and add it to the CI/CD variables in the repository settings.)

Deployment notes
----------------

- After deployment, don't forget to run python manage.py update_index to build the Haystack index.  This won't happen automatically.

Settings
--------

See detailed `cookiecutter-django settings documentation`_.

.. _cookiecutter-django settings documentation: http://cookiecutter-django-kingsdigitallab.readthedocs.io/en/latest/settings.html

Development
-----------

Local with Docker
^^^^^^^^^^^^^^^^^

See detailed `cookiecutter-django development with Docker documentation`_.

.. _cookiecutter-django development with Docker documentation: https://cookiecutter-django-kingsdigitallab.readthedocs.io/en/latest/developing-locally-docker.html

Local without Docker
^^^^^^^^^^^^^^^^^^^^

See detailed `cookiecutter-django local development documentation`_.

.. _cookiecutter-django local development documentation: https://cookiecutter-django-kingsdigitallab.readthedocs.io/en/latest/developing-locally.html

Basic Commands
--------------

Setting Up Your Users
^^^^^^^^^^^^^^^^^^^^^

* To create a **normal user account**, just go to Sign Up and fill out the
  form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go
  to your console to see a simulated email verification message. Copy the link
  into your browser. Now the user's email should be verified and ready to go.

* To create an **superuser account**, use this command::

    $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your
superuser logged in on Firefox (or similar), so that you can see how the site
behaves for both kinds of users.

Type checks
^^^^^^^^^^^

Running type checks with mypy:

::

  $ mypy language_acts

Test coverage
^^^^^^^^^^^^^

To run the tests, check your test coverage, and generate an HTML coverage report::

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

Running tests with py.test
~~~~~~~~~~~~~~~~~~~~~~~~~~

::

  $ pytest

Live reloading and Sass CSS compilation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Moved to `Live reloading and SASS compilation`_.

.. _`Live reloading and SASS compilation`: http://cookiecutter-django-kingsdigitallab.readthedocs.io/en/latest/live-reloading-and-sass-compilation.html





Deployment
----------

The following details how to deploy this application.



Docker
^^^^^^

See detailed `cookiecutter-django Docker documentation`_.

.. _`cookiecutter-django Docker documentation`: http://cookiecutter-django-kingsdigitallab.readthedocs.io/en/latest/deployment-with-docker.html



