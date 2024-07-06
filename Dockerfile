FROM python:3.12-slim AS requirements

WORKDIR ./app
RUN pip install poetry
COPY pyproject.toml poetry.lock ./

RUN poetry export --without-hashes --without=dev > requirements.txt

FROM python:3.12-slim AS base

COPY --from=requirements ./app ./app

WORKDIR ./app
RUN pip install -r ./requirements.txt --no-cache-dir

COPY ./src ./
