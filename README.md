<h1 align="center"><a href="https://paguiar.link/baileys-quickstart">Doc to PDF API</a></h1>

<p align="center">
    <br>
  <a href="https://pixabay.com/vectors/pdf-document-documents-pdf-file-4919559/">
    <img src="https://cdn.pixabay.com/photo/2020/03/10/17/02/pdf-4919559_960_720.png" width="120px" height="120px"/>
  </a>
  <br><br>
  Simple Flask API to convert DOC(X) to PDF
  <br>
</p>

<br>

## QuickStart

Install Docker and Docker Compose on your machine, and run the following command inside the project directory:

```sh
docker compose up
```

Docker compose will take a while to boot because "libreoffice" is a rather large dependency.

Flask will autoreload every time you save mre/main.py

```curl
python client.py
```