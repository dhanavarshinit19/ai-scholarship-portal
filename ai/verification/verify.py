import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "ocr"))

from ocr import extract_text, extract_details
from document_rules import get_required_fields


def verify_document(application, document, document_type):
    fields = get_required_fields(document_type)

    if not fields:
        return {
            "status": "REJECTED",
            "message": "Invalid document type. Please upload the correct document."
        }

    for field in fields:
        app_value = str(application.get(field, "")).strip().lower()
        doc_value = str(document.get(field, "")).strip().lower()

        if not app_value or not doc_value:
            return {
                "status": "REJECTED",
                "message": f"{field} is missing. Please reapply with the correct document."
            }

        if app_value != doc_value:
            return {
                "status": "REJECTED",
                "message": f"{field} mismatch. Please reapply with the correct document."
            }

    return {
        "status": "ACCEPTED",
        "message": "All document details are verified successfully."
    }


def verify_certificate(application, image_path, document_type):
    text = extract_text(image_path)
    document = extract_details(text)

    return verify_document(application, document, document_type)


if __name__ == "__main__":
    print("AI Verification module ready.")