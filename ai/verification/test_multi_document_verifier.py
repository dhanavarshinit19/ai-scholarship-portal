import os
from multi_document_verifier import verify_multiple_documents

PROJECT_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

TEST_DIR = os.path.join(
    PROJECT_DIR, "ai", "ocr", "test_data"
)

documents = {
    "10th": os.path.join(TEST_DIR, "sample_10th.png"),
    "12th": os.path.join(TEST_DIR, "sample_12th.png"),
    "aadhaar": os.path.join(TEST_DIR, "sample_aadhaar.png"),
    "community": os.path.join(TEST_DIR, "sample_community.png"),
    "income": os.path.join(TEST_DIR, "sample_income.png"),
}

result = verify_multiple_documents(documents)

print("----- MULTI-DOCUMENT VERIFICATION -----")
print("Status:", result["status"])
print("Message:", result["message"])

print("\n----- EXTRACTED DETAILS -----")
for document_type, details in result.get(
    "extracted_documents", {}
).items():
    print(f"\n{document_type.upper()}:")
    for field, value in details.items():
        print(f"  {field}: {value}")

print("\n----- MISMATCHES -----")
for mismatch in result.get("mismatches", []):
    print(mismatch)
