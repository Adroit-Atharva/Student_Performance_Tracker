-- ============================================
-- Student Course and Performance Tracker Schema
-- ============================================

-- Drop existing tables (for clean re-runs)
DROP TABLE IF EXISTS performance_records, enrollments, courses, teachers, students CASCADE;

-- =====================
-- 1. Students
-- =====================
CREATE TABLE students (
    student_id VARCHAR(20) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    semester INT NOT NULL DEFAULT 1
);

-- =====================
-- 2. Teachers
-- =====================
CREATE TABLE teachers (
    teacher_id VARCHAR(20) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    department VARCHAR(100)
);

-- =====================
-- 3. Courses
-- =====================
CREATE TABLE courses (
    course_id SERIAL PRIMARY KEY,
    course_name VARCHAR(100) NOT NULL,
    course_code VARCHAR(50) UNIQUE NOT NULL,
    teacher_id INT REFERENCES teachers(teacher_id) ON DELETE SET NULL,
    semester INT NOT NULL
);

-- =====================
-- 4. Enrollments (Student ↔ Course relationship)
-- =====================
CREATE TABLE enrollments (
    enrollment_id SERIAL PRIMARY KEY,
    student_id VARCHAR(20) REFERENCES students(student_id) ON DELETE CASCADE,
    course_id INT REFERENCES courses(course_id) ON DELETE CASCADE,
    enrollment_date DATE DEFAULT CURRENT_DATE,
    status VARCHAR(20) DEFAULT 'PENDING',
    is_approved BOOLEAN DEFAULT FALSE
);

-- =====================
-- 5. Performance Records
-- =====================
CREATE TABLE performance_records (
    record_id SERIAL PRIMARY KEY,
    student_id VARCHAR(20) REFERENCES students(student_id) ON DELETE CASCADE,
    course_id INT REFERENCES courses(course_id) ON DELETE CASCADE,
    assignments_completed INT DEFAULT 0,
    assignment_marks FLOAT DEFAULT 0,
    internal_marks FLOAT DEFAULT 0,
    external_marks FLOAT DEFAULT 0,
    attendance_percent FLOAT DEFAULT 0,
    CONSTRAINT unique_performance UNIQUE (student_id, course_id)
);
