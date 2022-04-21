ARG PYTHON_VERSION=3.9

# define an alias for the specfic python version used in this file.
FROM python:${PYTHON_VERSION}-bullseye as poetry

# install poetry in PATH
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/usr python -

# Python build stage
FROM poetry
RUN apt update \
    && apt upgrade -y \
    && apt install -y --no-install-recommends build-essential gcc libpq-dev gettext \
    # cleaning up unused files
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

#
#RUN python -m venv /opt/venv
## Make sure we use the virtualenv:
#ENV PATH="/opt/venv/bin:$PATH"

COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev

# Don't buffer and don't write bytecode
ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100

ARG APP_HOME=/app/
ARG APP_SRC=.
ARG APP_USER=django

# add a user for the application
RUN addgroup --system ${APP_USER} \
    && adduser --system --ingroup ${APP_USER} ${APP_USER} \
    && mkdir -p ${APP_HOME} \
    # make APP_USER owner of the WORKDIR directory as well.
    && chown ${APP_USER}:${APP_USER} ${APP_HOME}

WORKDIR ${APP_HOME}

# copy application code to WORKDIR
COPY --chown=${APP_USER}:${APP_USER} ${APP_SRC} ${APP_HOME}

USER ${APP_USER}
RUN ls -la
RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "--log-file", "-", "--threads", "10", "--bind", "0.0.0.0:8000", "hello_aws.wsgi"]
