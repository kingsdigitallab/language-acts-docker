# npm packages install
# from https://github.com/kingsdigitallab/radical_translations/blob/develop/compose/production/django/Dockerfile
FROM node:18-slim as client-builder

WORKDIR /app
COPY ./package.json /app
RUN npm install && npm cache clean --force
COPY . /app


FROM python:3.7-slim-buster

ENV PYTHONUNBUFFERED 1


RUN apt-get update \
  # dependencies for building Python packages
  && apt-get install -y build-essential \
  # curl for node
  && apt-get install -y curl \
  # psycopg2 dependencies
  && apt-get install -y libpq-dev \
  # Translations dependencies
  && apt-get install -y gettext \
  && apt-get install -y libldap2-dev libsasl2-dev ldap-utils \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

RUN addgroup --system django \
  && adduser --system --ingroup django django


# Requirements are installed here to ensure they will be cached.
COPY ./requirements /requirements
RUN pip install -U pip
RUN pip install --no-cache-dir -r /requirements/production.txt \
  && rm -rf /requirements

#COPY ./compose/production/django/entrypoint /entrypoint
#RUN sed -i 's/\r$//g' /entrypoint
#RUN chmod +x /entrypoint
#RUN chown django /entrypoint

COPY ./compose/production/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start
RUN chown django /start
# COPY --chown=django:django . /app
COPY --from=client-builder --chown=django:django /app /app

#USER django
#
#WORKDIR /app
#
#ENTRYPOINT ["/entrypoint"]
