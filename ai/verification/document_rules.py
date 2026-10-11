
DOCUMENT_RULES = {
    "10th": {
        "required_fields": ["name", "dob", "certificate_no"],
        "application_fields": {
            "name": "name",
            "dob": "dob",
            "certificate_no": "10th_certificate_no"
        }
    },
    "12th": {
        "required_fields": ["name", "dob", "certificate_no"],
        "application_fields": {
            "name": "name",
            "dob": "dob",
            "certificate_no": "12th_certificate_no"
        }
    },
    "aadhaar": {
        "required_fields": ["name", "dob", "aadhaar_no"],
        "application_fields": {
            "name": "name",
            "dob": "dob",
            "aadhaar_no": "aadhaar_no"
        }
    },
    "income": {
        "required_fields": ["name", "income", "certificate_no"],
        "application_fields": {
            "name": "name",
            "income": "income",
            "certificate_no": "income_certificate_no"
        }
    },
    "community": {
        "required_fields": ["name", "community", "certificate_no"],
        "application_fields": {
            "name": "name",
            "community": "community",
            "certificate_no": "community_certificate_no"
        }
    }
}


def get_required_fields(document_type):
    document_type = document_type.lower().strip()

    if document_type not in DOCUMENT_RULES:
        return None

    return DOCUMENT_RULES[document_type]["required_fields"]


def get_application_fields(document_type):
    document_type = document_type.lower().strip()

    if document_type not in DOCUMENT_RULES:
        return None

    return DOCUMENT_RULES[document_type]["application_fields"]
