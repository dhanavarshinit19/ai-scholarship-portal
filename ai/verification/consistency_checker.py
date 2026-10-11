def normalize_value(value):
    if value is None:
        return ""

    return " ".join(str(value).lower().split())


def check_document_consistency(documents):
    """
    documents format:
    {
        "10th": {"name": "...", "dob": "..."},
        "12th": {"name": "...", "dob": "..."},
        "aadhaar": {"name": "...", "dob": "..."}
    }
    """

    if not isinstance(documents, dict) or len(documents) < 2:
        return {
            "status": "REJECTED",
            "message": "At least two documents are required.",
            "mismatches": []
        }

    fields_to_compare = ["name", "dob"]
    mismatches = []
    comparisons = 0

    document_items = list(documents.items())

    for i in range(len(document_items)):
        type_a, details_a = document_items[i]

        for j in range(i + 1, len(document_items)):
            type_b, details_b = document_items[j]

            if not isinstance(details_a, dict):
                continue

            if not isinstance(details_b, dict):
                continue

            for field in fields_to_compare:
                value_a = normalize_value(details_a.get(field))
                value_b = normalize_value(details_b.get(field))

                # Compare only when both documents contain the field.
                if not value_a or not value_b:
                    continue

                comparisons += 1

                if value_a != value_b:
                    mismatches.append({
                        "field": field,
                        "document_1": type_a,
                        "document_2": type_b,
                        "message": (
                            f"{field} mismatch between "
                            f"{type_a} and {type_b}."
                        )
                    })

    if mismatches:
        return {
            "status": "REJECTED",
            "message": (
                "Document details do not match. "
                "Please correct the details and re-upload."
            ),
            "mismatches": mismatches
        }

    if comparisons == 0:
        return {
            "status": "REVIEW_REQUIRED",
            "message": (
                "No common fields could be compared. "
                "Please review the extracted document details."
            ),
            "mismatches": []
        }

    return {
        "status": "ACCEPTED",
        "message": (
            "All available common document details match. "
            "This does not confirm document authenticity."
        ),
        "mismatches": []
    }
