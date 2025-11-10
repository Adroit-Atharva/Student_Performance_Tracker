# app/utils/id_generator.py
import re
from app.utils.db import connect_db

_NUM_SUFFIX_RE = re.compile(r"(\d+)$")  # capture trailing digits

def _get_last_id_value(conn, table: str, id_column: str):
    """
    Return the last (largest) id value from table.id_column or None.
    We just fetch the top row ordering by id_column DESC.
    """
    cur = conn.cursor()
    try:
        # Use IDENTIFIER style in caller; here do simple safe formatting
        query = f"SELECT {id_column} FROM {table} ORDER BY {id_column} DESC LIMIT 1;"
        cur.execute(query)
        row = cur.fetchone()
        return row[0] if row else None
    finally:
        cur.close()

def _extract_numeric_suffix(val) -> int:
    """
    Given a value (like 'STU-000142' or '142' or 142), return integer suffix.
    If no digits found, return 0.
    """
    if val is None:
        return 0
    s = str(val).strip()
    m = _NUM_SUFFIX_RE.search(s)
    if m:
        try:
            return int(m.group(1))
        except ValueError:
            return 0
    # fallback: if entire string is digits
    if s.isdigit():
        return int(s)
    return 0

def _format_id(prefix: str, serial: int) -> str:
    """
    Format the ID with prefix and zero padded 6-digit serial.
    Example: prefix='STU', serial=42 -> 'STU-000042'
    """
    return f"{prefix}-{serial:06d}"

def generate_student_id() -> str:
    """
    Generate the next student ID in the form STU-000001, STU-000002, ...
    Uses the current maximum student_id in the students table to compute next.
    """
    conn = None
    try:
        conn = connect_db()
        last = _get_last_id_value(conn, "students", "student_id")
        last_num = _extract_numeric_suffix(last)
        next_num = last_num + 1
        return _format_id("STU", next_num)
    finally:
        if conn:
            conn.close()

def generate_teacher_id() -> str:
    """
    Generate the next teacher ID in the form TCH-000001, TCH-000002, ...
    """
    conn = None
    try:
        conn = connect_db()
        last = _get_last_id_value(conn, "teachers", "teacher_id")
        last_num = _extract_numeric_suffix(last)
        next_num = last_num + 1
        return _format_id("TCH", next_num)
    finally:
        if conn:
            conn.close()
