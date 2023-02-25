import requests

endpoint = "http://localhost:5000/doc_to_pdf"
path_to_doc = './mre/dummy_doc.docx'
chunk_size = 2000

r = requests.post(endpoint, files={
    'file': open(path_to_doc, 'rb'),
})

with open('output.pdf', 'wb') as fd:
    for chunk in r.iter_content(chunk_size):
        fd.write(chunk)
