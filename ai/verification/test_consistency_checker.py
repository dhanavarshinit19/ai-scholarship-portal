from consistency_checker import check_document_consistency

documents = {
    "10th": {
        "name": "Test Student",
        "dob": "01/01/2007"
    },
    "12th": {
        "name": "Test Student",
        "dob": "01/01/2007"
    }
}

print("MATCHING DOCUMENTS")
print(check_document_consistency(documents))

wrong_documents = {
    "10th": {
        "name": "Test Student",
        "dob": "01/01/2007"
    },
    "12th": {
        "name": "Wrong Student",
        "dob": "01/01/2007"
    }
}

print("\nMISMATCHING DOCUMENTS")
print(check_document_consistency(wrong_documents))
