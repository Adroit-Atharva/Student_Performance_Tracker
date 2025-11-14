# app/controllers/student_controller.py

def student_menu(cursor, student_id, conn):

    while True:
        print("\n=== STUDENT DASHBOARD ===")
        print("1. View Profile")
        print("2. View Available Courses")
        print("3. Request Enrollment")
        print("4. View My Enrolled Courses")
        print("5. View My Performance")
        print("6. Logout")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            view_profile(cursor, student_id)

        elif choice == "2":
            view_available_courses(cursor)

        elif choice == "3":
            request_enrollment(cursor, conn, student_id)

        elif choice == "4":
            view_enrolled_courses(cursor, student_id)

        elif choice == "5":
            view_performance(cursor, student_id)

        elif choice == "6":
            print("Logging out...")
            break

        else:
            print("Invalid choice. Try again.")


# ===============================
# 1. VIEW PROFILE (FULL VERSION)
# ===============================

def view_profile(cursor, student_id):
    cursor.execute("""
        SELECT student_id, name, email, semester
        FROM students
        WHERE student_id = %s;
    """, [student_id])

    record = cursor.fetchone()

    if not record:
        print("No profile found for this student.")
        return

    print("\n=== STUDENT PROFILE ===")
    print(f"Student ID : {record[0]}")
    print(f"Name       : {record[1]}")
    print(f"Email      : {record[2]}")
    print(f"Semester   : {record[3]}")


# ===============================
# 2. VIEW AVAILABLE COURSES (TEMP)
# ===============================

def view_available_courses(cursor):
    print("\nFetching available courses...")

    cursor.execute("""
        SELECT 
            c.course_id,
            c.course_name,
            c.course_code,
            c.semester,
            t.name AS teacher_name
        FROM courses c
        LEFT JOIN teachers t ON c.teacher_id = t.teacher_id
        ORDER BY c.course_id;
    """)

    rows = cursor.fetchall()

    if not rows:
        print("No courses available right now.")
        return

    print("\n=== AVAILABLE COURSES ===")
    for row in rows:
        teacher = row[4] if row[4] else "Not Assigned"
        print(f"[{row[0]}] {row[1]} ({row[2]})  Semester: {row[3]}  | Teacher: {teacher}")



# ===============================
# 3. REQUEST ENROLLMENT (TEMP)
# ===============================

def request_enrollment(cursor, conn, student_id):
    print("\n=== REQUEST COURSE ENROLLMENT ===")

    # Show available courses
    cursor.execute("""
        SELECT c.course_id, c.course_name, c.course_code, c.semester,
               t.name AS teacher_name
        FROM courses c
        LEFT JOIN teachers t ON c.teacher_id = t.teacher_id
        ORDER BY c.course_id;
    """)
    courses = cursor.fetchall()

    if not courses:
        print("No courses available.")
        return

    print("\nAvailable Courses:")
    for row in courses:
        course_id, name, code, sem, teacher = row
        teacher = teacher if teacher else "Not Assigned"
        print(f"[{course_id}] {name} ({code}) | Semester {sem} | Teacher: {teacher}")

    # Ask student to choose course
    try:
        course_id = int(input("\nEnter the Course ID you want to enroll in: ").strip())
    except ValueError:
        print("Invalid course ID.")
        return

    # Check that the course exists
    cursor.execute("SELECT 1 FROM courses WHERE course_id = %s;", [course_id])
    if not cursor.fetchone():
        print("Course does not exist.")
        return

    # Prevent duplicate enrollment requests
    cursor.execute("""
        SELECT 1 FROM enrollments
        WHERE student_id = %s AND course_id = %s;
    """, (student_id, course_id))

    if cursor.fetchone():
        print("You have already requested or enrolled in this course.")
        return

    # Insert enrollment request
    cursor.execute("""
        INSERT INTO enrollments (student_id, course_id, status, is_approved)
        VALUES (%s, %s, 'PENDING', FALSE);
    """, (student_id, course_id))

    conn.commit()

    print("Your enrollment request has been submitted and is pending approval.")



# ===============================
# 4. VIEW ENROLLED COURSES (TEMP)
# ===============================

def view_enrolled_courses(cursor, student_id):
    cursor.execute("""
        SELECT 
            c.course_id,
            c.course_name,
            t.name AS teacher_name,
            c.course_code,
            c.semester,
            e.enrollment_date,
            e.status,
            e.is_approved
        FROM enrollments e
        JOIN courses c ON e.course_id = c.course_id
        LEFT JOIN teachers t ON c.teacher_id = t.teacher_id
        WHERE e.student_id = %s
        ORDER BY e.enrollment_date DESC;
    """, (student_id,))

    courses = cursor.fetchall()

    if not courses:
        print("No enrolled courses found.")
        return

    print("\n=== ENROLLED COURSES ===")
    for course in courses:
        cid, name, teacher, code, sem, date, status, approved = course
        print(f"""
Course ID      : {cid}
Course Name    : {name}
Course Code    : {code}
Teacher        : {teacher if teacher else "Not Assigned"}
Semester       : {sem}
Enrolled On    : {date}
Status         : {status}
Approved       : {"Yes" if approved or status=='APPROVED' else "No"}
------------------------------""")





# ===============================
# 5. VIEW PERFORMANCE (TEMP)
# ===============================

def view_performance(cursor, student_id):
    print("\nFetching performance report...")
    print("Performance tracking will be added later.")
