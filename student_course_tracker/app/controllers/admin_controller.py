# app/controllers/admin_controller.py

import sys
from app.utils.db import connect_db

def admin_menu(admin_id):
    conn = connect_db()
    cursor = conn.cursor()

    while True:
        print("\n=== 🧠 ADMIN DASHBOARD ===")
        print("1️⃣  View All Students")
        print("2️⃣  View All Teachers")
        print("3️⃣  View All Courses")
        print("4️⃣  View All Performance Records")
        print("5️⃣  Delete a User (Student/Teacher)")
        print("6️⃣  Exit Admin Panel")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            view_all_students(cursor)
        elif choice == "2":
            view_all_teachers(cursor)
        elif choice == "3":
            view_all_courses(cursor)
        elif choice == "4":
            view_all_performance(cursor)
        elif choice == "5":
            delete_user(cursor, conn)
        elif choice == "6":
            print("👋 Exiting Admin Panel. Goodbye!")
            break
        else:
            print("❌ Invalid choice, try again.")

    conn.close()
    sys.exit(0)


def view_all_students(cursor):
    cursor.execute("SELECT student_id, name, email, semester FROM students;")
    rows = cursor.fetchall()
    if not rows:
        print("\n⚠️  No students found in the system.")
        return

    print("\n=== 👨‍🎓 All Students ===")
    for r in rows:
        print(f"  - ID: {r[0]} | Name: {r[1]} | Email: {r[2]} | Semester: {r[3]}")


def view_all_teachers(cursor):
    cursor.execute("SELECT teacher_id, name, email, department FROM teachers;")
    rows = cursor.fetchall()
    if not rows:
        print("\n⚠️  No teachers found in the system.")
        return

    print("\n=== 👩‍🏫 All Teachers ===")
    for r in rows:
        print(f"  - ID: {r[0]} | Name: {r[1]} | Email: {r[2]} | Department: {r[3]}")


def view_all_courses(cursor):
    cursor.execute("SELECT course_id, course_name, teacher_id FROM courses;")
    rows = cursor.fetchall()
    if not rows:
        print("\n⚠️  No courses available.")
        return

    print("\n=== 📚 All Courses ===")
    for r in rows:
        print(f"  - Course ID: {r[0]} | Name: {r[1]} | Teacher ID: {r[2]}")


def view_all_performance(cursor):
    cursor.execute("""
        SELECT p.student_id, s.name, p.course_id, p.marks, p.attendance
        FROM performance_records p
        JOIN students s ON p.student_id = s.student_id;
    """)
    rows = cursor.fetchall()
    if not rows:
        print("\n⚠️  No performance records found.")
        return

    print("\n=== 📊 All Performance Records ===")
    for r in rows:
        print(f"  - Student: {r[1]} (ID: {r[0]}) | Course: {r[2]} | Marks: {r[3]} | Attendance: {r[4]}%")


def delete_user(cursor, conn):
    print("\n=== ❌ Delete User ===")
    print("1️⃣  Delete Student")
    print("2️⃣  Delete Teacher")
    choice = input("Enter choice: ").strip()

    if choice == "1":
        sid = input("Enter Student ID to delete: ").strip()
        cursor.execute("DELETE FROM students WHERE student_id = %s;", (sid,))
        conn.commit()
        print(f"✅ Student {sid} deleted successfully (if existed).")

    elif choice == "2":
        tid = input("Enter Teacher ID to delete: ").strip()
        cursor.execute("DELETE FROM teachers WHERE teacher_id = %s;", (tid,))
        conn.commit()
        print(f"✅ Teacher {tid} deleted successfully (if existed).")

    else:
        print("❌ Invalid option.")
