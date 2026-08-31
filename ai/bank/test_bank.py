from bank_verification import verify_bank_details


application = {
    "name": "Test Student",
    "account_number": "123456789012",
    "ifsc_code": "SBIN0001234"
}

bank_details = {
    "name": "Test Student",
    "account_number": "123456789012",
    "ifsc_code": "SBIN0001234"
}

result = verify_bank_details(application, bank_details)

print("----- BANK DETAILS VERIFICATION -----")
print("Status:", result["status"])
print("Message:", result["message"])