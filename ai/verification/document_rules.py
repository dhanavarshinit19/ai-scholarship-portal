DOCUMENT_RULES = {
    "10th": {
        "required_fields": ["name", "dob", "certificate_no"]
    },

    "12th": {
        "required_fields": ["name", "dob", "certificate_no"]
    },

    "aadhaar": {
        "required_fields": ["name", "dob", "aadhaar_no"]
    },

    "income": {
        "required_fields": ["name", "income", "certificate_no"]
    },

    "community": {
        "required_fields": ["name", "community", "certificate_no"]
    }
}


def get_required_fields(document_type):
    document_type = document_type.lower()

    if document_type not in DOCUMENT_RULES:
        return None

    return DOCUMENT_RULES[document_type]["required_fields"]