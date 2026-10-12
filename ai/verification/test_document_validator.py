from document_validator import validate_document_type


def test_correct_type():
    text = "HIGHER SECONDARY CERTIFICATE"
    result = validate_document_type("12th", text)

    print("\nTest 1 - Correct Document Type")
    print(result)


def test_wrong_type():
    text = "INCOME CERTIFICATE"
    result = validate_document_type("12th", text)

    print("\nTest 2 - Wrong Document Type")
    print(result)


if __name__ == "__main__":
    test_correct_type()
    test_wrong_type()