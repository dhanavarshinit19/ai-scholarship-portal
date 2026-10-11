
import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.abspath(
    os.path.join(CURRENT_DIR, "..", "..")
)
OCR_DIR = os.path.join(PROJECT_DIR, "ai", "ocr")

sys.path.insert(0, OCR_DIR)
sys.path.insert(0, CURRENT_DIR)

from ocr import extract_text, extract_details
from document_rules import (
    get_required_fields,
    get_application_fields
)
from consistency_checker import check_document_consistency


def normalize_value(value):
    if value is None:
        return ""

    return " ".join(str(value).strip().lower().split())



def verify_document(application, document, document_type):
    document_type = document_type.lower().strip()

    required_fields = get_required_fields(document_type)
    application_fields = get_application_fields(document_type)

    if not required_fields or not application_fields:
        return {
            "status": "REJECTED",
            "message": (
                "Invalid document type. "
                "Please upload the correct document."
            )
        }

    for field in required_fields:
        application_field = application_fields[field]

        app_value = application.get(application_field)

        # Backward compatibility for older tests and callers
        if not app_value and field == "certificate_no":
            app_value = application.get("certificate_no")

        app_value = normalize_value(app_value)
        doc_value = normalize_value(document.get(field))

        if not app_value:
            return {
                "status": "REJECTED",
                "message": (
                    f"{application_field} is missing from the application. "
                    "Please correct the application details."
                )
            }

        if not doc_value:
            return {
                "status": "REVIEW_REQUIRED",
                "message": (
                    f"{field} could not be extracted from the "
                    f"{document_type} document. "
                    "Please upload a clearer document or request review."
                )
            }

        if app_value != doc_value:
            return {
                "status": "REJECTED",
                "message": (
                    f"{field} mismatch in {document_type}. "
                    "Please correct the details and re-upload."
                )
            }

    return {
        "status": "ACCEPTED",
        "message": (
            f"Required details in the {document_type} "
            "document match the application."
        )
    }


def verify_certificate(application, image_path, document_type):
    if not os.path.isfile(image_path):
        return {
            "status": "REVIEW_REQUIRED",
            "message": "Document image not found. Please upload it again."
        }

    try:
        text = extract_text(image_path)

        if not text or not text.strip():
            return {
                "status": "REVIEW_REQUIRED",
                "message": (
                    "Could not read the document. "
                    "Please upload a clearer image."
                )
            }

        document = extract_details(text)

    except Exception:
        return {
            "status": "REVIEW_REQUIRED",
            "message": "Document processing failed. Please review the upload."
        }

    return verify_document(application, document, document_type)


def verify_multiple_certificates(application, document_paths):
    if not isinstance(document_paths, dict) or not document_paths:
        return {
            "status": "REJECTED",
            "message": "No documents were provided.",
            "document_results": {},
            "mismatches": []
        }

    extracted_documents = {}
    document_results = {}

    for document_type, image_path in document_paths.items():
        document_type = document_type.lower().strip()

        if document_type in extracted_documents:
            return {
                "status": "REJECTED",
                "message": f"Duplicate document type: {document_type}.",
                "document_results": document_results,
                "mismatches": []
            }

        if not get_required_fields(document_type):
            return {
                "status": "REJECTED",
                "message": f"Invalid document type: {document_type}.",
                "document_results": document_results,
                "mismatches": []
            }

        result_document = verify_certificate(
            application,
            image_path,
            document_type
        )

        document_results[document_type] = result_document

        if result_document["status"] != "ACCEPTED":
            return {
                "status": result_document["status"],
                "message": result_document["message"],
                "document_results": document_results,
                "mismatches": []
            }

        text = extract_text(image_path)
        extracted_documents[document_type] = extract_details(text)

    consistency_result = check_document_consistency(
        extracted_documents
    )

    if consistency_result["status"] != "ACCEPTED":
        return {
            "status": consistency_result["status"],
            "message": consistency_result["message"],
            "document_results": document_results,
            "mismatches": consistency_result.get("mismatches", [])
        }

    return {
        "status": "ACCEPTED",
        "message": (
            "All required document details match the application, "
            "and available common details are consistent. "
            "Document authenticity has not been independently confirmed."
        ),
        "document_results": document_results,
        "mismatches": [],
        "extracted_documents": extracted_documents
    }


if __name__ == "__main__":
    print("AI Verification module ready.")
