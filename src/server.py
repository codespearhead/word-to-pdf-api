import os
from tempfile import NamedTemporaryFile
from subprocess import run
from flask import Flask, request, jsonify, send_file

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


@app.route("/doc_to_pdf", methods=["GET", "POST"])
def upload_file():
    if request.method == "GET":
        return """
        <!doctype html>
        <head>
            <meta charset="utf-8">
            <title>Convert Microsoft Word (DOC/DOCX) to PDF</title>
        </head>
        <body>
            <h1>Upload new File</h1>

            <form id="upload-form" method="post" enctype="multipart/form-data">
                <label for="file_input">Choose a file:</label>
                <input id="file_input" type="file" name="file" required>

                <button id="submit_form" type="submit">Upload</button>
            </form>
        </body>
        </html>
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

        result = run(
            [
                "libreoffice",
                "--headless",
                "--convert-to",
                "pdf",
                "--outdir",
                BASE_DIR,
                docx_file.name,
            ],
            capture_output=True,
            text=True,
            check=True,
        )

        if not os.path.exists(pdf_path):
            return (
                jsonify(
                    {
                        "message": "PDF was not generated. Verify that the input is a valid DOCX file.",
                        "stdout": result.stdout,
                        "stderr": result.stderr,
                    }
                ),
                500,
            )

        return send_file(
            pdf_path,
            download_name=os.path.basename(pdf_path),
            as_attachment=True,
        )

    except Exception as e:
        return jsonify({"message": "Conversion failed", "error": str(e)}), 500

    finally:
        if os.path.exists(docx_file.name):
            os.remove(docx_file.name)
        if os.path.exists(pdf_path):
            os.remove(pdf_path)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
