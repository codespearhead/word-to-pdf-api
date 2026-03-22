import logging
import os
import shutil
import zipfile
import pytest
from typing import Generator
from _pytest.fixtures import FixtureRequest
from playwright.sync_api import Page, expect
from test.util import helper_function__assert_generated_pdf_matches_expected


logger = logging.getLogger(__name__)

base_dir = os.path.dirname(__file__)
endpoint = "http://127.0.0.1:5000/doc_to_pdf"


@pytest.fixture(scope="function")
def temp_dir(request: FixtureRequest) -> Generator[str, None, None]:
    path = os.path.join(base_dir, "test_output", request.node.name)
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)

    yield path


FILE_INPUT__XPATH = """
//input[
    @id='file_input'
    and @type='file'
]
"""
SUBMIT_BUTTON__XPATH = """
//button[
    @id='submit_form'
    and @type='submit'
]
"""


def test__web_ui__file_input_and_submit_button_are_visible(page: Page) -> None:
    page.goto(endpoint)

    submit_button = page.locator(f"xpath={FILE_INPUT__XPATH}")
    file_input = page.locator(f"xpath={FILE_INPUT__XPATH}")

    expect(file_input).to_be_visible()
    expect(file_input).to_be_enabled()
    expect(file_input).to_have_attribute("required", "")

    expect(submit_button).to_be_visible()
    expect(submit_button).to_be_enabled()


def test__web_ui__invalid_file_in_request(
    page: Page,
    temp_dir: str,
) -> None:
    invalid_file = os.path.join(temp_dir, "invalid.docx")

    # [09301be5-a035-4d7f-82f3-f4502070da58]
    with zipfile.ZipFile(invalid_file, "w") as zf:
        zf.writestr("[Content_Types].xml", "")
        zf.writestr("_rels/.rels", "")

    page.goto(endpoint)

    file_input = page.locator(f"xpath={FILE_INPUT__XPATH}")
    file_input.set_input_files(invalid_file)

    submit_button = page.locator(f"xpath={SUBMIT_BUTTON__XPATH}")
    submit_button.click()

    error_message = page.locator(
        "text=PDF was not generated. Verify that the input is a valid DOCX file."
    )

    expect(error_message).to_be_visible()


def test__web_ui__pdf_generated_successfully(
    page: Page,
    temp_dir: str,
) -> None:
    input_file = os.path.join(base_dir, "dummy_doc.docx")
    expected_file = os.path.join(base_dir, "dummy_doc.pdf")
    actual_file = os.path.join(temp_dir, "output.pdf")

    page.goto(endpoint)

    file_input = page.locator(f"xpath={FILE_INPUT__XPATH}")
    file_input.set_input_files(input_file)

    submit_button = page.locator(f"xpath={SUBMIT_BUTTON__XPATH}")

    with page.expect_download() as download_info:
        submit_button.click()

    download = download_info.value
    download.save_as(actual_file)

    helper_function__assert_generated_pdf_matches_expected(
        actual_pdf_path=actual_file,
        expected_pdf_path=expected_file,
        temp_dir=temp_dir,
    )
