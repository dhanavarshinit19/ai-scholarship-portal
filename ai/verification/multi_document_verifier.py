import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.abspath(
    os.path.join(CURRENT_DIR, "..", "..")
)
OCR_DIR = os.path.join(PROJECT_DIR, "ai", "ocr")

sys.path.insert(0, OCR_DIR)

from ocr import extract_text, extract_details
from consistency_checker import check_document_consistency
from document_rules import get_required_fields


def verify_multiple_documents(document_paths):
    if not isinstance(document_paths, dict) or len(document_paths) < 2:
        return {
            "status": "REJECTED",
            "message": "At least two documents are required.",
            "mismatches": []
        }

    extracted_documents = {}

    for document_type, image_path in document_paths.items():
        document_type = document_type.lower().strip()
        required_fields = get_required_fields(document_type)

        if not required_fields:
            return {
                "status": "REJECTED",
                "message": f"Unknown document type: {document_type}.",
                "mismatches": []
            }

        if not os.path.isfile(image_path):
            return {
                "status": "REVIEW_REQUIRED",
                "message": (
                    f"{document_type} image was not found. "
                    "Please upload the document again."
                ),
                "mismatches": []
            }

        try:
            text = extract_text(image_path)

            if not text or not text.strip():
                return {
                    "status": "REVIEW_REQUIRED",
                    "message": (
                        f"Could not read {document_type}. "
                        "Please upload a clearer image."
                    ),
                    "mismatches": []
                }

            details = extract_details(text)

        except Exception:
            return {
                "status": "REVIEW_REQUIRED",
                "message": (
                    f"Could not process {document_type}. "
                    "Please review the uploaded document."
                ),
                "mismatches": []
            }

        missing_fields = [
            field for field in required_fields
            if not details.get(field)
        ]

        if missing_fields:
            return {
                "status": "REVIEW_REQUIRED",
                "message": (
                    f"Could not extract required fields from "
                    f"{document_type}: {', '.join(missing_fields)}. "
                    "Please upload a clearer document or request review."
                ),
                "mismatches": []
            }

        extracted_documents[document_type] = details

    result = check_document_consistency(extracted_documents)
    result["extracted_documents"] = extracted_documents

    return result
