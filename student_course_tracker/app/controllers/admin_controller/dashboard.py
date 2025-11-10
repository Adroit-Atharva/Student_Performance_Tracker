# app/controllers/admin_controller/dashboard.py

from app.utils.db import connect_db
from app.controllers.admin_controller import manage_students, manage_teachers, manage_courses, reports, system_controls

def admin_menu(admin_id):
    conn = connect_db()
    cursor = conn.cursor()

    while True:
        print("\n" + "="*60)
        print("🎓 STUDENT COURSE & PERFORMANCE TRACKER SYSTEM")
        print("="*60)
        print(f"\n👋 Welcome, Admin (ID: {admin_id})")
        print("-"*60)
        print("Please select an option:\n")
        print("  1️⃣  📘 Manage Courses")
        print("  2️⃣  🎓 Manage Students")
        print("  3️⃣  👩‍🏫 Manage Teachers")
        print("  4️⃣  📊 Reports & Data")
        print("  5️⃣  ⚙️ System Controls")
        print("-"*60)
        print("🔙 [B] Go Back     🏠 [H] Home     🚪 [Q] Logout / Exit")
        print("="*60)

        choice = input("\nEnter your choice: ").strip().lower()

        if choice == "1":
            manage_courses.course_menu(cursor, conn)
        elif choice == "2":
            manage_students.student_menu(cursor, conn)
        elif choice == "3":
            manage_teachers.teacher_menu(cursor, conn)
        elif choice == "4":
            reports.report_menu(cursor)
        elif choice == "5":
            system_controls.system_menu()
        elif choice in ["q", "exit"]:
            print("\n👋 Logged out successfully. Goodbye!")
            break
        elif choice in ["b", "h"]:
            print("\n🏠 Returning to main login screen...")
            break
        else:
            print("❌ Invalid choice, try again.")

    conn.close()
