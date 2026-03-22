<h1 align="center"><a href="https://github.com/codespearhead/word-to-pdf-api">Doc to PDF API</a></h1>

<p align="center">
    <br>
  <a href="https://pixabay.com/vectors/pdf-document-documents-pdf-file-4919559/">
    <img src="https://cdn.pixabay.com/photo/2020/03/10/17/02/pdf-4919559_960_720.png" width="120px" height="120px"/>
  </a>
  <br><br>
    Seamlessly convert Microsoft Word documents (.DOC/.DOCX) to PDF programmatically via a REST API
  <br>
</p>

<br>


## Quickstart

### Prerequisites

1. Ensure you have the latest stable version of Docker Compose installed on your machine:

```bash
docker compose version
```

### Start the server

> **Note**: The initial build may take a while as LibreOffice is a large dependency. Subsequent builds and container starts will be near-instant due to Docker's layer caching.

```bash
docker compose up
```

### Check if the application is working

#### Via automated tests

1. Install the test dependencies inside the running container:

```bash
docker exec -it flask_api poetry install --with test
```

2. Run the test suite:

```bash
docker exec -it flask_api poetry run pytest -rfsxE --capture=no --log-cli-level=DEBUG --maxfail=1 ./test
```

#### Via Web UI

1. Navigate to [http://localhost:5000/doc_to_pdf](http://localhost:5000/doc_to_pdf).
2. Select a local DOC or DOCX file (e.g. [dummy_doc.docx](./test/dummy_doc.docx)).
3. Click the Upload button.
4. Check that the resulting PDF either appears directly in the browser or starts downloading automatically.

## Dev mode

TODO

## Useful commands

1. Format code:

```bash
docker exec -it flask_api poetry install --with format
docker exec -it flask_api poetry run python ./tasks/format.py
```
