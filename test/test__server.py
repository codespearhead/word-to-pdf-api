import os
from pathlib import Path
import shutil
from typing import List
from typing import Tuple
from typing import Generator
import pytest
from _pytest.fixtures import FixtureRequest
import pypdfium2 as pdfium
import requests
from PIL import Image
from pypdfium2._helpers.bitmap import PdfBitmap


base_dir = os.path.dirname(__file__)


@pytest.fixture(scope="function")
def temp_dir(request: FixtureRequest) -> Generator[str, None, None]:
    path = os.path.join(base_dir, "test_output", request.node.name)
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)

    yield path


endpoint = "http://localhost:5000/doc_to_pdf"


def render_pdf_pages(
    pdf_path: str, prefix: str, temp_dir: str, scale: int = 2
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


def test_doc_to_pdf_success(temp_dir: str):
    input_file = os.path.join(base_dir, "dummy_doc.docx")
    expected_file = os.path.join(base_dir, "dummy_doc.pdf")
    actual_file = os.path.join(temp_dir, "output.pdf")

    with open(input_file, "rb") as f:
        response = requests.post(endpoint, files={"file": f})

    assert response.status_code == 200

    content_type = response.headers.get("content-type", "")
    assert "application/pdf" in content_type

    with open(actual_file, "wb") as f:
        chunk_size = 2000
        for chunk in response.iter_content(chunk_size):
            f.write(chunk)

    expected_pages = render_pdf_pages(
        prefix="expected",
        pdf_path=expected_file,
        temp_dir=temp_dir,
    )
    actual_pages = render_pdf_pages(
        prefix="actual",
        pdf_path=actual_file,
        temp_dir=temp_dir,
    )

    assert len(actual_pages) == len(expected_pages), (
        f"Page count mismatch: actual={len(actual_pages)}, expected={len(expected_pages)}; "
        f"actual_pdf={actual_file}; expected_pdf={expected_file}"
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
