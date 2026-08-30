import os

from verification_pipeline import verification_pipeline


image_path = os.path.join(
    os.path.dirname(__file__),
    "..",
    "ocr",
    "test_data",
    "sample_certificate.png"
)


application = {
    "name": "Arun Kumar",
    "dob": "12/05/2006",
    "certificate_no": "SAMPLE12345"
}


result = verification_pipeline(
    application,
    "12th",
    image_path
)

print("\n----- FINAL AI VERIFICATION -----")
print("Status:", result["status"])
print("Message:", result["message"])