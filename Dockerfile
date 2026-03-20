FROM python:3.14.3-trixie AS python


FROM python AS python_with_libreoffice

RUN apt-get update && \
    apt-get --no-install-recommends install libreoffice -y && \
    apt-get install -y libreoffice-java-common default-jre


FROM python_with_libreoffice AS python_with_libreoffice_and_poetry

RUN pip install poetry


FROM python_with_libreoffice_and_poetry AS python_with_libreoffice_and_project_dependencies

WORKDIR /app
COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock
RUN poetry config virtualenvs.create false
RUN poetry install --no-root
