# app/controllers/admin_controller/manage_courses.py

from app.utils.db import connect_db

def course_menu(cursor, conn):
    while True:
        print("\n=== 📚 MANAGE COURSES ===")
        print("1️⃣  View All Courses")
        print("2️⃣  Add New Course")
        print("3️⃣  Update Course Info")
        print("4️⃣  Delete Course")
        print("5️⃣  Back to Admin Dashboard")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            view_all_courses(cursor)
        elif choice == "2":
            add_course(cursor, conn)
        elif choice == "3":
            update_course(cursor, conn)
        elif choice == "4":
            delete_course(cursor, conn)
        elif choice == "5":
            break
        else:
            print("❌ Invalid choice, try again.")


# ===============================
# COURSE OPERATIONS
# ===============================

def view_all_courses(cursor):
    cursor.execute("""
        SELECT c.course_id, c.course_name, c.course_code, c.semester, t.name
        FROM courses c
        LEFT JOIN teachers t ON c.teacher_id = t.teacher_id;
    """)
    rows = cursor.fetchall()
    if not rows:
        print("\n⚠️  No courses found in the system.")
        return

    print("\n=== 📖 All Courses ===")
    for r in rows:
        teacher_name = r[4] if r[4] else "Unassigned"
        print(f"  - ID: {r[0]} | Name: {r[1]} | Code: {r[2]} | Semester: {r[3]} | Teacher: {teacher_name}")


def add_course(cursor, conn):
    print("\n=== ➕ Add New Course ===")
    course_name = input("Enter Course Name: ").strip()
    course_code = input("Enter Course Code: ").strip()
    semester = input("Enter Semester: ").strip()
    teacher_id = input("Enter Teacher ID (or leave blank for unassigned): ").strip() or None

    cursor.execute("""
        INSERT INTO courses (course_name, course_code, semester, teacher_id)
        VALUES (%s, %s, %s, %s);
    """, (course_name, course_code, semester, teacher_id))
    conn.commit()
    print(f"✅ Course '{course_name}' added successfully.")


def update_course(cursor, conn):
    print("\n=== ✏️ Update Course Info ===")
    course_id = input("Enter Course ID to update: ").strip()

    cursor.execute("SELECT * FROM courses WHERE course_id = %s;", (course_id,))
    if not cursor.fetchone():
        print("⚠️  No such course found.")
        return

    print("Leave field blank to keep current value.")
    new_name = input("New Course Name: ").strip()
    new_code = input("New Course Code: ").strip()
    new_semester = input("New Semester: ").strip()
    new_teacher_id = input("New Teacher ID: ").strip()

    update_fields = []
    values = []

    if new_name:
        update_fields.append("course_name = %s")
        values.append(new_name)
    if new_code:
        update_fields.append("course_code = %s")
        values.append(new_code)
    if new_semester:
        update_fields.append("semester = %s")
        values.append(new_semester)
    if new_teacher_id:
        update_fields.append("teacher_id = %s")
        values.append(new_teacher_id)

    if update_fields:
        query = f"UPDATE courses SET {', '.join(update_fields)} WHERE course_id = %s;"
        values.append(course_id)
        cursor.execute(query, tuple(values))
        conn.commit()
        print(f"✅ Course {course_id} updated successfully.")
    else:
        print("⚠️  No changes made.")


def delete_course(cursor, conn):
    print("\n=== ❌ Delete Course ===")
    course_id = input("Enter Course ID to delete: ").strip()

    cursor.execute("DELETE FROM courses WHERE course_id = %s;", (course_id,))
    conn.commit()
    print(f"✅ Course {course_id} deleted successfully (if existed).")
