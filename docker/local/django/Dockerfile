ARG PYTHON_VERSION=3.10-slim

FROM python:${PYTHON_VERSION} as python

FROM python as python-build-stage
ARG BUILD_ENVIRONMENT=local

WORKDIR /app

COPY requirements .

RUN apt-get update --fix-missing && \
    apt-get install --no-install-recommends -y \
    build-essential \
    libpq-dev


RUN pip wheel --wheel-dir /app/wheels \
   -r ${BUILD_ENVIRONMENT}.txt


FROM python as python-run-stage

ARG BUILD_ENVIRONMENT=local
ARG APP_HOME=/app

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

ENV BUILD_ENV ${BUILD_ENVIRONMENT}

WORKDIR ${APP_HOME}

RUN apt-get update && apt-get install --no-install-recommends -y \
    libpq-dev \
    gettext
COPY --from=python-build-stage /app/wheels /wheels/

RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
   && rm -rf /wheels/


COPY ./docker/local/django/entrypoint /entrypoint
RUN chmod +x /entrypoint

COPY ./docker/local/django/start /start
RUN chmod +x /start

COPY . ${APP_HOME}

ENTRYPOINT ["/entrypoint"]
