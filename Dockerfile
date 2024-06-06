FROM python:3.8-slim as python

# Python build stage
FROM python as python-build-stage

# Install apt packages
RUN apt-get update && apt-get install --no-install-recommends -y \
  # dependencies for building Python packages
  build-essential \
  # psycopg dependencies
  libpq-dev

COPY requirements.txt requirements.txt

# Create Python Dependency and Sub-Dependency Wheels.
RUN pip wheel --wheel-dir /usr/src/app/wheels  \
  -r requirements.txt

# Python 'run' stage
FROM python as python-run-stage

ARG APP_HOME=/app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR ${APP_HOME}

RUN addgroup --system django \
    && adduser --system --ingroup django django

# Install required system dependencies
RUN apt-get update && apt-get install --no-install-recommends -y \
  # psycopg dependencies
  libpq-dev \
  # Translations dependencies
  gettext \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*


COPY --from=python-build-stage /usr/src/app/wheels  /wheels/

# use wheels to install python dependencies
RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
  && rm -rf /wheels/

#COPY ./compose/django/entrypoint /entrypoint
#RUN sed -i 's/\r$//g' /entrypoint
#RUN chmod +x /entrypoint
#
#COPY --chown=django:django start start
#RUN sed -i 's/\r$//g' start
#RUN chmod +x start
#
## copy application code to WORKDIR
#COPY --chown=django:django . ${APP_HOME}
#
# make django owner of the WORKDIR directory as well.
RUN chown -R django:django ${APP_HOME}

USER django

COPY . .
#
#ENTRYPOINT ["/entrypoint"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]