from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from database import get_connection, create_table

import os
import re


app = FastAPI(title="AI Scholarship Portal")

create_table()


# =========================================================
# MODELS
# =========================================================

class Student(BaseModel):
    name: str
    email: str
    password: str


class Scholarship(BaseModel):
    name: str
    eligibility: str
    amount: str
    last_date: str


class Application(BaseModel):
    student_id: int
    scholarship_id: int


class ApplicationStatus(BaseModel):
    status: str


class BankDetails(BaseModel):
    student_id: int
    account_holder: str
    account_number: str
    ifsc: str
    bank_name: str


# =========================================================
# HOME
# =========================================================

@app.get("/")
def home():
    return {
        "message": "AI Scholarship Portal Backend is running"
    }


# =========================================================
# REGISTER
# =========================================================

@app.post("/register")
def register(student: Student):

    connection = get_connection()

    try:

        connection.execute(
            """
            INSERT INTO students (name, email, password)
            VALUES (?, ?, ?)
            """,
            (
                student.name,
                student.email,
                student.password
            )
        )

        connection.commit()

        return {
            "message": "Registration successful"
        }

    except Exception:

        return {
            "message": "Email already registered"
        }

    finally:

        connection.close()


# =========================================================
# LOGIN
# =========================================================

@app.post("/login")
def login(student: Student):

    connection = get_connection()

    user = connection.execute(
        """
        SELECT * FROM students
        WHERE email = ? AND password = ?
        """,
        (
            student.email,
            student.password
        )
    ).fetchone()

    connection.close()

    if user:

        return {
            "message": "Login successful",
            "student_id": user["id"],
            "name": user["name"],
            "email": user["email"]
        }

    return {
        "message": "Invalid email or password"
    }


# =========================================================
# GET STUDENT PROFILE
# =========================================================

@app.get("/profile/{student_id}")
def get_profile(student_id: int):

    connection = get_connection()

    student = connection.execute(
        """
        SELECT id, name, email
        FROM students
        WHERE id = ?
        """,
        (student_id,)
    ).fetchone()

    connection.close()

    if student:

        return dict(student)

    return {
        "message": "Student not found"
    }


# =========================================================
# ADD SCHOLARSHIP
# =========================================================

@app.post("/scholarships")
def add_scholarship(scholarship: Scholarship):

    connection = get_connection()

    connection.execute(
        """
        INSERT INTO scholarships
        (name, eligibility, amount, last_date)
        VALUES (?, ?, ?, ?)
        """,
        (
            scholarship.name,
            scholarship.eligibility,
            scholarship.amount,
            scholarship.last_date
        )
    )

    connection.commit()
    connection.close()

    return {
        "message": "Scholarship added successfully"
    }


# =========================================================
# GET ALL SCHOLARSHIPS
# =========================================================

@app.get("/scholarships")
def get_scholarships():

    connection = get_connection()

    scholarships = connection.execute(
        """
        SELECT * FROM scholarships
        """
    ).fetchall()

    connection.close()

    return [
        dict(scholarship)
        for scholarship in scholarships
    ]


# =========================================================
# GET SCHOLARSHIP BY ID
# =========================================================

@app.get("/scholarships/{scholarship_id}")
def get_scholarship(scholarship_id: int):

    connection = get_connection()

    scholarship = connection.execute(
        """
        SELECT * FROM scholarships
        WHERE id = ?
        """,
        (scholarship_id,)
    ).fetchone()

    connection.close()

    if scholarship:

        return dict(scholarship)

    return {
        "message": "Scholarship not found"
    }


# =========================================================
# APPLY FOR SCHOLARSHIP
# =========================================================

@app.post("/applications")
def apply_scholarship(application: Application):

    connection = get_connection()

    # Check student
    student = connection.execute(
        """
        SELECT * FROM students
        WHERE id = ?
        """,
        (application.student_id,)
    ).fetchone()

    if not student:

        connection.close()

        return {
            "message": "Student not found"
        }

    # Check scholarship
    scholarship = connection.execute(
        """
        SELECT * FROM scholarships
        WHERE id = ?
        """,
        (application.scholarship_id,)
    ).fetchone()

    if not scholarship:

        connection.close()

        return {
            "message": "Scholarship not found"
        }

    # Check already applied
    existing = connection.execute(
        """
        SELECT * FROM applications
        WHERE student_id = ?
        AND scholarship_id = ?
        """,
        (
            application.student_id,
            application.scholarship_id
        )
    ).fetchone()

    if existing:

        connection.close()

        return {
            "message": "Already applied for this scholarship"
        }

    # Apply
    connection.execute(
        """
        INSERT INTO applications
        (student_id, scholarship_id)
        VALUES (?, ?)
        """,
        (
            application.student_id,
            application.scholarship_id
        )
    )

    connection.commit()
    connection.close()

    return {
        "message": "Scholarship application submitted successfully",
        "status": "Pending"
    }


# =========================================================
# GET STUDENT APPLICATIONS
# =========================================================

@app.get("/applications/{student_id}")
def get_applications(student_id: int):

    connection = get_connection()

    applications = connection.execute(
        """
        SELECT
            applications.id,
            scholarships.name AS scholarship_name,
            scholarships.amount,
            scholarships.last_date,
            applications.status,
            applications.applied_date
        FROM applications
        JOIN scholarships
        ON applications.scholarship_id = scholarships.id
        WHERE applications.student_id = ?
        """,
        (student_id,)
    ).fetchall()

    connection.close()

    return [
        dict(application)
        for application in applications
    ]


