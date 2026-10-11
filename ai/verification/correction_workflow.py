from verify import verify_certificate


def reverify_after_correction(
    application,
    corrected_image_path,
    document_type,
    previous_result=None
):
    result = verify_certificate(
        application,
        corrected_image_path,
        document_type
    )

    previous_attempts = 0

    if previous_result:
        previous_attempts = previous_result.get(
            "attempts", 1
        )

    result["attempts"] = previous_attempts + 1

    if result["status"] == "ACCEPTED":
        result["message"] = (
            "Corrected submission verified successfully."
        )
    elif result["status"] == "REJECTED":
        result["message"] = (
            "Verification failed again. "
            + result["message"]
        )
    elif result["status"] == "REVIEW_REQUIRED":
        result["message"] = (
            "Manual review is required after correction. "
            + result["message"]
        )

    return result
