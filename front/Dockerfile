ARG NODE_VERSION=16-bullseye-slim

# define an alias for the specfic python version used in this file.
FROM node:${NODE_VERSION} as node

# update the base image
RUN apt update \
    && apt upgrade -y \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

# Node build stage
FROM node

ARG APP_HOME=/app/
ARG APP_SRC=.
ARG APP_USER=nuxt

# add a user for the application
RUN addgroup --system ${APP_USER} \
    && adduser --system --ingroup ${APP_USER} ${APP_USER} \
    && mkdir -p ${APP_HOME} \
  # make ${APP_USER owner of the WORKDIR directory as well.
    && chown ${APP_USER}:${APP_USER} ${APP_HOME}

WORKDIR ${APP_HOME}

# copy application code to WORKDIR
COPY --chown=${APP_USER}:${APP_USER} ${APP_SRC} ${APP_HOME}

USER ${APP_USER}
RUN npm ci \
  && npm run build

# expose 3000 on container
ENV NUXT_PORT=3000 \
    NUXT_HOST="0.0.0.0"
EXPOSE ${NUXT_PORT}

# start the app
CMD [ "npm", "start" ]