# =========================================================
# UPDATE APPLICATION STATUS
# =========================================================

@app.put("/applications/{application_id}/status")
def update_application_status(
    application_id: int,
    application_status: ApplicationStatus
):

    allowed_status = [
        "Pending",
        "Approved",
        "Rejected"
    ]

    if application_status.status not in allowed_status:

        return {
            "message": "Invalid status"
        }

    connection = get_connection()

    result = connection.execute(
        """
        UPDATE applications
        SET status = ?
        WHERE id = ?
        """,
        (
            application_status.status,
            application_id
        )
    )

    connection.commit()

    if result.rowcount == 0:

        connection.close()

        return {
            "message": "Application not found"
        }

    connection.close()

    return {
        "message": "Application status updated",
        "status": application_status.status
    }


# =========================================================
# DOCUMENT UPLOAD
# =========================================================

@app.post("/documents/{student_id}")
async def upload_document(
    student_id: int,
    file: UploadFile = File(...)
):

    connection = get_connection()

    student = connection.execute(
        """
        SELECT * FROM students
        WHERE id = ?
        """,
        (student_id,)
    ).fetchone()

    connection.close()

    if not student:

        return {
            "message": "Student not found"
        }

    # Create uploads folder
    os.makedirs("uploads", exist_ok=True)

    file_path = os.path.join(
        "uploads",
        file.filename
    )

    file_content = await file.read()

    with open(file_path, "wb") as f:

        f.write(file_content)

    connection = get_connection()

    connection.execute(
        """
        INSERT INTO documents
        (student_id, document_name, document_path)
        VALUES (?, ?, ?)
        """,
        (
            student_id,
            file.filename,
            file_path
        )
    )

    connection.commit()
    connection.close()

    return {
        "message": "Document uploaded successfully",
        "file_name": file.filename
    }


# =========================================================
# GET STUDENT DOCUMENTS
# =========================================================

@app.get("/documents/{student_id}")
def get_documents(student_id: int):

    connection = get_connection()

    documents = connection.execute(
        """
        SELECT * FROM documents
        WHERE student_id = ?
        """,
        (student_id,)
    ).fetchall()

    connection.close()

    return [
        dict(document)
        for document in documents
    ]


# =========================================================
# SAVE BANK DETAILS
# =========================================================

@app.post("/bank-details")
def save_bank_details(bank: BankDetails):

    connection = get_connection()

    # Check student
    student = connection.execute(
        """
        SELECT * FROM students
        WHERE id = ?
        """,
        (bank.student_id,)
    ).fetchone()

    if not student:

        connection.close()

        return {
            "message": "Student not found"
        }

    # Check if bank details already exist
    existing = connection.execute(
        """
        SELECT * FROM bank_details
        WHERE student_id = ?
        """,
        (bank.student_id,)
    ).fetchone()

    if existing:

        connection.execute(
            """
            UPDATE bank_details
            SET account_holder = ?,
                account_number = ?,
                ifsc = ?,
                bank_name = ?,
                verification_status = 'Pending'
            WHERE student_id = ?
            """,
            (
                bank.account_holder,
                bank.account_number,
                bank.ifsc,
                bank.bank_name,
                bank.student_id
            )
        )

    else:

        connection.execute(
            """
            INSERT INTO bank_details
            (
                student_id,
                account_holder,
                account_number,
                ifsc,
                bank_name
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                bank.student_id,
                bank.account_holder,
                bank.account_number,
                bank.ifsc,
                bank.bank_name
            )
        )

    connection.commit()
    connection.close()

    return {
        "message": "Bank details saved successfully",
        "verification_status": "Pending"
    }


# =========================================================
# VERIFY BANK DETAILS
# =========================================================

@app.post("/verify-bank/{student_id}")
def verify_bank(student_id: int):

    connection = get_connection()

    bank = connection.execute(
        """
        SELECT * FROM bank_details
        WHERE student_id = ?
        """,
        (student_id,)
    ).fetchone()

    if not bank:

        connection.close()

        return {
            "message": "Bank details not found"
        }

    account_number = bank["account_number"]
    ifsc = bank["ifsc"]

    # Account number: 9 to 18 digits
    account_valid = bool(
        re.fullmatch(r"\d{9,18}", account_number)
    )

    # Indian IFSC format
    # Example: SBIN0001234
    ifsc_valid = bool(
        re.fullmatch(
            r"[A-Z]{4}0[A-Z0-9]{6}",
            ifsc.upper()
        )
    )

    if account_valid and ifsc_valid:

        status = "Valid Format"

    else:

        status = "Invalid Format"

    connection.execute(
        """
        UPDATE bank_details
        SET verification_status = ?
        WHERE student_id = ?
        """,
        (
            status,
            student_id
        )
    )

    connection.commit()
    connection.close()

    return {
        "student_id": student_id,
        "bank_name": bank["bank_name"],
        "account_holder": bank["account_holder"],
        "verification_status": status,
        "message": (
            "Bank details format is valid"
            if status == "Valid Format"
            else "Bank details format is invalid"
        )
    }


# =========================================================
# GET BANK DETAILS
# =========================================================

@app.get("/bank-details/{student_id}")
def get_bank_details(student_id: int):

    connection = get_connection()

    bank = connection.execute(
        """
        SELECT
            id,
            student_id,
            account_holder,
            account_number,
            ifsc,
            bank_name,
            verification_status
        FROM bank_details
        WHERE student_id = ?
        """,
        (student_id,)
    ).fetchone()

    connection.close()

    if not bank:

        return {
            "message": "Bank details not found"
        }

    return dict(bank)