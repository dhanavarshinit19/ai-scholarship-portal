import os
from verify import verify_certificate, verify_document

PROJECT_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

image_path = os.path.join(
    PROJECT_DIR,
    "ai",
    "ocr",
    "test_data",
    "sample_10th.png"
)

application = {
    "name": "Test Student",
    "dob": "01/01/2007",
    "certificate_no": "TEN001"
}

print("----- TEST 1: CORRECT DETAILS -----")
result = verify_certificate(
    application, image_path, "10th"
)
print(result)

print("\n----- TEST 2: WRONG NAME -----")
wrong_application = {
    "name": "Wrong Student",
    "dob": "01/01/2007",
    "certificate_no": "TEN001"
}

result = verify_certificate(
    wrong_application, image_path, "10th"
)
print(result)

print("\n----- TEST 3: MISSING OCR FIELD -----")
document = {
    "name": "Test Student",
    "dob": None,
    "certificate_no": "TEN001"
}

result = verify_document(
    application, document, "10th"
)
print(result)
