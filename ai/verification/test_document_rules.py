from document_rules import get_required_fields


document_types = ["10th", "12th", "aadhaar", "income", "community"]

for document_type in document_types:
    fields = get_required_fields(document_type)

    print(f"\n{document_type.upper()} DOCUMENT")
    print("Required fields:", fields)