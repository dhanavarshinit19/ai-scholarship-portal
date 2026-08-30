import os
from verification_pipeline import verification_pipeline


def verify_all_documents(application, documents):
    results = {}

    for document_type, image_path in documents.items():

        if not os.path.exists(image_path):
            results[document_type] = {
                "status": "REJECTED",
                "message": f"{document_type} document is missing. Please upload and reapply."
            }
            continue

        document_application = application.get(document_type, {})

        results[document_type] = verification_pipeline(
            document_application,
            document_type,
            image_path
        )

    overall = (
        "ACCEPTED"
        if results and all(
            result["status"] == "ACCEPTED"
            for result in results.values()
        )
        else "REJECTED"
    )

    return overall, results