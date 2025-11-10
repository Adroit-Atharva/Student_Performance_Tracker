# app/main.py

import sys
import re
import psycopg2
from psycopg2 import sql
from app.utils.db import connect_db
from app.controllers import student_controller, teacher_controller
from app.controllers.admin_controller import dashboard
from app.utils.id_generator import generate_student_id, generate_teacher_id


# ==============================
#  SIGN-UP SCREEN
# ==============================
def signup_screen(conn):
    cursor = conn.cursor()
    print("\n=== ✨ Sign Up ===")

    # --- ROLE SELECTION ---
    while True:
        role = input("Enter your role (student/teacher): ").strip().lower()
        if role in ("student", "teacher"):
            break
        print("❌ Invalid role! Please enter either 'student' or 'teacher'.")

    # --- NAME ---
    while True:
        name = input("Enter your full name: ").strip()
        if len(name) < 3:
            print("❌ Name must be at least 3 characters long.")
        else:
            break

    # --- EMAIL ---
    table = "students" if role == "student" else "teachers"
    id_column = "student_id" if role == "student" else "teacher_id"

    while True:
        email = input("Enter your email: ").strip().lower()
        if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
            print("❌ Invalid email format.")
            continue

        cursor.execute(
            sql.SQL("SELECT 1 FROM {} WHERE email = %s;").format(sql.Identifier(table)),
            [email],
        )
        if cursor.fetchone():
            print("❌ That email is already registered. Try another.")
        else:
            break

    # --- PASSWORD ---
    while True:
        password = input("Enter your password (min 6 chars): ").strip()
        if len(password) < 6:
            print("❌ Password must be at least 6 characters long.")
            continue
        confirm = input("Re-enter your password: ").strip()
        if confirm != password:
            print("❌ Passwords do not match. Try again.")
        else:
            break

    # --- AUTO-GENERATE UNIQUE ID ---
    if role == "student":
        user_id = generate_student_id()
    else:
        user_id = generate_teacher_id()

    # --- VERIFY UNIQUE ID IN DB (safety check) ---
    cursor.execute(
        sql.SQL("SELECT 1 FROM {} WHERE {} = %s;").format(
            sql.Identifier(table), sql.Identifier(id_column)
        ),
        [user_id],
    )
    if cursor.fetchone():
        print("⚠️ Generated ID already exists — regenerating...")
        user_id = generate_student_id() if role == "student" else generate_teacher_id()

    # --- ROLE-SPECIFIC DETAILS ---
    if role == "student":
        while True:
            try:
                semester = int(input("Enter your current semester (1–4): ").strip())
                if 1 <= semester <= 4:
                    break
                else:
                    print("❌ Semester must be between 1 and 4.")
            except ValueError:
                print("❌ Please enter a valid number for semester.")

        cursor.execute(
            """
            INSERT INTO students (student_id, name, email, password, semester)
            VALUES (%s, %s, %s, %s, %s);
            """,
            (user_id, name, email, password, semester),
        )

    elif role == "teacher":
        while True:
            department = input("Enter your department: ").strip()
            if department:
                break
            print("❌ Department cannot be empty.")

        cursor.execute(
            """
            INSERT INTO teachers (teacher_id, name, email, password, department)
            VALUES (%s, %s, %s, %s, %s);
            """,
            (user_id, name, email, password, department),
        )

    conn.commit()
    print(f"\n✅ {role.capitalize()} {name} registered successfully with ID: {user_id}")
    return user_id, password, role


# ==============================
#  LOGIN SCREEN
# ==============================
def login_screen(conn):
    print("\n=== 🔐 Login ===")
    cursor = conn.cursor()

    # --- ROLE VALIDATION ---
    while True:
        role = input("Enter your role (student/teacher/admin): ").strip().lower()
        if role in ("student", "teacher", "admin"):
            break
        print("❌ Invalid role! Please enter either 'student', 'teacher', or 'admin'.")

    # --- EMAIL VALIDATION ---
    while True:
        email = input("Enter your email: ").strip().lower()
        if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
            print("❌ Invalid email format. Please try again.")
        else:
            break

    # --- PASSWORD VALIDATION ---
    while True:
        password = input("Enter your password: ").strip()
        if len(password) < 6:
            print("❌ Password must be at least 6 characters long.")
        else:
            break

    # --- ROLE-BASED AUTHENTICATION ---
    if role == "student":
        cursor.execute("SELECT student_id FROM students WHERE email=%s AND password=%s;", (email, password))
        record = cursor.fetchone()
        if record:
            print(f"✅ Login successful! Welcome Student {record[0]}.")
            return record[0], role

    elif role == "teacher":
        cursor.execute("SELECT teacher_id FROM teachers WHERE email=%s AND password=%s;", (email, password))
        record = cursor.fetchone()
        if record:
            print(f"✅ Login successful! Welcome Teacher {record[0]}.")
            return record[0], role

    elif role == "admin":
        # Static admin credentials for now
        if email == "birajdaratharva@gmail.com" and password == "admin123":
            print("✅ Welcome Admin!")
            return 0, "admin"

    print("❌ Invalid credentials or role. Please try again.\n")
    return None


# ==============================
#  ROLE ROUTER
# ==============================
def route_to_role(role, user_id):
    if role == "student":
        student_controller.student_menu(user_id)
    elif role == "teacher":
        teacher_controller.teacher_menu(user_id)
    elif role == "admin":
        dashboard.admin_menu(user_id)
    else:
        print("❌ Invalid role! Please restart the program.")
        sys.exit(1)


# ==============================
#  MAIN ENTRY POINT
# ==============================
def main():
    conn = connect_db()

    print("\n=== 🎓 Student Course and Performance Tracker ===")
    choice = input("Do you want to (1) Login, (2) Sign Up, or (3) Exit? Enter 1, 2, or 3: ").strip()
    
    if choice == "3":
        print("👋 Exiting the system. Goodbye!")
        conn.close()
        sys.exit(0)

    elif choice == "2":
        signup_result = signup_screen(conn)
        if signup_result:
            user_id, password, role = signup_result
            print(f"\nWelcome {role.capitalize()} {user_id}!\n")
            route_to_role(role, user_id)
        else:
            print("Returning to main menu...")
            main()
    else:
        login_result = login_screen(conn)
        if login_result:
            user_id, role = login_result
            print(f"\nWelcome back {role.capitalize()} {user_id}!\n")
            route_to_role(role, user_id)
        else:
            print("Returning to main menu...")
            main()

    conn.close()


if __name__ == "__main__":
    main()
