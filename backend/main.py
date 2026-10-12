import os
import re
import sys
from pathlib import Path as FilePath

from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel

PROJECT_ROOT = FilePath(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.database import get_connection, create_table
from ai.verification.verify import verify_certificate

app = FastAPI(title="AI Scholarship Portal")
create_table()


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


class VerificationRequest(BaseModel):
    student_id: int
    document_type: str
    application: dict


@app.get("/")
def home():
    return {"message": "AI Scholarship Portal Backend is running"}


@app.post("/register")
def register(student: Student):
    connection = get_connection()
    try:
        connection.execute(
            "INSERT INTO students (name, email, password) VALUES (?, ?, ?)",
            (student.name, student.email, student.password),
        )
        connection.commit()
        return {"message": "Registration successful"}
    except Exception:
        raise HTTPException(status_code=400, detail="Email already registered")
    finally:
        connection.close()


@app.post("/login")
def login(student: Student):
    connection = get_connection()
    user = connection.execute(
        "SELECT * FROM students WHERE email = ? AND password = ?",
        (student.email, student.password),
    ).fetchone()
    connection.close()

    if user:
        return {
            "message": "Login successful",
            "student_id": user["id"],
            "name": user["name"],
            "email": user["email"],
        }
    raise HTTPException(status_code=401, detail="Invalid email or password")


@app.get("/profile/{student_id}")
def get_profile(student_id: int):
    connection = get_connection()
    student = connection.execute(
        "SELECT id, name, email FROM students WHERE id = ?", (student_id,)
    ).fetchone()
    connection.close()
    if student:
        return dict(student)
    raise HTTPException(status_code=404, detail="Student not found")


@app.post("/scholarships")
def add_scholarship(scholarship: Scholarship):
    connection = get_connection()
    connection.execute(
        """INSERT INTO scholarships (name, eligibility, amount, last_date)
           VALUES (?, ?, ?, ?)""",
        (scholarship.name, scholarship.eligibility, scholarship.amount,
         scholarship.last_date),
    )
    connection.commit()
    connection.close()
    return {"message": "Scholarship added successfully"}


@app.get("/scholarships")
def get_scholarships():
    connection = get_connection()
    rows = connection.execute("SELECT * FROM scholarships").fetchall()
    connection.close()
    return [dict(row) for row in rows]


@app.get("/scholarships/{scholarship_id}")
def get_scholarship(scholarship_id: int):
    connection = get_connection()
    row = connection.execute(
        "SELECT * FROM scholarships WHERE id = ?", (scholarship_id,)
    ).fetchone()
    connection.close()
    if row:
        return dict(row)
    raise HTTPException(status_code=404, detail="Scholarship not found")


@app.post("/applications")
def apply_scholarship(application: Application):
    connection = get_connection()
    try:
        student = connection.execute(
            "SELECT id FROM students WHERE id = ?", (application.student_id,)
        ).fetchone()
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

        scholarship = connection.execute(
            "SELECT id FROM scholarships WHERE id = ?",
            (application.scholarship_id,),
        ).fetchone()
        if not scholarship:
            raise HTTPException(status_code=404, detail="Scholarship not found")

        existing = connection.execute(
            """SELECT id FROM applications
               WHERE student_id = ? AND scholarship_id = ?""",
            (application.student_id, application.scholarship_id),
        ).fetchone()
        if existing:
            raise HTTPException(
                status_code=409, detail="Already applied for this scholarship"
            )

        connection.execute(
            """INSERT INTO applications (student_id, scholarship_id)
               VALUES (?, ?)""",
            (application.student_id, application.scholarship_id),
        )
        connection.commit()
        return {
            "message": "Scholarship application submitted successfully",
            "status": "Pending",
        }
    finally:
        connection.close()


@app.get("/applications/{student_id}")
def get_applications(student_id: int):
    connection = get_connection()
    rows = connection.execute(
        """SELECT applications.id, scholarships.name AS scholarship_name,
                  scholarships.amount, scholarships.last_date,
                  applications.status, applications.applied_date
           FROM applications
           JOIN scholarships ON applications.scholarship_id = scholarships.id
           WHERE applications.student_id = ?""",
        (student_id,),
    ).fetchall()
    connection.close()
    return [dict(row) for row in rows]


@app.put("/applications/{application_id}/status")
def update_application_status(
    application_id: int, application_status: ApplicationStatus
):
    allowed_status = ["Pending", "Approved", "Rejected"]
    if application_status.status not in allowed_status:
        raise HTTPException(status_code=400, detail="Invalid status")

    connection = get_connection()
    try:
        result = connection.execute(
            "UPDATE applications SET status = ? WHERE id = ?",
            (application_status.status, application_id),
        )
        connection.commit()
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Application not found")
        return {
            "message": "Application status updated",
            "status": application_status.status,
        }
    finally:
        connection.close()


@app.post("/documents/{student_id}")
async def upload_document(student_id: int, file: UploadFile = File(...)):
    connection = get_connection()
    student = connection.execute(
        "SELECT id FROM students WHERE id = ?", (student_id,)
    ).fetchone()
    connection.close()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    # Save using a generated filename to avoid path traversal and filename collisions.
    os.makedirs("uploads", exist_ok=True)
    safe_name = os.path.basename(file.filename or "document")
    stored_name = f"{student_id}_{__import__('uuid').uuid4().hex}_{safe_name}"
    file_path = os.path.abspath(os.path.join("uploads", stored_name))

    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Uploaded file is empty")
    with open(file_path, "wb") as output:
        output.write(content)

    connection = get_connection()
    try:
        cursor = connection.execute(
            """INSERT INTO documents (student_id, document_name, document_path)
               VALUES (?, ?, ?)""",
            (student_id, safe_name, file_path),
        )
        connection.commit()
        return {
            "message": "Document uploaded successfully",
            "document_id": cursor.lastrowid,
            "file_name": safe_name,
        }
    finally:
        connection.close()


@app.get("/documents/{student_id}")
def get_documents(student_id: int):
    connection = get_connection()
    rows = connection.execute(
        """SELECT id, student_id, document_name, document_path
           FROM documents WHERE student_id = ?""",
        (student_id,),
    ).fetchall()
    connection.close()
    return [dict(row) for row in rows]


@app.post("/verify-document/{document_id}")
def verify_uploaded_document(
    document_id: int, request: VerificationRequest
):
    allowed_types = {"10th", "12th", "aadhaar", "income", "community"}
    document_type = request.document_type.strip().lower()
    if document_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Invalid document type")

    connection = get_connection()
    try:
        row = connection.execute(
            """SELECT id, student_id, document_path FROM documents
               WHERE id = ? AND student_id = ?""",
            (document_id, request.student_id),
        ).fetchone()
    finally:
        connection.close()

    if not row:
        raise HTTPException(
            status_code=404,
            detail="Document not found for this student",
        )

    image_path = FilePath(row["document_path"]).resolve()
    uploads_root = FilePath("uploads").resolve()
    try:
        image_path.relative_to(uploads_root)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid stored document path")

    if not image_path.is_file():
        raise HTTPException(status_code=404, detail="Uploaded document file not found")

    result = verify_certificate(
        request.application, str(image_path), document_type
    )
    return {
        "document_id": document_id,
        "document_type": document_type,
        **result,
    }


@app.post("/bank-details")
def save_bank_details(bank: BankDetails):
    connection = get_connection()
    try:
        student = connection.execute(
            "SELECT id FROM students WHERE id = ?", (bank.student_id,)
        ).fetchone()
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

        existing = connection.execute(
            "SELECT id FROM bank_details WHERE student_id = ?",
            (bank.student_id,),
        ).fetchone()

        if existing:
            connection.execute(
                """UPDATE bank_details
                   SET account_holder = ?, account_number = ?, ifsc = ?,
                       bank_name = ?, verification_status = 'Pending'
                   WHERE student_id = ?""",
                (bank.account_holder, bank.account_number, bank.ifsc,
                 bank.bank_name, bank.student_id),
            )
        else:
            connection.execute(
                """INSERT INTO bank_details
                   (student_id, account_holder, account_number, ifsc, bank_name)
                   VALUES (?, ?, ?, ?, ?)""",
                (bank.student_id, bank.account_holder, bank.account_number,
                 bank.ifsc, bank.bank_name),
            )
        connection.commit()
        return {
            "message": "Bank details saved successfully",
            "verification_status": "Pending",
        }
    finally:
        connection.close()


@app.post("/verify-bank/{student_id}")
def verify_bank(student_id: int):
    connection = get_connection()
    try:
        bank = connection.execute(
            "SELECT * FROM bank_details WHERE student_id = ?", (student_id,)
        ).fetchone()
        if not bank:
            raise HTTPException(status_code=404, detail="Bank details not found")

        account_valid = bool(re.fullmatch(r"\d{9,18}", bank["account_number"]))
        ifsc_valid = bool(
            re.fullmatch(r"[A-Z]{4}0[A-Z0-9]{6}", bank["ifsc"].upper())
        )
        status = "Valid Format" if account_valid and ifsc_valid else "Invalid Format"

        connection.execute(
            "UPDATE bank_details SET verification_status = ? WHERE student_id = ?",
            (status, student_id),
        )
        connection.commit()
        return {
            "student_id": student_id,
            "bank_name": bank["bank_name"],
            "account_holder": bank["account_holder"],
            "verification_status": status,
            "message": (
                "Bank details format is valid"
                if status == "Valid Format"
                else "Bank details format is invalid"
            ),
        }
    finally:
        connection.close()


@app.get("/bank-details/{student_id}")
def get_bank_details(student_id: int):
    connection = get_connection()
    bank = connection.execute(
        """SELECT id, student_id, account_holder, account_number,
                  ifsc, bank_name, verification_status
           FROM bank_details WHERE student_id = ?""",
        (student_id,),
    ).fetchone()
    connection.close()
    if not bank:
        raise HTTPException(status_code=404, detail="Bank details not found")
    return dict(bank)
