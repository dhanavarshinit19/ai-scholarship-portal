from multi_document_verification import verify_all_documents


application = {
    "10th": {
        "name": "Test Student",
        "dob": "01/01/2007",
        "certificate_no": "TEN001"
    },

    "12th": {
        "name": "Test Student",
        "dob": "01/01/2007",
        "certificate_no": "TEST12TH001"
    },

    "aadhaar": {
        "name": "Test Student",
        "dob": "01/01/2007",
        "aadhaar_no": "9999 8888 7777"
    },

    "income": {
        "name": "Test Student",
        "income": "250000",
        "certificate_no": "TESTINC001"
    },

    "community": {
        "name": "Test Student",
        "community": "Sample Community",
        "certificate_no": "COM001"
    }
}


documents = {
    "10th": "ai/ocr/test_data/sample_10th.png",
    "12th": "ai/ocr/test_data/sample_12th.png",
    "aadhaar": "ai/ocr/test_data/sample_aadhaar.png",
    "income": "ai/ocr/test_data/sample_income.png",
    "community": "ai/ocr/test_data/sample_community.png"
}


overall, results = verify_all_documents(
    application,
    documents
)


print("\n----- MULTI DOCUMENT VERIFICATION -----")

for document_type, result in results.items():
    print(f"\n{document_type.upper()}")
    print("Status:", result["status"])
    print("Message:", result["message"])


print("\n----- OVERALL RESULT -----")
print("Status:", overall)