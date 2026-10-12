import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "ocr"))

from ocr import extract_text, extract_details
from verify import verify_document
from document_validator import validate_document_type


def verification_pipeline(application, document_type, image_path):
    text = extract_text(image_path)

    type_result = validate_document_type(document_type, text)

    if type_result["status"] == "REJECTED":
        return type_result

    document = extract_details(text)

    return verify_document(application, document,document_type)


if __name__ == "__main__":
    print("AI Verification Pipeline ready.")