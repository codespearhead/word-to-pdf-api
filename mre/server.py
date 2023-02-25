from os import remove
from random import randint
from subprocess import check_output
from flask import Flask, request, jsonify, send_file

app = Flask(__name__)

@app.route('/doc_to_pdf', methods = ['POST'])
def upload_file():
    filename = randint(0,1000)
    filename = {
        'docx': f'{filename}.docx',
        'pdf': f'{filename}.pdf'
    }
    if 'file' not in request.files:
        resp = jsonify({'message' : 'No file part in the request'})
        resp.status_code = 400
        return resp
    file = request.files['file']
    if file.filename == '':
        resp = resp = jsonify({'message' : 'No file selected for uploading'})
        resp.status_code = 400
        return resp
    if file and request.method == 'POST':
        try:
            file.save(filename["docx"])
            check_output(['libreoffice', '--headless', '--convert-to', 'pdf' , filename["docx"]])
            return send_file(filename["pdf"], download_name=filename["pdf"])
        except Exception as e:
            return str(e)
        finally:
            for key in filename: remove(filename[key])

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5000, debug=True)