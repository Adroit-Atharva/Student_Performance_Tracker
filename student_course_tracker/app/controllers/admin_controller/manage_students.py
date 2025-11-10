# app/controllers/admin_controller/manage_students.py

from app.utils.db import connect_db

# ===============================
# STUDENT MANAGEMENT MENU
# ===============================
def student_menu(cursor, conn):
    while True:
        print("\n=== 🎓 MANAGE STUDENTS ===")
        print("1️⃣  View All Students")
        print("2️⃣  View All Student Performance Records")
        print("3️⃣  Delete Student")
        print("4️⃣  Approve/Reject Enrollment Requests")
        print("5️⃣  Back to Admin Dashboard")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            view_all_students(cursor)
        elif choice == "2":
            view_all_performance(cursor)
        elif choice == "3":
            delete_student(cursor, conn)
        elif choice == "4":
            approve_enrollments(cursor, conn)
        elif choice == "5":
            break
        else:
            print("❌ Invalid choice, try again.")


# ===============================
# VIEW STUDENTS
# ===============================
def view_all_students(cursor):
    cursor.execute("SELECT student_id, name, email, semester FROM students;")
    rows = cursor.fetchall()
    if not rows:
        print("\n⚠️  No students found in the system.")
        return

    print("\n=== 👨‍🎓 All Students ===")
    for r in rows:
        print(f"  - ID: {r[0]} | Name: {r[1]} | Email: {r[2]} | Semester: {r[3]}")


# ===============================
# VIEW PERFORMANCE RECORDS
# ===============================
def view_all_performance(cursor):
    cursor.execute("""
        SELECT p.student_id, s.name, p.course_id, p.assignments_completed, 
               p.assignment_marks, p.internal_marks, p.external_marks, p.attendance_percent
        FROM performance_records p
        JOIN students s ON p.student_id = s.student_id;
    """)
    rows = cursor.fetchall()

    if not rows:
        print("\n⚠️  No performance records found.")
        return

    print("\n=== 📊 All Student Performance Records ===")
    for r in rows:
        print(f"  - Student: {r[1]} (ID: {r[0]}) | Course: {r[2]} | "
              f"Assignments: {r[3]} | Assignment Marks: {r[4]} | "
              f"Internal: {r[5]} | External: {r[6]} | Attendance: {r[7]}%")


# ===============================
# DELETE STUDENT
# ===============================
def delete_student(cursor, conn):
    print("\n=== ❌ Delete Student ===")
    sid = input("Enter Student ID to delete: ").strip()

    cursor.execute("DELETE FROM students WHERE student_id = %s;", (sid,))
    conn.commit()
    print(f"✅ Student {sid} deleted successfully (if existed).")


# ===============================
# APPROVE/REJECT ENROLLMENTS
# ===============================
def approve_enrollments(cursor, conn):
    print("\n=== ✅ Approve/Reject Enrollment Requests ===")
    cursor.execute("""
        SELECT e.enrollment_id, s.name, c.course_name, e.status
        FROM enrollments e
        JOIN students s ON e.student_id = s.student_id
        JOIN courses c ON e.course_id = c.course_id
        WHERE e.status = 'PENDING';
    """)
    rows = cursor.fetchall()

    if not rows:
        print("⚠️  No pending enrollment requests.")
        return

    for r in rows:
        print(f"  - Enrollment ID: {r[0]} | Student: {r[1]} | Course: {r[2]} | Status: {r[3]}")

    eid = input("\nEnter Enrollment ID to approve/reject (or 'all' to approve all): ").strip()
    if eid.lower() == "all":
        cursor.execute("UPDATE enrollments SET status = 'APPROVED' WHERE status = 'PENDING';")
        conn.commit()
        print("✅ All pending enrollments approved.")
    else:
        action = input("Type 'approve' or 'reject': ").strip().lower()
        if action == "approve":
            cursor.execute("UPDATE enrollments SET status = 'APPROVED' WHERE enrollment_id = %s;", (eid,))
            conn.commit()
            print(f"✅ Enrollment {eid} approved successfully.")
        elif action == "reject":
            cursor.execute("UPDATE enrollments SET status = 'REJECTED' WHERE enrollment_id = %s;", (eid,))
            conn.commit()
            print(f"✅ Enrollment {eid} rejected successfully.")
        else:
            print("❌ Invalid action, skipping.")

