import requests

files = {
    'file': open('./mre/dummy_doc.docx', 'rb'),
}

r = requests.post('http://localhost:5000/doc_to_pdf', files=files)

chunk_size = 2000
with open('output.pdf', 'wb') as fd:
    for chunk in r.iter_content(chunk_size):
        fd.write(chunk)