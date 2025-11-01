# app/controllers/teacher_controller.py

import sys
import csv
from app.utils.db import connect_db

def teacher_menu(teacher_id):
    conn = connect_db()
    cursor = conn.cursor()

    while True:
        print("\n=== 📚 Teacher Dashboard ===")
        print("1️⃣  View My Courses")
        print("2️⃣  View Enrolled Students in a Course")
        print("3️⃣  Import Student Performance (CSV)")
        print("4️⃣  View Course Performance Summary")
        print("5️⃣  Logout")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            view_courses(cursor, teacher_id)
        elif choice == "2":
            view_enrolled_students(cursor, teacher_id)
        elif choice == "3":
            import_performance_csv(conn, cursor, teacher_id)
        elif choice == "4":
            view_performance_summary(cursor, teacher_id)
        elif choice == "5":
            print("👋 Logging out...")
            break
        else:
            print("❌ Invalid choice, try again.")

    conn.close()


def view_courses(cursor, teacher_id):
    cursor.execute("SELECT course_id, course_name FROM courses WHERE teacher_id = %s;", (teacher_id,))
    rows = cursor.fetchall()
    if not rows:
        print("\n⚠️  You are not assigned to any courses.")
        return
    print("\nYour Courses:")
    for course in rows:
        print(f"  - {course[1]} (Course ID: {course[0]})")


def view_enrolled_students(cursor, teacher_id):
    course_id = input("Enter Course ID to view enrolled students: ").strip()
    cursor.execute("""
        SELECT s.student_id, s.name, s.email
        FROM enrollments e
        JOIN students s ON e.student_id = s.student_id
        JOIN courses c ON e.course_id = c.course_id
        WHERE c.course_id = %s AND c.teacher_id = %s;
    """, (course_id, teacher_id))
    rows = cursor.fetchall()

    if not rows:
        print("\n⚠️  No students enrolled in this course or invalid Course ID.")
        return

    print("\nEnrolled Students:")
    for s in rows:
        print(f"  - {s[1]} (ID: {s[0]}, Email: {s[2]})")


def import_performance_csv(conn, cursor, teacher_id):
    course_id = input("Enter Course ID for importing performance data: ").strip()
    csv_path = input("Enter path to CSV file: ").strip()

    try:
        with open(csv_path, 'r') as file:
            reader = csv.DictReader(file)
            count = 0
            for row in reader:
                student_id = row['student_id']
                marks = float(row['marks'])
                attendance = float(row['attendance'])
                cursor.execute("""
                    INSERT INTO performance_records (student_id, course_id, marks, attendance)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (student_id, course_id)
                    DO UPDATE SET marks = EXCLUDED.marks, attendance = EXCLUDED.attendance;
                """, (student_id, course_id, marks, attendance))
                count += 1
            conn.commit()
            print(f"✅ Successfully imported performance data for {count} students.")
    except Exception as e:
        print(f"❌ Error importing CSV: {e}")


def view_performance_summary(cursor, teacher_id):
    course_id = input("Enter Course ID to view summary: ").strip()
    cursor.execute("""
        SELECT AVG(marks), AVG(attendance)
        FROM performance_records
        WHERE course_id = %s;
    """, (course_id,))
    result = cursor.fetchone()

    if not result or result[0] is None:
        print("\n⚠️  No performance data available for this course.")
        return

    avg_marks, avg_attendance = result
    print(f"\n📊 Performance Summary for Course {course_id}:")
    print(f"  - Average Marks: {avg_marks:.2f}")
    print(f"  - Average Attendance: {avg_attendance:.2f}%")
