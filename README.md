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

## QuickStart

> **Note**: You'll need to have the latest version of the [Docker Engine](https://docs.docker.com/engine/install/) and [Docker Compose](https://docs.docker.com/compose/install/) installed on your machine

1. Clone the repository and cd into it:

```
git clone https://github.com/codespearhead/doc-to-file-api
cd doc-to-file-api
```

2. Spin up the API 

> **Note**: The container will take a while to boot because "libreoffice" is a rather large dependency. Luckily, Flask's built-in web server will auto-reload the Flask app once changes are made to the server.py and saved, since the Flask app's running in debug mode.

```
docker compose up
```

3. Check if the API is working:

3.1. (Automated testing)

```bash
# 3.1.1 - Install test dependencies
docker exec -it flask_api poetry install --with test
# 3.1.2 - Run test suite
docker exec -it flask_api poetry run pytest -rfsxE --capture=no --log-cli-level=DEBUG --maxfail=1 ./test
```

3.2. (UI) Go to [http://localhost:5000/doc_to_pdf](http://localhost:5000/doc_to_pdf), select a local DOC or DOCX file, such as the one in ./test/dummy_doc.docx, then press `upload` and see whether a PDF file is either displayed on the browser or downloaded automatically.

## Dev mode

A.0 - Prerequisites

1 - Make sure you have a supported Python version (see property "requires-python" in [pyproject.toml](./pyproject.toml)) available on your machine:

```bash
python --version
```

2 - Create a Virtual Enviroment:

```bash
python -m venv .venv
```

3 - Activate it:

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

4 - Make sure it's actually enabled:

```bash
PYTHON_PATH=$(which python)
if [[ "$PYTHON_PATH" == *".venv"* ]]; then
  echo "Python is using a .venv environment: $PYTHON_PATH"
else
  echo "Python is NOT using a .venv environment: $PYTHON_PATH"
fi
```

5 - Instale o gerenciador de dependências Poetry:

```bash
pip install poetry
```

6 - Install all the project dependency groups:

```bash
poetry install --with format,test
```


```bash
poetry run python ./entrypoint/main.py
```

```bash
poetry run python ./tasks/format.py
```
