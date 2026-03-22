import os
import shutil
from typing import Generator
import pytest
from _pytest.fixtures import FixtureRequest
import requests

from test.util import (
    helper_function__assert_generated_pdf_matches_expected,
    helper_function__create_invalid_docx_file,
    helper_function__save_response_pdf,
)


base_dir = os.path.dirname(__file__)
endpoint = "http://127.0.0.1:5000/doc_to_pdf"


@pytest.fixture(scope="function")
def temp_dir(request: FixtureRequest) -> Generator[str, None, None]:
    path = os.path.join(base_dir, "test_output", request.node.name)
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)

    yield path


def test__api__missing_file_in_request():
    response = requests.post(endpoint)

    assert response.status_code == 400

    content_type = response.headers.get("content-type", "")
    assert "application/json" in content_type

    data = response.json()
    assert data.get("message") == "No file part in the request"


def test__api__invalid_file_in_request(temp_dir: str):
    invalid_file__path = helper_function__create_invalid_docx_file(
        file_path=os.path.join(temp_dir, "invalid.docx"),
    )

    with open(invalid_file__path, "rb") as f:
        response = requests.post(endpoint, files={"file": f})

    assert response.status_code == 500

    content_type = response.headers.get("content-type", "")
    assert "application/json" in content_type

    data = response.json()
    assert data.get("message") in {
        "Conversion failed",
        "PDF was not generated. Verify that the input is a valid DOCX file.",
    }


def test__api__pdf_generated_successfully(temp_dir: str):
    input_file = os.path.join(base_dir, "dummy_doc.docx")
    expected_file = os.path.join(base_dir, "dummy_doc.pdf")
    actual_file = os.path.join(temp_dir, "output.pdf")

    with open(input_file, "rb") as f:
        response = requests.post(endpoint, files={"file": f}, stream=True)

    assert response.status_code == 200

    content_type = response.headers.get("content-type", "")
    assert "application/pdf" in content_type

    helper_function__save_response_pdf(response, actual_file)

    helper_function__assert_generated_pdf_matches_expected(
        actual_pdf_path=actual_file,
        expected_pdf_path=expected_file,
        temp_dir=temp_dir,
    )
