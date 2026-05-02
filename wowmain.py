import sqlite3
import re

conn = sqlite3.connect("students.db")
cursor = conn.cursor()

itemCount = 0

# REGEX PATTERNS
id_pattern = r"^20\d{2}-\d{3}$"
email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
phone_pattern = r"^(09\d{9}|\+639\d{9})$"
date_pattern = r"^(0[1-9]|1[0-2])/(0[1-9]|[12]\d|3[01])/\d{4}$"

def validate(pattern, value):
    return re.match(pattern, value)

def add_student():
    global itemCount

    student_id = input("Enter ID (20YY-XXX): ")
    if not validate(id_pattern, student_id):
        print("Invalid ID format!")
        return

    first = input("First Name: ")
    middle = input("Middle Name: ")
    last = input("Last Name: ")
    gender = input("Gender (Male/Female/Others): ")

    birthdate = input("Birthdate (MM/DD/YYYY): ")
    if not validate(date_pattern, birthdate):
        print("Invalid date!")
        return

    place = input("Place of Birth: ")

    email = input("Email: ")
    if not validate(email_pattern, email):
        print("Invalid email!")
        return

    phone = input("Contact Number: ")
    if not validate(phone_pattern, phone):
        print("Invalid phone!")
        return

    section = input("Section: ")
    league = input("League Color: ")

    try:
        cursor.execute("""
        INSERT INTO students VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (student_id, first, middle, last, gender,
              birthdate, place, email, phone, section, league))

        conn.commit()
        itemCount += 1
        print("Student added!")

    except sqlite3.IntegrityError:
        print("Duplicate ID or Email!")

def view_students():
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()

    if not rows:
        print("No records found.")
        return

    for row in rows:
        print(row)

def update_student():
    student_id = input("Enter ID to update: ")

    cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
    if not cursor.fetchone():
        print("Student not found!")
        return

    email = input("New Email: ")
    if not validate(email_pattern, email):
        print("Invalid email!")
        return

    phone = input("New Contact: ")
    if not validate(phone_pattern, phone):
        print("Invalid phone!")
        return

    cursor.execute("""
    UPDATE students
    SET email_address = ?, contact_number = ?
    WHERE id = ?
    """, (email, phone, student_id))

    conn.commit()
    print("Student updated!")

def delete_student():
    global itemCount

    student_id = input("Enter ID to delete: ")

    cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
    conn.commit()

    if cursor.rowcount > 0:
        itemCount -= 1
        print("Deleted successfully!")
    else:
        print("Student not found!")

def main():
    while True:
        print("\nStudent Information System")
        print("1. Add Student")
        print("2. View Students")
        print("3. Update Student")
        print("4. Delete Student")
        print("5. Exit")

        choice = input("Choose: ")

        if choice == "1":
            add_student()
        elif choice == "2":
            view_students()
        elif choice == "3":
            update_student()
        elif choice == "4":
            delete_student()
        elif choice == "5":
            break
        else:
            print("Invalid choice!")

main()
conn.close()