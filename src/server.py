import os
from tempfile import NamedTemporaryFile
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

    if "file" not in request.files:
        return jsonify({"message": "No file part in the request"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"message": "No file selected for uploading"}), 400

    docx_file = NamedTemporaryFile(delete=False, suffix=".docx", dir=BASE_DIR)
    pdf_path = f"{docx_file.name[:-5]}.pdf"

    try:
        file.save(docx_file.name)
        docx_file.close()

        check_output(
            [
                "libreoffice",
                "--headless",
                "--convert-to",
                "pdf",
                "--outdir",
                BASE_DIR,
                docx_file.name,
            ],
        )

        return send_file(
            pdf_path,
            download_name=os.path.basename(pdf_path),
            as_attachment=True,
        )

    except Exception as e:
        return str(e)

    finally:
        if os.path.exists(docx_file.name):
            os.remove(docx_file.name)
        if os.path.exists(pdf_path):
            os.remove(pdf_path)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
