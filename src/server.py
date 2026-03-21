import os
from random import randint
from subprocess import check_output
from flask import Flask, request, jsonify, send_file

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


@app.route("/doc_to_pdf", methods=["GET", "POST"])
def upload_file():
    if request.method == "GET":
        return """
        <!doctype html>
        <title>Upload new File</title>
        <h1>Upload new File</h1>
        <form method=post enctype=multipart/form-data>
        <input type=file name=file>
        <input type=submit value=Upload>
        </form>
        """

    filename = randint(0, 1000)
    filename = {
        "docx": os.path.join(BASE_DIR, f"{filename}.docx"),
        "pdf": os.path.join(BASE_DIR, f"{filename}.pdf"),
    }
    if "file" not in request.files:
        resp = jsonify({"message": "No file part in the request"})
        resp.status_code = 400
        return resp
    file = request.files["file"]
    if file.filename == "":
        resp = resp = jsonify({"message": "No file selected for uploading"})
        resp.status_code = 400
        return resp
    if file and request.method == "POST":
        try:
            file.save(filename["docx"])
            check_output(
                [
                    "libreoffice",
                    "--headless",
                    "--convert-to",
                    "pdf",
                    "--outdir",
                    BASE_DIR,
                    filename["docx"],
                ]
            )
            return send_file(filename["pdf"], download_name=filename["pdf"])
        except Exception as e:
            return str(e)
        finally:
            for key in filename:
                os.path.remove(filename[key])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
