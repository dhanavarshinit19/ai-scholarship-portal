import os
from correction_workflow import reverify_after_correction

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

wrong_application = {
    "name": "Wrong Student",
    "dob": "01/01/2007",
    "certificate_no": "TEN001"
}

first_result = reverify_after_correction(
    wrong_application,
    image_path,
    "10th"
)

print("----- FIRST SUBMISSION -----")
print(first_result)

corrected_application = {
    "name": "Test Student",
    "dob": "01/01/2007",
    "certificate_no": "TEN001"
}

second_result = reverify_after_correction(
    corrected_application,
    image_path,
    "10th",
    previous_result=first_result
)

print("\n----- CORRECTED SUBMISSION -----")
print(second_result)
