import re


def verify_bank_details(application, bank_details):
    errors = []

    expected_account = str(application.get("account_number", "")).strip()
    expected_ifsc = str(application.get("ifsc_code", "")).strip().upper()
    expected_name = str(application.get("name", "")).strip().lower()

    actual_account = str(bank_details.get("account_number", "")).strip()
    actual_ifsc = str(bank_details.get("ifsc_code", "")).strip().upper()
    actual_name = str(bank_details.get("name", "")).strip().lower()

    if not actual_account:
        errors.append("Account number is missing.")
    elif not re.fullmatch(r"\d{9,18}", actual_account):
        errors.append("Invalid account number.")

    if not actual_ifsc:
        errors.append("IFSC code is missing.")
    elif not re.fullmatch(r"[A-Z]{4}0[A-Z0-9]{6}", actual_ifsc):
        errors.append("Invalid IFSC code.")

    if expected_account and actual_account != expected_account:
        errors.append("Account number mismatch.")

    if expected_ifsc and actual_ifsc != expected_ifsc:
        errors.append("IFSC code mismatch.")

    if expected_name and actual_name != expected_name:
        errors.append("Account holder name mismatch.")

    if errors:
        return {
            "status": "REJECTED",
            "message": " ".join(errors)
        }

    return {
        "status": "ACCEPTED",
        "message": "Bank details verified successfully."
    }