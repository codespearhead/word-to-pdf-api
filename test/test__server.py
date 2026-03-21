import os
from pathlib import Path
import shutil
from typing import List
from typing import Tuple
from typing import Generator
import zipfile
import pytest
from _pytest.fixtures import FixtureRequest
import pypdfium2 as pdfium
import requests
from PIL import Image
from pypdfium2._helpers.bitmap import PdfBitmap


base_dir = os.path.dirname(__file__)
endpoint = "http://127.0.0.1:5000/doc_to_pdf"


@pytest.fixture(scope="function")
def temp_dir(request: FixtureRequest) -> Generator[str, None, None]:
    path = os.path.join(base_dir, "test_output", request.node.name)
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)

    yield path


def render_pdf_pages(
    pdf_path: str,
    prefix: str,
    temp_dir: str,
    scale: int = 2,
) -> List[Tuple[Image.Image, str]]:
    pdf = pdfium.PdfDocument(pdf_path)
    pages: List[Tuple[Image.Image, str]] = []

    for index in range(len(pdf)):
        page = pdf[index]
        bitmap: PdfBitmap = page.render(scale=scale)
        image: Image.Image = bitmap.to_pil()

        output_path = os.path.join(temp_dir, f"{prefix}_page_{index + 1}.png")
        image.save(output_path)

        pages.append((image, output_path))

    return pages


def assert_generated_pdf_matches_expected(
    actual_pdf_path: str,
    expected_pdf_path: str,
    temp_dir: str,
) -> None:
    expected_pages = render_pdf_pages(
        prefix="expected",
        pdf_path=expected_pdf_path,
        temp_dir=temp_dir,
    )
    actual_pages = render_pdf_pages(
        prefix="actual",
        pdf_path=actual_pdf_path,
        temp_dir=temp_dir,
    )

    assert len(actual_pages) == len(expected_pages), (
        f"Page count mismatch: actual={len(actual_pages)}, expected={len(expected_pages)}; "
        f"actual_pdf={actual_pdf_path}; expected_pdf={expected_pdf_path}"
    )

    for (actual_image, actual_image_path), (expected_image, expected_image_path) in zip(
        actual_pages,
        expected_pages,
    ):
        actual_name = Path(actual_image_path).name
        expected_name = Path(expected_image_path).name

        actual_bytes = actual_image.tobytes()
        expected_bytes = expected_image.tobytes()

        if actual_bytes != expected_bytes:
            raise AssertionError(
                f"Rendered page differs from expected output; "
                f"actual_image={actual_name}; expected_image={expected_name}; "
            )


def save_response_pdf(response: requests.Response, output_path: str) -> None:
    with open(output_path, "wb") as f:
        chunk_size = 2000
        for chunk in response.iter_content(chunk_size):
            f.write(chunk)


def test__api__missing_file_in_request():
    response = requests.post(endpoint)

    assert response.status_code == 400

    content_type = response.headers.get("content-type", "")
    assert "application/json" in content_type

    data = response.json()
    assert data.get("message") == "No file part in the request"


def test__api__invalid_file_in_request(temp_dir: str):
    invalid_file = os.path.join(temp_dir, "invalid.docx")

    # [09301be5-a035-4d7f-82f3-f4502070da58] DOCX files are ZIP archives with a specific structure. This creates a fake DOCX (valid ZIP but missing required files), which reliably triggers a conversion failure.
    with zipfile.ZipFile(invalid_file, "w") as zf:
        zf.writestr("[Content_Types].xml", "")
        zf.writestr("_rels/.rels", "")

    with open(invalid_file, "rb") as f:
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

    save_response_pdf(response, actual_file)

    assert_generated_pdf_matches_expected(
        actual_pdf_path=actual_file,
        expected_pdf_path=expected_file,
        temp_dir=temp_dir,
    )
