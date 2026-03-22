import os
from pathlib import Path
from typing import List
from typing import Tuple
import zipfile
import pypdfium2 as pdfium
import requests
from PIL import Image
from pypdfium2._helpers.bitmap import PdfBitmap


# [09301be5-a035-4d7f-82f3-f4502070da58] DOCX files are ZIP archives with a specific structure. This creates a fake DOCX (valid ZIP but missing required files), which reliably triggers a conversion failure.
def helper_function__create_invalid_docx_file(
    file_path: str,
):
    with zipfile.ZipFile(file_path, "w") as zf:
        zf.writestr("[Content_Types].xml", "")
        zf.writestr("_rels/.rels", "")
    return file_path


def helper_function__render_pdf_pages(
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


def helper_function__assert_generated_pdf_matches_expected(
    actual_pdf_path: str,
    expected_pdf_path: str,
    temp_dir: str,
) -> None:
    expected_pages = helper_function__render_pdf_pages(
        prefix="expected",
        pdf_path=expected_pdf_path,
        temp_dir=temp_dir,
    )
    actual_pages = helper_function__render_pdf_pages(
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


def helper_function__save_response_pdf(
    response: requests.Response, output_path: str
) -> None:
    with open(output_path, "wb") as f:
        chunk_size = 2000
        for chunk in response.iter_content(chunk_size):
            f.write(chunk)
