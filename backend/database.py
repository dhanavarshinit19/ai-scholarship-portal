import sqlite3

DATABASE = "scholarship.db"


def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def create_table():
    connection = get_connection()

    # STUDENTS TABLE
    connection.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # SCHOLARSHIPS TABLE
    connection.execute("""
        CREATE TABLE IF NOT EXISTS scholarships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            eligibility TEXT NOT NULL,
            amount TEXT NOT NULL,
            last_date TEXT NOT NULL
        )
    """)

    # APPLICATIONS TABLE
    connection.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            scholarship_id INTEGER NOT NULL,
            status TEXT DEFAULT 'Pending',
            applied_date TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(student_id) REFERENCES students(id),
            FOREIGN KEY(scholarship_id) REFERENCES scholarships(id)
        )
    """)

    # DOCUMENTS TABLE
    connection.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            document_name TEXT NOT NULL,
            document_path TEXT NOT NULL,
            FOREIGN KEY(student_id) REFERENCES students(id)
        )
    """)

    # BANK DETAILS TABLE
    connection.execute("""
        CREATE TABLE IF NOT EXISTS bank_details (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER UNIQUE NOT NULL,
            account_holder TEXT NOT NULL,
            account_number TEXT NOT NULL,
            ifsc TEXT NOT NULL,
            bank_name TEXT NOT NULL,
            verification_status TEXT DEFAULT 'Pending',
            FOREIGN KEY(student_id) REFERENCES students(id)
        )
    """)

    connection.commit()
    connection.close()