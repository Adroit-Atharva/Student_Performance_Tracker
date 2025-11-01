# app/main.py

import sys
from app.utils.db import connect_db
from app.controllers import student_controller, teacher_controller, admin_controller
import psycopg2
from psycopg2 import sql

def signup_screen(conn):
    cursor = conn.cursor()

    role = input("Enter your role (student/teacher): ").strip().lower()
    user_id = input("Enter a unique numeric ID: ").strip()

    # Ensure ID is numeric
    if not user_id.isdigit():
        print("❌ ID must be numeric.")
        return None, None, None

    table = "students" if role == "student" else "teachers"
    id_column = "student_id" if role == "student" else "teacher_id"

    # Check if the ID already exists
    cursor.execute(sql.SQL("SELECT 1 FROM {} WHERE {} = %s;").format(
        sql.Identifier(table), sql.Identifier(id_column)
    ), [user_id])
    if cursor.fetchone():
        print("❌ That ID is already taken. Please choose another one.")
        return None, None, None

    # Gather other details
    name = input("Enter your full name: ").strip()
    email = input("Enter your email: ").strip()
    password = input("Enter your password: ").strip()

    # Optional fields
    semester = 1
    department = None
    if role == "student":
        semester = int(input("Enter your current semester (1–4): ").strip())
        cursor.execute(
            "INSERT INTO students (student_id, name, email, password, semester) VALUES (%s, %s, %s, %s, %s);",
            (user_id, name, email, password, semester)
        )
    elif role == "teacher":
        department = input("Enter your department: ").strip()
        cursor.execute(
            "INSERT INTO teachers (teacher_id, name, email, password, department) VALUES (%s, %s, %s, %s, %s);",
            (user_id, name, email, password, department)
        )
    else:
        print("❌ Invalid role. Signup cancelled.")
        return None, None, None

    conn.commit()
    print(f"\n✅ {role.capitalize()} {name} registered successfully with ID: {user_id}")
    return user_id, password, role


def login_screen(conn):
    print("\n=== Login ===")
    role = input("Enter your role (student/teacher/admin): ").strip().lower()
    email = input("Enter your email: ").strip()
    password = input("Enter your password: ").strip()

    cursor = conn.cursor()

    if role == "student":
        cursor.execute("SELECT student_id FROM students WHERE email=%s AND password=%s", (email, password))
        record = cursor.fetchone()
        if record:
            return record[0], role
    elif role == "teacher":
        cursor.execute("SELECT teacher_id FROM teachers WHERE email=%s AND password=%s", (email, password))
        record = cursor.fetchone()
        if record:
            return record[0], role
    elif role == "admin":
        # temporary static admin login
        if email == "admin@tracker.com" and password == "admin123":
            return 0, "admin"

    print("❌ Invalid credentials or role.")
    return None


def route_to_role(role, user_id):
    if role == "student":
        student_controller.student_menu(user_id)
    elif role == "teacher":
        teacher_controller.teacher_menu(user_id)
    elif role == "admin":
        admin_controller.admin_menu(user_id)
    else:
        print("❌ Invalid role! Please restart the program.")
        sys.exit(1)


def main():
    conn = connect_db()

    print("\n=== Student Course and Performance Tracker ===")
    choice = input("Do you want to (1) Login, (2) Sign Up, or (3) Exit? Enter 1, 2, or 3: ").strip()
    
    if choice == "3":
        print("👋 Exiting the system. Goodbye!")
        conn.close()
        sys.exit(0)

    if choice == "2":
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
