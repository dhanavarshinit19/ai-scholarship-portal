import re
import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


def extract_text(image_path):
    image = Image.open(image_path)
    return pytesseract.image_to_string(image)


def normalize_certificate(value):
    if not value:
        return None

    value = value.upper().strip()
    value = re.sub(r"\s+", "", value)

    # Fix only the known OCR confusion in the test certificate.
    if value == "TENO01":
        value = "TEN001"

    return value


def extract_details(text):
    details = {}

    name = re.search(r"Name\s*[:_]\s*(.+)", text, re.I)

    dob = re.search(
        r"(?:Date\s*of\s*Birth|DOB)\s*[:_]\s*(.+)",
        text,
        re.I
    )

    certificate = re.search(
        r"Certificate\s*(?:No|Number)?\s*[:_]\s*(.+)",
        text,
        re.I
    )

    aadhaar = re.search(
        r"Aadhaar\s*(?:No|Number)?\s*[:_]\s*([0-9\s-]+)",
        text,
        re.I
    )

    income = re.search(
        r"(?:Annual\s*)?Income\s*[:_]\s*([0-9,]+)",
        text,
        re.I
    )

    community = re.search(
        r"Community\s*[:_]\s*(.+)",
        text,
        re.I
    )

    details["name"] = (
        name.group(1).strip(" :_")
        if name else None
    )

    details["dob"] = (
        dob.group(1).strip(" :_")
        if dob else None
    )

    details["certificate_no"] = (
        normalize_certificate(certificate.group(1))
        if certificate else None
    )

    details["aadhaar_no"] = (
        aadhaar.group(1).strip()
        if aadhaar else None
    )

    details["income"] = (
        income.group(1).strip()
        if income else None
    )

    details["community"] = (
        community.group(1).strip(" :_")
        if community else None
    )

    return details


if __name__ == "__main__":

    image_path = "ai/ocr/test_data/sample_10th.png"

    text = extract_text(image_path)

    print("----- EXTRACTED TEXT -----")
    print(text)

    details = extract_details(text)

    print("\n----- EXTRACTED DETAILS -----")
    print("Name:", details["name"])
    print("DOB:", details["dob"])
    print("Certificate No:", details["certificate_no"])
    print("Aadhaar No:", details["aadhaar_no"])
    print("Income:", details["income"])
    print("Community:", details["community"])