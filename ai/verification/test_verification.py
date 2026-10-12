from verify import verify_document


def test_correct_document():
    application = {
        "name": "Student",
        "dob": "01/01/2007",
        "certificate_no": "CERT001"
    }

    document = {
        "name": "Student",
        "dob": "01/01/2007",
        "certificate_no": "CERT001"
    }

    result = verify_document(application, document, "12th")

    print("\nTest 1 - Correct Document")
    print(result)


def test_wrong_document():
    application = {
        "name": "Student",
        "dob": "01/01/2007",
        "certificate_no": "CERT001"
    }

    document = {
        "name": "Different Student",
        "dob": "01/01/2007",
        "certificate_no": "CERT001"
    }

    result = verify_document(application, document, "12th")

    print("\nTest 2 - Wrong Document")
    print(result)


if __name__ == "__main__":
    test_correct_document()
    test_wrong_document()