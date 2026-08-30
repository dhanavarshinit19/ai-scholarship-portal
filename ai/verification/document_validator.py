def validate_document_type(document_type, text):
    text = text.lower()

    keywords = {
        "10th": ["10th", "tenth", "secondary"],
        "12th": ["12th", "twelfth", "higher secondary"],
        "aadhaar": ["aadhaar", "aadhar", "uidai"],
        "income": ["income certificate", "annual income"],
        "community": ["community certificate", "community"]
    }

    if document_type not in keywords:
        return {
            "status": "REJECTED",
            "message": "Unknown document type."
        }

    for keyword in keywords[document_type]:
        if keyword in text:
            return {
                "status": "ACCEPTED",
                "message": f"{document_type} document type verified."
            }

    return {
        "status": "REJECTED",
        "message": f"Uploaded document is not a valid {document_type} document. Please reapply with the correct document."
    }