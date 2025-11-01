# app/main.py

import sys
from app.utils.db import connect_db
from app.controllers import student_controller, teacher_controller, admin_controller

def login_screen():
    print("\n=== Student Course and Performance Tracker ===\n")
    user_id = input("Enter your ID: ").strip()
    password = input("Enter your password: ").strip()
    role = input("Enter your role (student/teacher/admin): ").strip().lower()

    return user_id, password, role


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
    # Initialize DB connection
    conn = connect_db()

    # Simple login
    user_id, password, role = login_screen()

    # TODO: Replace with actual authentication logic
    print(f"\nWelcome {role.capitalize()} {user_id}!\n")

    # Route user to respective role menu
    route_to_role(role, user_id)

    # Close DB connection on exit
    conn.close()


if __name__ == "__main__":
    main()
