FROM python:3.14.3-trixie AS python


FROM python AS python_with_libreoffice

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && \
    apt-get --no-install-recommends install libreoffice -y && \
    apt-get install -y libreoffice-java-common default-jre


FROM python_with_libreoffice AS python_with_libreoffice_and_poetry

RUN pip install poetry


FROM python_with_libreoffice_and_poetry AS python_with_libreoffice_and_project_dependencies

ENV POETRY_VIRTUALENVS_CREATE=false
ENV POETRY_VIRTUALENVS_IN_PROJECT=false

WORKDIR /app
COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock
RUN poetry install --only main --no-root
