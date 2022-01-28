ARG PYTHON_VERSION=3.9-slim-bullseye

# define an alias for the specfic python version used in this file.
FROM python:${PYTHON_VERSION} as python

# Python build stage
FROM python AS compile-image
RUN apt-get update && apt-get install -y --no-install-recommends build-essential gcc libpq-dev gettext \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*


RUN python -m venv /opt/venv
# Make sure we use the virtualenv:
ENV PATH="/opt/venv/bin:$PATH"

# Don't buffer and don't write bytecode
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY pyproject.toml .
COPY poetry.lock .
COPY hello_aws .
RUN pip install poetry && poetry config virtualenvs.create false && poetry install --no-dev

#COPY setup.py .
#COPY src/ .
#RUN pip install .


FROM python AS build-image
COPY --from=compile-image /opt/venv /opt/venv

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100

ARG APP_HOME=/app

# add a user for the application
RUN addgroup --system django \
    && adduser --system --ingroup django django

COPY --chown=django:django ./build/django/scripts/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY --chown=django:django ./build/django/scripts/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start


# copy application code to WORKDIR
COPY --chown=django:django ./hello_aws ${APP_HOME}

# make django owner of the WORKDIR directory as well.
RUN chown django:django ${APP_HOME}

WORKDIR ${APP_HOME}

USER django
# Make sure we use the virtualenv:
ENV PATH="/opt/venv/bin:$PATH"

RUN python -c "import sys; print(sys.executable)"

ENTRYPOINT ["/entrypoint"]
