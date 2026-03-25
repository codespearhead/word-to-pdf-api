<h1 align="center"><a href="https://github.com/codespearhead/word-to-pdf-api">Word to PDF API</a></h1>

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

### Prerequisites

1. Complete the Quickstart and ensure the server is already up and running.

> **Note**: Since Flask is running in debug mode, the server will automatically reload whenever changes are saved to [server.py](./src/server.py).

2. Ensure you have the latest stable version of Python installed:

```bash
python --version
```

### Local Environment Setup

1. Create a Virtual Enviroment:

```bash
python -m venv .venv
```

2. Activate the Virtual Enviroment:

```bash
activate_venv() {
    if [[ $(uname) == "Darwin" ]]; then
        source .venv/bin/activate
    elif [[ $(uname) == "Linux" ]]; then
        source .venv/bin/activate
    elif [[ $(uname) == CYGWIN* || $(uname) == MINGW* ]]; then
        source .venv/Scripts/activate
    else
        echo "Unsupported operating system"
    fi
}

activate_venv
```

3. Ensure the Virtual Enviroment is active:

```bash
PYTHON_PATH=$(which python)
if [[ "$PYTHON_PATH" == *".venv"* ]]; then
  echo "Python is using a .venv environment: $PYTHON_PATH"
else
  echo "Python is NOT using a .venv environment: $PYTHON_PATH"
fi
```

4. Install the Poetry package manager:

```bash
pip install poetry
```

5. Install the project dependencies from all dependency groups:

```bash
poetry install --with test,format
```

6. The test and task commands will now run without the `docker exec -it flask_api` prefix.


## Useful commands

#### Code Formatting

1. Install the required dependencies inside the running container:

```bash
docker exec -it flask_api poetry install --with format
```

2. Run the formatting task:

```bash
docker exec -it flask_api poetry run python ./tasks/format.py
```
