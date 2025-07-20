import streamlit as st
from groq import Groq
from PIL import Image
import sqlite3
import os
import hashlib
import datetime
from io import BytesIO
import time
import pandas as pd

# Streamlit page configuration
st.set_page_config(
    page_title="Danmay International Academy",
    page_icon="🏫",
    layout="centered",
    initial_sidebar_state="auto"
)

# Enhanced Color Scheme and Design
st.markdown("""
<style>
    /* Vibrant Color Theme */
    :root {
        --primary: #6a11cb;
        --secondary: #2575fc;
        --accent: #ff758c;
        --success: #4CAF50;
        --warning: #FFC107;
        --danger: #F44336;
        --info: #00BCD4;
        --light: #f8f9fa;
        --dark: #212529;
    }
    
    /* Main container */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4e8f0 100%);
        padding: 1rem;
    }
    
    /* Header styling */
    .header-container {
        text-align: center;
        margin-bottom: 1.5rem;
        padding: 2rem;
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        border-radius: 20px;
        color: white;
        box-shadow: 0 8px 16px rgba(0,0,0,0.15);
        border: 2px solid rgba(255,255,255,0.2);
    }
    
    /* Card styling */
    .card {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 6px 15px rgba(0,0,0,0.1);
        border-left: 5px solid var(--primary);
        transition: all 0.3s ease;
        backdrop-filter: blur(5px);
    }
    
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 20px rgba(0,0,0,0.15);
    }
    
    /* Subject-specific card colors */
    .card-english { border-left-color: #3498db; }
    .card-math { border-left-color: #e74c3c; }
    .card-science { border-left-color: #2ecc71; }
    .card-social { border-left-color: #f39c12; }
    .card-arts { border-left-color: #9b59b6; }
    .card-tech { border-left-color: #1abc9c; }
    .card-pe { border-left-color: #e67e22; }
    .card-religion { border-left-color: #34495e; }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(135deg, var(--accent) 0%, #ff7eb3 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.5rem 1.5rem;
        font-weight: bold;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.2);
    }
    
    /* Form styling */
    .stTextInput>div>div>input, 
    .stTextArea>div>div>textarea,
    .stSelectbox>div>div>select {
        border-radius: 12px;
        padding: 0.5rem 1rem;
        border: 1px solid #ddd;
    }
    
    /* Profile picture styling */
    .profile-pic {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        object-fit: cover;
        margin: 0 auto;
        display: block;
        border: 4px solid var(--primary);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }
    
    /* Timetable styling */
    .timetable {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    .timetable th {
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        color: white;
        padding: 12px;
        text-align: center;
    }
    
    .timetable td {
        padding: 10px;
        text-align: center;
        background: rgba(255,255,255,0.9);
    }
    
    .timetable tr:nth-child(even) td {
        background: rgba(245,245,245,0.9);
    }
    
    /* Status badges */
    .status-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: bold;
        color: white;
    }
    
    .status-pending { background: linear-gradient(135deg, #FFC107 0%, #FFD54F 100%); }
    .status-graded { background: linear-gradient(135deg, #4CAF50 0%, #81C784 100%); }
    .status-late { background: linear-gradient(135deg, #F44336 0%, #E57373 100%); }
    .status-approved { background: linear-gradient(135deg, #00BCD4 0%, #80DEEA 100%); }
    .status-rejected { background: linear-gradient(135deg, #9E9E9E 0%, #E0E0E0 100%); }
    
    /* Message bubbles */
    .message-bubble {
        border-radius: 20px;
        padding: 12px 16px;
        margin: 10px 0;
        max-width: 70%;
        word-wrap: break-word;
        position: relative;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .user-message {
        background: linear-gradient(135deg, #ff9a9e 0%, #fad0c4 100%);
        color: white;
        margin-left: auto;
        border-bottom-right-radius: 5px;
    }
    
    .assistant-message {
        background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
        color: white;
        margin-right: auto;
        border-bottom-left-radius: 5px;
    }
    
    /* Leave request card */
    .leave-card {
        background: rgba(255,255,255,0.9);
        border-radius: 15px;
        padding: 1.2rem;
        margin: 1rem 0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        border-left: 4px solid var(--info);
    }
    
    /* Teacher specific styles */
    .teacher-card {
        background: rgba(255,255,255,0.9);
        border-radius: 15px;
        padding: 1.2rem;
        margin: 1rem 0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        border-left: 4px solid var(--success);
    }
    
    /* Animation for new messages */
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .new-message {
        animation: pulse 1s ease infinite;
    }
    
    /* Attendance status */
    .attendance-present { color: var(--success); font-weight: bold; }
    .attendance-absent { color: var(--danger); font-weight: bold; }
    .attendance-late { color: var(--warning); font-weight: bold; }
    
    /* Parent info card */
    .parent-card {
        background: rgba(255,255,255,0.9);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        border-left: 4px solid var(--primary);
    }
</style>
""", unsafe_allow_html=True)

# Initialize Groq client
api_key = st.secrets.get("GROQ_API_KEY")
if api_key:
    client = Groq(api_key=api_key)
else:
    st.error("GROQ_API_KEY not found in secrets")
    st.stop()

# Database setup with new tables
def init_db():
    conn = sqlite3.connect('school.db')
    c = conn.cursor()
    
    # Create users table with teacher role
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE,
                  password TEXT,
                  role TEXT CHECK(role IN ('admin', 'teacher', 'student')),
                  full_name TEXT,
                  class_level TEXT,
                  profile_pic BLOB,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    # Create homework table
    c.execute('''CREATE TABLE IF NOT EXISTS homework
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  student_id INTEGER,
                  teacher_id INTEGER,
                  subject TEXT,
                  title TEXT,
                  description TEXT,
                  file_data BLOB,
                  file_name TEXT,
                  file_type TEXT,
                  submitted_at TIMESTAMP,
                  due_date TIMESTAMP,
                  status TEXT DEFAULT 'pending',
                  feedback TEXT,
                  FOREIGN KEY(student_id) REFERENCES users(id),
                  FOREIGN KEY(teacher_id) REFERENCES users(id))''')
    
    # Create timetable table
    c.execute('''CREATE TABLE IF NOT EXISTS timetable
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  class_level TEXT,
                  day TEXT,
                  period INTEGER,
                  subject TEXT,
                  teacher_id INTEGER,
                  room TEXT,
                  FOREIGN KEY(teacher_id) REFERENCES users(id))''')
    
    # Create messages table
    c.execute('''CREATE TABLE IF NOT EXISTS messages
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  sender_id INTEGER,
                  receiver_id INTEGER,
                  message TEXT,
                  is_admin_broadcast BOOLEAN DEFAULT 0,
                  is_teacher_broadcast BOOLEAN DEFAULT 0,
                  sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  is_read BOOLEAN DEFAULT 0,
                  FOREIGN KEY(sender_id) REFERENCES users(id),
                  FOREIGN KEY(receiver_id) REFERENCES users(id))''')
    
    # Enhanced parents table
    c.execute('''CREATE TABLE IF NOT EXISTS parents
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  student_id INTEGER UNIQUE,
                  parent_name TEXT,
                  relationship TEXT,
                  address TEXT,
                  phone TEXT,
                  email TEXT,
                  occupation TEXT,
                  nationality TEXT,
                  children_in_school INTEGER,
                  emergency_contact TEXT,
                  emergency_phone TEXT,
                  remarks TEXT,
                  FOREIGN KEY(student_id) REFERENCES users(id))''')
    
    # Create teachers table
    c.execute('''CREATE TABLE IF NOT EXISTS teachers
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER UNIQUE,
                  subjects TEXT,
                  qualification TEXT,
                  phone TEXT,
                  email TEXT,
                  join_date TEXT,
                  FOREIGN KEY(user_id) REFERENCES users(id))''')
    
    # Create attendance table
    c.execute('''CREATE TABLE IF NOT EXISTS attendance
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  date DATE,
                  time_in TIME,
                  time_out TIME,
                  status TEXT,
                  remarks TEXT,
                  FOREIGN KEY(user_id) REFERENCES users(id))''')
    
    # Create leave_requests table
    c.execute('''CREATE TABLE IF NOT EXISTS leave_requests
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  start_date DATE,
                  end_date DATE,
                  reason TEXT,
                  status TEXT DEFAULT 'pending',
                  admin_remarks TEXT,
                  submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  FOREIGN KEY(user_id) REFERENCES users(id))''')
    
    # Insert admin user if not exists
    c.execute("SELECT COUNT(*) FROM users WHERE role='admin'")
    if c.fetchone()[0] == 0:
        admin_password = hashlib.sha256("admin123".encode()).hexdigest()
        c.execute("INSERT INTO users (username, password, role, full_name) VALUES (?, ?, ?, ?)",
                  ("admin", admin_password, "admin", "Administrator"))
    
    conn.commit()
    conn.close()

init_db()

# Database helper functions
def get_db_connection():
    return sqlite3.connect('school.db')

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_user(username, password):
    conn = get_db_connection()
    c = conn.cursor()
    hashed_password = hash_password(password)
    c.execute("SELECT id, username, role, full_name, class_level, profile_pic FROM users WHERE username=? AND password=?", 
              (username, hashed_password))
    user = c.fetchone()
    conn.close()
    return user

def create_user(username, password, role, full_name, class_level=None, profile_pic=None):
    conn = get_db_connection()
    c = conn.cursor()
    hashed_password = hash_password(password)
    try:
        c.execute("INSERT INTO users (username, password, role, full_name, class_level, profile_pic) VALUES (?, ?, ?, ?, ?, ?)",
                  (username, hashed_password, role, full_name, class_level, profile_pic))
        user_id = c.lastrowid
        conn.commit()
        return user_id
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()

def create_teacher(user_id, subjects, qualification, phone, email, join_date):
    conn = get_db_connection()
    c = conn.cursor()
    try:
        c.execute("INSERT INTO teachers (user_id, subjects, qualification, phone, email, join_date) VALUES (?, ?, ?, ?, ?, ?)",
                  (user_id, subjects, qualification, phone, email, join_date))
        conn.commit()
        return True
    except sqlite3.Error:
        return False
    finally:
        conn.close()

def add_parent_info(student_id, parent_name, relationship, address, phone, email, occupation, 
                    nationality, children_in_school, emergency_contact, emergency_phone, remarks):
    conn = get_db_connection()
    c = conn.cursor()
    try:
        c.execute("""INSERT INTO parents 
                    (student_id, parent_name, relationship, address, phone, email, occupation, 
                     nationality, children_in_school, emergency_contact, emergency_phone, remarks)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (student_id, parent_name, relationship, address, phone, email, occupation,
                     nationality, children_in_school, emergency_contact, emergency_phone, remarks))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        # Update if already exists
        c.execute("""UPDATE parents SET 
                    parent_name=?, relationship=?, address=?, phone=?, email=?, occupation=?,
                    nationality=?, children_in_school=?, emergency_contact=?, emergency_phone=?, remarks=?
                    WHERE student_id=?""",
                    (parent_name, relationship, address, phone, email, occupation,
                     nationality, children_in_school, emergency_contact, emergency_phone, remarks, student_id))
        conn.commit()
        return True
    finally:
        conn.close()

def get_teacher_id_by_subject(subject, class_level):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("""SELECT t.user_id 
                 FROM teachers t 
                 JOIN users u ON t.user_id = u.id 
                 WHERE t.subjects LIKE ? AND (u.class_level=? OR u.class_level IS NULL)""",
              (f"%{subject}%", class_level))
    teacher = c.fetchone()
    conn.close()
    return teacher[0] if teacher else None

def get_students(class_level=None):
    conn = get_db_connection()
    c = conn.cursor()
    if class_level:
        c.execute("SELECT id, username, full_name, class_level FROM users WHERE role='student' AND class_level=?", (class_level,))
    else:
        c.execute("SELECT id, username, full_name, class_level FROM users WHERE role='student'")
    students = c.fetchall()
    conn.close()
    return students

def get_timetable(class_level=None, teacher_id=None):
    conn = get_db_connection()
    c = conn.cursor()
    if class_level:
        c.execute("""SELECT t.day, t.period, t.subject, u.full_name as teacher, t.room 
                     FROM timetable t 
                     JOIN users u ON t.teacher_id = u.id 
                     WHERE t.class_level=? 
                     ORDER BY t.day, t.period""", (class_level,))
    elif teacher_id:
        c.execute("""SELECT t.class_level, t.day, t.period, t.subject, t.room 
                     FROM timetable t 
                     WHERE t.teacher_id=?
                     ORDER BY t.day, t.period""", (teacher_id,))
    else:
        c.execute("SELECT class_level, day, period, subject, teacher_id, room FROM timetable ORDER BY class_level, day, period")
    timetable = c.fetchall()
    conn.close()
    return timetable

def submit_homework(student_id, subject, title, description, file_data, file_name, file_type, due_date=None):
    conn = get_db_connection()
    c = conn.cursor()
    
    # Get teacher for this subject and class
    c.execute("SELECT class_level FROM users WHERE id=?", (student_id,))
    class_level = c.fetchone()[0]
    teacher_id = get_teacher_id_by_subject(subject, class_level)
    
    c.execute("""INSERT INTO homework 
                (student_id, teacher_id, subject, title, description, file_data, file_name, file_type, submitted_at, due_date) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
              (student_id, teacher_id, subject, title, description, file_data, file_name, file_type, datetime.datetime.now(), due_date))
    conn.commit()
    conn.close()

def get_student_homework(student_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("""SELECT h.id, h.subject, h.title, h.description, h.file_name, h.submitted_at, h.due_date, h.status, h.feedback, u.full_name as teacher
                 FROM homework h 
                 JOIN users u ON h.teacher_id = u.id
                 WHERE h.student_id=? 
                 ORDER BY h.submitted_at DESC""", (student_id,))
    homework = c.fetchall()
    conn.close()
    return homework

def get_teacher_homework(teacher_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("""SELECT h.id, u.full_name as student, u.class_level, h.subject, h.title, h.description, 
                        h.file_name, h.submitted_at, h.due_date, h.status
                 FROM homework h 
                 JOIN users u ON h.student_id = u.id
                 WHERE h.teacher_id=?
                 ORDER BY h.submitted_at DESC""", (teacher_id,))
    homework = c.fetchall()
    conn.close()
    return homework

def update_homework_status(homework_id, status, feedback):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("UPDATE homework SET status=?, feedback=? WHERE id=?", (status, feedback, homework_id))
    conn.commit()
    conn.close()

def send_message(sender_id, receiver_id, message, is_admin_broadcast=False, is_teacher_broadcast=False):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("""INSERT INTO messages 
                (sender_id, receiver_id, message, is_admin_broadcast, is_teacher_broadcast) 
                VALUES (?, ?, ?, ?, ?)""",
              (sender_id, receiver_id, message, is_admin_broadcast, is_teacher_broadcast))
    conn.commit()
    conn.close()

def get_messages(user_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("""SELECT m.id, m.sender_id, m.receiver_id, m.message, m.sent_at, m.is_read, 
                        u1.username as sender_name, u2.username as receiver_name, 
                        m.is_admin_broadcast, m.is_teacher_broadcast
                 FROM messages m
                 JOIN users u1 ON m.sender_id = u1.id
                 JOIN users u2 ON m.receiver_id = u2.id
                 WHERE m.sender_id=? OR m.receiver_id=?
                 ORDER BY m.sent_at DESC""", (user_id, user_id))
    messages = c.fetchall()
    
    # Mark messages as read
    c.execute("UPDATE messages SET is_read=1 WHERE receiver_id=? AND is_read=0", (user_id,))
    conn.commit()
    conn.close()
    return messages

def get_unread_message_count(user_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM messages WHERE receiver_id=? AND is_read=0", (user_id,))
    count = c.fetchone()[0]
    conn.close()
    return count

def get_parent_info(student_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM parents WHERE student_id=?", (student_id,))
    parent = c.fetchone()
    conn.close()
    return parent

def get_all_parents_info():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("""SELECT p.*, u.full_name as student_name, u.class_level 
                 FROM parents p 
                 JOIN users u ON p.student_id = u.id""")
    parents = c.fetchall()
    conn.close()
    return parents

def get_teachers():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("""SELECT u.id, u.full_name, u.class_level, t.subjects, t.qualification, t.phone, t.email
                 FROM users u
                 JOIN teachers t ON u.id = t.user_id""")
    teachers = c.fetchall()
    conn.close()
    return teachers

def record_attendance(user_id, date, time_in=None, time_out=None, status=None, remarks=None):
    conn = get_db_connection()
    c = conn.cursor()
    
    if time_in:  # Signing in
        c.execute("""INSERT INTO attendance 
                    (user_id, date, time_in, status, remarks)
                    VALUES (?, ?, ?, ?, ?)""",
                  (user_id, date, time_in, status, remarks))
    else:  # Signing out
        c.execute("""UPDATE attendance 
                     SET time_out=?, status=?, remarks=?
                     WHERE user_id=? AND date=?""",
                  (time_out, status, remarks, user_id, date))
    
    conn.commit()
    conn.close()

def get_attendance(user_id, date=None):
    conn = get_db_connection()
    c = conn.cursor()
    
    if date:
        c.execute("SELECT * FROM attendance WHERE user_id=? AND date=?", (user_id, date))
    else:
        c.execute("SELECT * FROM attendance WHERE user_id=? ORDER BY date DESC", (user_id,))
    
    attendance = c.fetchall()
    conn.close()
    return attendance

def submit_leave_request(user_id, start_date, end_date, reason):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("""INSERT INTO leave_requests 
                (user_id, start_date, end_date, reason) 
                VALUES (?, ?, ?, ?)""",
              (user_id, start_date, end_date, reason))
    conn.commit()
    conn.close()

def get_leave_requests(user_id=None):
    conn = get_db_connection()
    c = conn.cursor()
    
    if user_id:
        c.execute("""SELECT l.*, u.full_name 
                     FROM leave_requests l
                     JOIN users u ON l.user_id = u.id
                     WHERE l.user_id=?
                     ORDER BY l.submitted_at DESC""", (user_id,))
    else:
        c.execute("""SELECT l.*, u.full_name 
                     FROM leave_requests l
                     JOIN users u ON l.user_id = u.id
                     ORDER BY l.submitted_at DESC""")
    
    requests = c.fetchall()
    conn.close()
    return requests

def update_leave_request(request_id, status, admin_remarks=None):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("""UPDATE leave_requests 
                 SET status=?, admin_remarks=?
                 WHERE id=?""",
              (status, admin_remarks, request_id))
    conn.commit()
    conn.close()

# Subject lists
JSS_SUBJECTS = [
    "English Language", "Mathematics", "Basic Science", "Social Studies", 
    "Civic Education", "Security Education", "Hausa", "Igbo", "Yoruba", 
    "French", "Cultural and Creative Art", "Basic Technology", "Computer Studies", 
    "Home Economics", "Agricultural Science", "Physical & Health Education", 
    "IRK", "CRK", "Business Studies"
]

SSS_SUBJECTS = [
    "English Language", "Mathematics", "Physics", "Chemistry", "Biology", 
    "Further Mathematics", "Economics", "Government", "Literature in English", 
    "Geography", "History", "Commerce", "Accounting", "Civic Education", 
    "CRS", "IRS", "French", "Hausa", "Igbo", "Yoruba", 
    "Fine Arts", "Music", "Drama", "Business Studies"
]

# Session state management
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.chat_history = []
    st.session_state.disappearing_messages = []

# Helper functions
def get_subject_card_class(subject):
    subject_lower = subject.lower()
    if 'english' in subject_lower or 'literature' in subject_lower:
        return "card-english"
    elif 'math' in subject_lower:
        return "card-math"
    elif 'science' in subject_lower or 'physics' in subject_lower or 'chemistry' in subject_lower or 'biology' in subject_lower:
        return "card-science"
    elif 'social' in subject_lower or 'civic' in subject_lower or 'history' in subject_lower or 'geography' in subject_lower:
        return "card-social"
    elif 'art' in subject_lower or 'music' in subject_lower or 'drama' in subject_lower or 'creative' in subject_lower:
        return "card-arts"
    elif 'tech' in subject_lower or 'computer' in subject_lower:
        return "card-tech"
    elif 'physical' in subject_lower or 'health' in subject_lower or 'pe' in subject_lower:
        return "card-pe"
    elif 'irk' in subject_lower or 'crk' in subject_lower or 'religious' in subject_lower:
        return "card-religion"
    else:
        return ""

def show_disappearing_message(message, message_type="info"):
    """Show a message that disappears after 5 seconds"""
    if message_type == "success":
        msg = st.success(message)
    elif message_type == "error":
        msg = st.error(message)
    elif message_type == "warning":
        msg = st.warning(message)
    else:
        msg = st.info(message)
    
    # Add to session state to track
    st.session_state.disappearing_messages.append({
        "time": time.time(),
        "message": msg,
        "type": message_type
    })

def check_disappearing_messages():
    """Check and remove messages older than 5 seconds"""
    current_time = time.time()
    to_remove = []
    
    for i, msg in enumerate(st.session_state.disappearing_messages):
        if current_time - msg["time"] > 5:
            to_remove.append(i)
    
    # Remove from end to avoid index issues
    for i in sorted(to_remove, reverse=True):
        del st.session_state.disappearing_messages[i]

def render_timetable(timetable):
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    periods = sorted(list(set([period for day, period, subject, teacher, room in timetable])))
    
    st.markdown('<h3 class="section-title">📅 Weekly Timetable</h3>', unsafe_allow_html=True)
    
    for day in days:
        day_schedule = [item for item in timetable if item[0] == day]
        if day_schedule:
            st.markdown(f"<h4>{day}</h4>", unsafe_allow_html=True)
            st.table({
                "Period": [f"Period {item[1]}" for item in day_schedule],
                "Subject": [item[2] for item in day_schedule],
                "Teacher": [item[3] for item in day_schedule],
                "Room": [item[4] for item in day_schedule]
            })

# Landing page
def show_landing_page():
    st.markdown("""
    <div class="header-container">
        <h1 style="font-size: 2.5rem; margin-bottom: 0.5rem;">Welcome to Danmay International Academy</h1>
        <p style="font-size: 1.2rem; margin-bottom: 0;">Excellence in Education for Junior and Senior Secondary Students</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Features grid
    cols = st.columns(3)
    features = [
        {"icon": "📚", "title": "Interactive Learning", "desc": "Engage with our AI-powered learning assistant"},
        {"icon": "📝", "title": "Homework Management", "desc": "Submit and track assignments digitally"},
        {"icon": "⏱️", "title": "Timetable Access", "desc": "View your personalized class schedule"},
        {"icon": "👨‍🏫", "title": "Teacher Portal", "desc": "Dedicated tools for educators"},
        {"icon": "👪", "title": "Parent Connection", "desc": "Stay informed about your child's progress"},
        {"icon": "📱", "title": "Mobile Friendly", "desc": "Access from any device"}
    ]
    
    for i, col in enumerate(cols):
        with col:
            for j in range(2):
                idx = i + (j * 3)
                if idx < len(features):
                    feat = features[idx]
                    st.markdown(f"""
                    <div class="card" style="text-align: center; padding: 1rem;">
                        <div style="font-size: 2rem; margin-bottom: 0.5rem;">{feat['icon']}</div>
                        <h3 style="margin-top: 0;">{feat['title']}</h3>
                        <p>{feat['desc']}</p>
                    </div>
                    """, unsafe_allow_html=True)
    
    # Login section
    st.markdown('<h3 class="section-title" style="text-align: center; margin-top: 2rem;">Login to Your Account</h3>', unsafe_allow_html=True)
    
    with st.form("login_form"):
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        submit = st.form_submit_button("Login", type="primary")
        
        if submit:
            user = verify_user(username, password)
            if user:
                st.session_state.logged_in = True
                st.session_state.user = {
                    "id": user[0],
                    "username": user[1],
                    "role": user[2],
                    "full_name": user[3],
                    "class_level": user[4],
                    "profile_pic": user[5]
                }
                st.rerun()
            else:
                show_disappearing_message("Invalid username or password", "error")
    
    # About school section
    st.markdown("""
    <div style="margin-top: 3rem;">
        <h2 style="text-align: center; color: var(--primary);">About Our School</h2>
        <div class="card" style="text-align: center;">
            <p><strong style="color: var(--primary);">🏆 Premier Secondary Education</strong></p>
            <p>A quality education management system that nurtures intellectual, moral, and social development.</p>
            <div style="display: flex; justify-content: space-around; margin-top: 1rem;">
                <div>
                    <p><strong>🌟 Mission:</strong></p>
                    <p>Stimulating learning environment promoting excellence</p>
                </div>
                <div>
                    <p><strong>✨ Vision:</strong></p>
                    <p>Producing future leaders with strong values</p>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Main application logic
if not st.session_state.logged_in:
    show_landing_page()
    st.stop()

# Check for disappearing messages
check_disappearing_messages()

# Admin Dashboard
if st.session_state.user["role"] == "admin":
    st.sidebar.title("Admin Dashboard")
    menu = st.sidebar.radio(
        "Menu",
        ["Student Management", "Teacher Management", "Homework Review", 
         "Timetable Management", "Parent Information", "Messaging", 
         "Leave Requests", "Admin Profile"]
    )
    
    st.markdown(f'<div class="header-container"><h2>👨‍💼 Admin Dashboard</h2></div>', unsafe_allow_html=True)
    
    if menu == "Student Management":
        st.markdown('<h3 class="section-title">👥 Student Management</h3>', unsafe_allow_html=True)
        
        with st.expander("➕ Add New Student with Parent Details"):
            with st.form("add_student_form"):
                col1, col2 = st.columns(2)
                with col1:
                    new_username = st.text_input("Username")
                    new_password = st.text_input("Password", type="password")
                    full_name = st.text_input("Full Name")
                    class_level = st.selectbox(
                        "Class Level",
                        ["JSS 1", "JSS 2", "JSS 3", "SSS 1", "SSS 2", "SSS 3"]
                    )
                    profile_pic = st.file_uploader("Profile Picture (optional)", type=["jpg", "png", "jpeg"])
                
                with col2:
                    st.markdown("**Parent Information**")
                    parent_name = st.text_input("Parent Name")
                    relationship = st.selectbox("Relationship", ["Father", "Mother", "Guardian"])
                    address = st.text_area("Address")
                    phone = st.text_input("Phone Number")
                    email = st.text_input("Email")
                    occupation = st.text_input("Occupation")
                    nationality = st.text_input("Nationality")
                    children_in_school = st.number_input("Number of Children in School", min_value=1, value=1)
                    emergency_contact = st.text_input("Emergency Contact Name")
                    emergency_phone = st.text_input("Emergency Contact Phone")
                    remarks = st.text_area("Remarks")
                
                if st.form_submit_button("Create Student Account"):
                    if new_username and new_password and full_name and parent_name:
                        pic_data = profile_pic.read() if profile_pic else None
                        student_id = create_user(new_username, new_password, "student", full_name, class_level, pic_data)
                        if student_id:
                            if add_parent_info(student_id, parent_name, relationship, address, phone, email, occupation,
                                            nationality, children_in_school, emergency_contact, emergency_phone, remarks):
                                show_disappearing_message(f"Student account for {full_name} created successfully with parent information!", "success")
                            else:
                                show_disappearing_message("Error saving parent information", "error")
                        else:
                            show_disappearing_message("Username already exists", "error")
                    else:
                        show_disappearing_message("Please fill in all required fields", "warning")
        
        st.markdown('<h4>📋 Student List</h4>', unsafe_allow_html=True)
        students = get_students()
        if students:
            for student in students:
                with st.expander(f"{student[2]} - {student[3]}"):
                    col1, col2 = st.columns([1, 3])
                    with col1:
                        conn = get_db_connection()
                        c = conn.cursor()
                        c.execute("SELECT profile_pic FROM users WHERE id=?", (student[0],))
                        pic_data = c.fetchone()[0]
                        conn.close()
                        
                        if pic_data:
                            st.image(Image.open(BytesIO(pic_data)), width=150)
                        else:
                            st.image(Image.new('RGB', (150, 150), color='gray'), width=150)
                    
                    with col2:
                        with st.form(f"update_form_{student[0]}"):
                            new_full_name = st.text_input("Full Name", value=student[2], key=f"name_{student[0]}")
                            new_class_level = st.selectbox(
                                "Class Level",
                                ["JSS 1", "JSS 2", "JSS 3", "SSS 1", "SSS 2", "SSS 3"],
                                index=["JSS 1", "JSS 2", "JSS 3", "SSS 1", "SSS 2", "SSS 3"].index(student[3]),
                                key=f"class_{student[0]}")
                            new_profile_pic = st.file_uploader("Update Profile Picture", type=["jpg", "png", "jpeg"], key=f"pic_{student[0]}")
                            
                            if st.form_submit_button("Update Profile"):
                                pic_data = new_profile_pic.read() if new_profile_pic else pic_data
                                update_student_profile(student[0], new_full_name, new_class_level, pic_data)
                                show_disappearing_message("Profile updated successfully!", "success")
                                st.rerun()
        else:
            st.info("No students found")
    
    elif menu == "Teacher Management":
        st.markdown('<h3 class="section-title">👨‍🏫 Teacher Management</h3>', unsafe_allow_html=True)
        
        with st.expander("➕ Add New Teacher"):
            with st.form("add_teacher_form"):
                col1, col2 = st.columns(2)
                with col1:
                    username = st.text_input("Username")
                    password = st.text_input("Password", type="password")
                    full_name = st.text_input("Full Name")
                    class_level = st.selectbox(
                        "Assigned Class (optional)",
                        ["None", "JSS 1", "JSS 2", "JSS 3", "SSS 1", "SSS 2", "SSS 3"],
                        index=0
                    )
                    profile_pic = st.file_uploader("Profile Picture (optional)", type=["jpg", "png", "jpeg"])
                
                with col2:
                    subjects = st.multiselect("Subjects Taught", JSS_SUBJECTS + SSS_SUBJECTS)
                    qualification = st.text_input("Qualification")
                    phone = st.text_input("Phone Number")
                    email = st.text_input("Email")
                    join_date = st.date_input("Join Date", datetime.date.today())
                
                if st.form_submit_button("Create Teacher Account"):
                    if username and password and full_name and subjects:
                        pic_data = profile_pic.read() if profile_pic else None
                        class_level = None if class_level == "None" else class_level
                        teacher_id = create_user(username, password, "teacher", full_name, class_level, pic_data)
                        if teacher_id:
                            if create_teacher(teacher_id, ",".join(subjects), qualification, phone, email, join_date.strftime("%Y-%m-%d")):
                                show_disappearing_message(f"Teacher account for {full_name} created successfully!", "success")
                            else:
                                show_disappearing_message("Error creating teacher profile", "error")
                        else:
                            show_disappearing_message("Username already exists", "error")
                    else:
                        show_disappearing_message("Please fill in all required fields", "warning")
        
        st.markdown('<h4>👨‍🏫 Teacher List</h4>', unsafe_allow_html=True)
        teachers = get_teachers()
        if teachers:
            for teacher in teachers:
                with st.expander(f"{teacher[1]} - {teacher[3]}"):
                    col1, col2 = st.columns([1, 3])
                    with col1:
                        conn = get_db_connection()
                        c = conn.cursor()
                        c.execute("SELECT profile_pic FROM users WHERE id=?", (teacher[0],))
                        pic_data = c.fetchone()[0]
                        conn.close()
                        
                        if pic_data:
                            st.image(Image.open(BytesIO(pic_data)), width=150)
                        else:
                            st.image(Image.new('RGB', (150, 150), color='gray'), width=150)
                    
                    with col2:
                        st.write(f"**Class:** {teacher[2] if teacher[2] else 'All Classes'}")
                        st.write(f"**Subjects:** {teacher[3]}")
                        st.write(f"**Qualification:** {teacher[4]}")
                        st.write(f"**Contact:** {teacher[5]} | {teacher[6]}")
        else:
            st.info("No teachers found")
    
    elif menu == "Homework Review":
        st.markdown('<h3 class="section-title">📚 Homework Submissions</h3>', unsafe_allow_html=True)
        
        homework_list = get_all_homework()
        if homework_list:
            for hw in homework_list:
                card_class = get_subject_card_class(hw[3])
                with st.container():
                    status_class = "submitted" if hw[6] == "graded" else "pending"
                    st.markdown(f"""
                    <div class="card {card_class}">
                        <div style="font-weight: bold; font-size: 1.1rem; color: var(--primary);">{hw[3]}: {hw[4]}</div>
                        <div>Student: {hw[1]} (Class: {hw[2]})</div>
                        <div style="font-size: 0.8rem; color: #666;">Submitted: {hw[5]}</div>
                        <div>Status: <span class="status-badge {status_class}">{hw[6]}</span></div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    with st.expander("View Details"):
                        conn = get_db_connection()
                        c = conn.cursor()
                        c.execute("SELECT description, file_name, file_type, feedback FROM homework WHERE id=?", (hw[0],))
                        details = c.fetchone()
                        conn.close()
                        
                        st.write(f"**Description:** {details[0]}")
                        if details[1]:
                            st.write(f"**Attached File:** {details[1]} ({details[2]})")
                        
                        with st.form(f"feedback_form_{hw[0]}"):
                            feedback = st.text_area("Feedback", value=details[3] if details[3] else "")
                            status = st.selectbox("Status", ["pending", "graded"], index=0 if hw[6] == "pending" else 1)
                            
                            if st.form_submit_button("Update"):
                                update_homework_status(hw[0], status, feedback)
                                show_disappearing_message("Homework updated successfully!", "success")
                                st.rerun()
        else:
            st.info("No homework submissions yet")
    
    elif menu == "Timetable Management":
        st.markdown('<h3 class="section-title">⏱️ Timetable Management</h3>', unsafe_allow_html=True)
        
        with st.form("add_timetable_form"):
            col1, col2 = st.columns(2)
            with col1:
                class_level = st.selectbox(
                    "Class Level",
                    ["JSS 1", "JSS 2", "JSS 3", "SSS 1", "SSS 2", "SSS 3"]
                )
                day = st.selectbox(
                    "Day",
                    ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
                )
                subject = st.selectbox(
                    "Subject",
                    JSS_SUBJECTS if class_level.startswith("JSS") else SSS_SUBJECTS
                )
            with col2:
                period = st.number_input("Period", min_value=1, max_value=8, step=1)
                teacher = st.selectbox(
                    "Teacher",
                    [f"{t[0]} - {t[1]}" for t in get_teachers()],
                    format_func=lambda x: x.split(" - ")[1]
                )
                teacher_id = int(teacher.split(" - ")[0]) if teacher else None
                room = st.text_input("Room")
            
            if st.form_submit_button("Add to Timetable"):
                if class_level and day and period and subject and teacher_id and room:
                    conn = get_db_connection()
                    c = conn.cursor()
                    c.execute("INSERT INTO timetable (class_level, day, period, subject, teacher_id, room) VALUES (?, ?, ?, ?, ?, ?)",
                              (class_level, day, period, subject, teacher_id, room))
                    conn.commit()
                    conn.close()
                    show_disappearing_message("Timetable entry added successfully!", "success")
                else:
                    show_disappearing_message("Please fill in all fields", "warning")
        
        st.markdown('<h4>Current Timetable</h4>', unsafe_allow_html=True)
        selected_class = st.selectbox(
            "View Timetable for Class",
            ["JSS 1", "JSS 2", "JSS 3", "SSS 1", "SSS 2", "SSS 3"]
        )
        timetable = get_timetable(selected_class)
        render_timetable(timetable)
    
    elif menu == "Parent Information":
        st.markdown('<h3 class="section-title">👪 Parent Information</h3>', unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["Add/Edit Parent Info", "View All Parents"])
        
        with tab1:
            student_id = st.selectbox(
                "Select Student",
                [f"{s[0]} - {s[2]} ({s[3]})" for s in get_students()],
                index=None,
                placeholder="Select a student"
            )
            
            if student_id:
                student_id = int(student_id.split(" - ")[0])
                existing_info = get_parent_info(student_id)
                
                with st.form("parent_info_form"):
                    parent_name = st.text_input("Parent Name", value=existing_info[2] if existing_info else "")
                    relationship = st.selectbox(
                        "Relationship",
                        ["Father", "Mother", "Guardian"],
                        index=["Father", "Mother", "Guardian"].index(existing_info[3]) if existing_info and existing_info[3] in ["Father", "Mother", "Guardian"] else 0
                    )
                    address = st.text_area("Address", value=existing_info[4] if existing_info else "")
                    phone = st.text_input("Phone Number", value=existing_info[5] if existing_info else "")
                    email = st.text_input("Email", value=existing_info[6] if existing_info else "")
                    occupation = st.text_input("Occupation", value=existing_info[7] if existing_info else "")
                    nationality = st.text_input("Nationality", value=existing_info[8] if existing_info else "")
                    children_in_school = st.number_input("Number of Children in School", min_value=1, value=existing_info[9] if existing_info else 1)
                    emergency_contact = st.text_input("Emergency Contact Name", value=existing_info[10] if existing_info else "")
                    emergency_phone = st.text_input("Emergency Contact Phone", value=existing_info[11] if existing_info else "")
                    remarks = st.text_area("Remarks", value=existing_info[12] if existing_info else "")
                    
                    if st.form_submit_button("Save Parent Information"):
                        if add_parent_info(student_id, parent_name, relationship, address, phone, email, occupation,
                                        nationality, children_in_school, emergency_contact, emergency_phone, remarks):
                            show_disappearing_message("Parent information saved successfully!", "success")
                        else:
                            show_disappearing_message("Error saving parent information", "error")
        
        with tab2:
            parents_info = get_all_parents_info()
            if parents_info:
                for parent in parents_info:
                    with st.expander(f"{parent[13]} - {parent[14]}"):
                        st.markdown(f"""
                        <div class="parent-card">
                            <p><strong>Parent Name:</strong> {parent[2]} ({parent[3]})</p>
                            <p><strong>Address:</strong> {parent[4]}</p>
                            <p><strong>Contact:</strong> {parent[5]} | {parent[6]}</p>
                            <p><strong>Occupation:</strong> {parent[7]}</p>
                            <p><strong>Nationality:</strong> {parent[8]}</p>
                            <p><strong>Children in School:</strong> {parent[9]}</p>
                            <p><strong>Emergency Contact:</strong> {parent[10]} ({parent[11]})</p>
                            <p><strong>Remarks:</strong> {parent[12]}</p>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.info("No parent information available")
    
    elif menu == "Messaging":
        st.markdown('<h3 class="section-title">✉️ Messaging</h3>', unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["Send Message", "Message Inbox"])
        
        with tab1:
            with st.form("message_form"):
                message_type = st.radio("Message Type", ["To Individual", "To All Students", "To All Teachers"])
                
                if message_type == "To Individual":
                    recipient_type = st.radio("Recipient Type", ["Student", "Teacher"])
                    if recipient_type == "Student":
                        recipient = st.selectbox(
                            "Select Student",
                            [f"{s[0]} - {s[2]} ({s[3]})" for s in get_students()],
                            index=None,
                            placeholder="Select a student"
                        )
                    else:
                        recipient = st.selectbox(
                            "Select Teacher",
                            [f"{t[0]} - {t[1]}" for t in get_teachers()],
                            index=None,
                            placeholder="Select a teacher"
                        )
                    receiver_id = int(recipient.split(" - ")[0]) if recipient else None
                    is_broadcast = False
                    is_teacher_broadcast = False
                elif message_type == "To All Students":
                    st.info("This message will be sent to all students")
                    receiver_id = None
                    is_broadcast = True
                    is_teacher_broadcast = False
                else:  # To All Teachers
                    st.info("This message will be sent to all teachers")
                    receiver_id = None
                    is_broadcast = False
                    is_teacher_broadcast = True
                
                message = st.text_area("Message")
                
                if st.form_submit_button("Send Message"):
                    if message:
                        if message_type == "To Individual" and receiver_id:
                            send_message(st.session_state.user["id"], receiver_id, message)
                            show_disappearing_message("Message sent successfully!", "success")
                        elif message_type == "To All Students":
                            students = get_students()
                            for student in students:
                                send_message(st.session_state.user["id"], student[0], message, True, False)
                            show_disappearing_message(f"Message sent to {len(students)} students!", "success")
                        elif message_type == "To All Teachers":
                            teachers = get_teachers()
                            for teacher in teachers:
                                send_message(st.session_state.user["id"], teacher[0], message, False, True)
                            show_disappearing_message(f"Message sent to {len(teachers)} teachers!", "success")
                    else:
                        show_disappearing_message("Please enter a message", "warning")
        
        with tab2:
            messages = get_messages(st.session_state.user["id"])
            if messages:
                for msg in messages:
                    if msg[1] == st.session_state.user["id"]:  # Sent message
                        st.markdown(f"""
                        <div style="display: flex; justify-content: flex-end; margin-bottom: 10px;">
                            <div class="message-bubble user-message">
                                <div><strong>To:</strong> {msg[7]}</div>
                                <div>{msg[3]}</div>
                                <div style="font-size: 0.8rem; text-align: right;">{msg[4]}</div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:  # Received message
                        st.markdown(f"""
                        <div style="display: flex; justify-content: flex-start; margin-bottom: 10px;">
                            <div class="message-bubble assistant-message">
                                <div><strong>From:</strong> {msg[6]}</div>
                                <div>{msg[3]}</div>
                                <div style="font-size: 0.8rem;">{msg[4]}</div>
                                {f'<div style="font-size: 0.7rem; color: #eee;">(Broadcast to all {"teachers" if msg[9] else "students"})</div>' if msg[8] or msg[9] else ''}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.info("No messages yet")
    
    elif menu == "Leave Requests":
        st.markdown('<h3 class="section-title">📝 Leave Requests</h3>', unsafe_allow_html=True)
        
        requests = get_leave_requests()
        if requests:
            for req in requests:
                status_class = req[5].lower()
                with st.container():
                    st.markdown(f"""
                    <div class="leave-card">
                        <div style="display: flex; justify-content: space-between;">
                            <div style="font-weight: bold;">{req[7]}</div>
                            <div><span class="status-badge status-{status_class}">{req[5]}</span></div>
                        </div>
                        <div>Requested: {req[2]} to {req[3]}</div>
                        <div>Reason: {req[4]}</div>
                        {f'<div style="font-size: 0.9rem; margin-top: 0.5rem;">Admin Remarks: {req[6]}</div>' if req[6] else ''}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if req[5] == "pending":
                        with st.expander("Take Action"):
                            with st.form(f"leave_action_{req[0]}"):
                                action = st.radio("Action", ["Approve", "Reject"], key=f"action_{req[0]}")
                                remarks = st.text_area("Remarks", key=f"remarks_{req[0]}")
                                if st.form_submit_button("Submit Decision"):
                                    update_leave_request(req[0], action.lower(), remarks)
                                    show_disappearing_message(f"Leave request {action.lower()}ed!", "success")
                                    st.rerun()
        else:
            st.info("No leave requests pending")
    
    elif menu == "Admin Profile":
        st.markdown('<h3 class="section-title">👤 Admin Profile</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div style="text-align: center;">
                <h4>{st.session_state.user['full_name']}</h4>
                <p>Administrator</p>
            </div>
            """, unsafe_allow_html=True)
        
        with st.form("logout_form"):
            if st.form_submit_button("Logout"):
                st.session_state.logged_in = False
                st.session_state.user = None
                st.rerun()

# Teacher Dashboard
elif st.session_state.user["role"] == "teacher":
    st.sidebar.title("Teacher Dashboard")
    menu = st.sidebar.radio(
        "Menu",
        ["My Timetable", "Homework", "Students", "Attendance", 
         "Leave Requests", "Messaging", "Teacher Profile"]
    )
    
    # Display teacher profile in sidebar
    with st.sidebar:
        if st.session_state.user["profile_pic"]:
            st.image(Image.open(BytesIO(st.session_state.user["profile_pic"])), width=100, caption=st.session_state.user["full_name"])
        else:
            st.image(Image.new('RGB', (100, 100), color='gray'), width=100, caption=st.session_state.user["full_name"])
        
        # Get teacher details
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("SELECT subjects, qualification FROM teachers WHERE user_id=?", (st.session_state.user["id"],))
        teacher_details = c.fetchone()
        conn.close()
        
        if teacher_details:
            st.markdown(f"**Subjects:** {teacher_details[0]}")
            st.markdown(f"**Qualification:** {teacher_details[1]}")
        
        # Show unread message count
        unread_count = get_unread_message_count(st.session_state.user["id"])
        if unread_count > 0:
            st.markdown(f"**Unread Messages:** {unread_count}")
        
        # Attendance status for today
        today = datetime.date.today().strftime("%Y-%m-%d")
        attendance = get_attendance(st.session_state.user["id"], today)
        if attendance:
            status = attendance[0][4]
            if status == "present":
                st.markdown("**Status:** <span class='attendance-present'>Present</span>", unsafe_allow_html=True)
            elif status == "late":
                st.markdown("**Status:** <span class='attendance-late'>Late</span>", unsafe_allow_html=True)
            else:
                st.markdown("**Status:** <span class='attendance-absent'>Absent</span>", unsafe_allow_html=True)
        
        with st.form("logout_form"):
            if st.form_submit_button("Logout"):
                st.session_state.logged_in = False
                st.session_state.user = None
                st.rerun()
    
    st.markdown(f'<div class="header-container"><h2>👨‍🏫 Teacher Dashboard</h2></div>', unsafe_allow_html=True)
    
    if menu == "My Timetable":
        st.markdown('<h3 class="section-title">⏱️ My Timetable</h3>', unsafe_allow_html=True)
        
        timetable = get_timetable(teacher_id=st.session_state.user["id"])
        if timetable:
            render_timetable(timetable)
        else:
            st.info("No timetable assigned yet")
    
    elif menu == "Homework":
        st.markdown('<h3 class="section-title">📝 Homework Management</h3>', unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["Assign Homework", "Submitted Homework"])
        
        with tab1:
            with st.form("assign_homework_form"):
                class_level = st.selectbox(
                    "Class Level",
                    ["JSS 1", "JSS 2", "JSS 3", "SSS 1", "SSS 2", "SSS 3"]
                )
                subject = st.selectbox(
                    "Subject",
                    JSS_SUBJECTS if class_level.startswith("JSS") else SSS_SUBJECTS
                )
                title = st.text_input("Title")
                description = st.text_area("Description")
                due_date = st.date_input("Due Date", datetime.date.today() + datetime.timedelta(days=7))
                homework_file = st.file_uploader("Attach File (optional)", type=["pdf", "docx", "txt"])
                
                if st.form_submit_button("Assign Homework"):
                    if subject and title and description:
                        file_data = homework_file.read() if homework_file else None
                        file_name = homework_file.name if homework_file else None
                        file_type = homework_file.type if homework_file else None
                        
                        # Get all students in the class
                        students = get_students(class_level)
                        if students:
                            for student in students:
                                submit_homework(
                                    student[0],
                                    subject,
                                    title,
                                    description,
                                    file_data,
                                    file_name,
                                    file_type,
                                    due_date.strftime("%Y-%m-%d")
                                )
                            show_disappearing_message(f"Homework assigned to {len(students)} students in {class_level}!", "success")
                        else:
                            show_disappearing_message(f"No students found in {class_level}", "warning")
                    else:
                        show_disappearing_message("Please fill in all required fields", "warning")
        
        with tab2:
            homework_list = get_teacher_homework(st.session_state.user["id"])
            if homework_list:
                for hw in homework_list:
                    card_class = get_subject_card_class(hw[3])
                    with st.container():
                        status_class = "graded" if hw[9] == "graded" else "pending"
                        st.markdown(f"""
                        <div class="card {card_class}">
                            <div style="font-weight: bold; font-size: 1.1rem; color: var(--primary);">{hw[3]}: {hw[4]}</div>
                            <div>Student: {hw[1]} (Class: {hw[2]})</div>
                            <div style="font-size: 0.8rem; color: #666;">Submitted: {hw[7]}</div>
                            <div style="font-size: 0.8rem; color: #666;">Due: {hw[8]}</div>
                            <div>Status: <span class="status-badge {status_class}">{hw[9]}</span></div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        with st.expander("View Details"):
                            st.write(f"**Description:** {hw[5]}")
                            if hw[6]:
                                st.write(f"**Attached File:** {hw[6]}")
                            
                            with st.form(f"feedback_form_{hw[0]}"):
                                feedback = st.text_area("Feedback", value=hw[5] if hw[5] else "")
                                status = st.selectbox("Status", ["pending", "graded"], index=0 if hw[9] == "pending" else 1)
                                
                                if st.form_submit_button("Update"):
                                    update_homework_status(hw[0], status, feedback)
                                    show_disappearing_message("Homework updated successfully!", "success")
                                    st.rerun()
            else:
                st.info("No homework submissions yet")
    
    elif menu == "Students":
        st.markdown('<h3 class="section-title">👥 My Students</h3>', unsafe_allow_html=True)
        
        # Get teacher's subjects
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("SELECT subjects FROM teachers WHERE user_id=?", (st.session_state.user["id"],))
        teacher_subjects = c.fetchone()[0].split(",") if c.fetchone() else []
        conn.close()
        
        # Get all classes where teacher teaches
        timetable = get_timetable(teacher_id=st.session_state.user["id"])
        classes_taught = list(set([item[0] for item in timetable])) if timetable else []
        
        if classes_taught:
            selected_class = st.selectbox("Select Class", classes_taught)
            students = get_students(selected_class)
            
            if students:
                st.markdown(f"### Students in {selected_class}")
                for student in students:
                    with st.expander(student[2]):
                        col1, col2 = st.columns([1, 3])
                        with col1:
                            conn = get_db_connection()
                            c = conn.cursor()
                            c.execute("SELECT profile_pic FROM users WHERE id=?", (student[0],))
                            pic_data = c.fetchone()[0]
                            conn.close()
                            
                            if pic_data:
                                st.image(Image.open(BytesIO(pic_data)), width=100)
                            else:
                                st.image(Image.new('RGB', (100, 100), color='gray'), width=100)
                        
                        with col2:
                            st.write(f"**Username:** {student[1]}")
                            st.write(f"**Class:** {student[3]}")
                            
                            # Get parent info
                            parent = get_parent_info(student[0])
                            if parent:
                                st.markdown("**Parent Information**")
                                st.write(f"**Name:** {parent[2]}")
                                st.write(f"**Contact:** {parent[5]} | {parent[6]}")
            else:
                st.info(f"No students found in {selected_class}")
        else:
            st.info("You are not assigned to any classes yet")
    
    elif menu == "Attendance":
        st.markdown('<h3 class="section-title">📝 Attendance</h3>', unsafe_allow_html=True)
        
        today = datetime.date.today().strftime("%Y-%m-%d")
        attendance = get_attendance(st.session_state.user["id"], today)
        
        if attendance:
            st.info(f"You have already signed in today at {attendance[0][3]}")
            
            if not attendance[0][4]:  # If not signed out
                with st.form("sign_out_form"):
                    remarks = st.text_area("Remarks (optional)")
                    if st.form_submit_button("Sign Out"):
                        record_attendance(
                            st.session_state.user["id"],
                            today,
                            time_out=datetime.datetime.now().strftime("%H:%M:%S"),
                            status="present",
                            remarks=remarks
                        )
                        show_disappearing_message("Signed out successfully!", "success")
                        st.rerun()
        else:
            with st.form("sign_in_form"):
                status = st.radio("Status", ["Present", "Late"], index=0)
                remarks = st.text_area("Remarks (optional)")
                
                if st.form_submit_button("Sign In"):
                    record_attendance(
                        st.session_state.user["id"],
                        today,
                        time_in=datetime.datetime.now().strftime("%H:%M:%S"),
                        status=status.lower(),
                        remarks=remarks
                    )
                    show_disappearing_message("Signed in successfully!", "success")
                    st.rerun()
        
        # Show attendance history
        st.markdown("### Attendance History")
        attendance_history = get_attendance(st.session_state.user["id"])
        if attendance_history:
            attendance_data = []
            for record in attendance_history:
                attendance_data.append({
                    "Date": record[2],
                    "Time In": record[3],
                    "Time Out": record[4],
                    "Status": record[5].capitalize(),
                    "Remarks": record[6]
                })
            st.table(pd.DataFrame(attendance_data))
        else:
            st.info("No attendance records found")
    
    elif menu == "Leave Requests":
        st.markdown('<h3 class="section-title">📝 Leave Requests</h3>', unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["New Request", "My Requests"])
        
        with tab1:
            with st.form("leave_request_form"):
                start_date = st.date_input("Start Date", datetime.date.today())
                end_date = st.date_input("End Date", datetime.date.today() + datetime.timedelta(days=1))
                reason = st.text_area("Reason")
                
                if st.form_submit_button("Submit Request"):
                    if start_date and end_date and reason:
                        if end_date >= start_date:
                            submit_leave_request(st.session_state.user["id"], start_date, end_date, reason)
                            show_disappearing_message("Leave request submitted successfully!", "success")
                            st.rerun()
                        else:
                            show_disappearing_message("End date must be after start date", "error")
                    else:
                        show_disappearing_message("Please fill in all fields", "warning")
        
        with tab2:
            requests = get_leave_requests(st.session_state.user["id"])
            if requests:
                for req in requests:
                    status_class = req[5].lower()
                    with st.container():
                        st.markdown(f"""
                        <div class="leave-card">
                            <div style="display: flex; justify-content: space-between;">
                                <div style="font-weight: bold;">{req[2]} to {req[3]}</div>
                                <div><span class="status-badge status-{status_class}">{req[5]}</span></div>
                            </div>
                            <div>Reason: {req[4]}</div>
                            {f'<div style="font-size: 0.9rem; margin-top: 0.5rem;">Admin Remarks: {req[6]}</div>' if req[6] else ''}
                            <div style="font-size: 0.8rem; color: #666;">Submitted: {req[7]}</div>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.info("No leave requests submitted yet")
    
    elif menu == "Messaging":
        st.markdown('<h3 class="section-title">✉️ Messaging</h3>', unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["Send Message", "Message Inbox"])
        
        with tab1:
            with st.form("message_form"):
                message_type = st.radio("Message Type", ["To Admin", "To Student"])
                
                if message_type == "To Admin":
                    st.info("This message will be sent to the admin")
                    receiver_id = None  # Will be handled in send logic
                else:
                    student = st.selectbox(
                        "Select Student",
                        [f"{s[0]} - {s[2]} ({s[3]})" for s in get_students()],
                        index=None,
                        placeholder="Select a student"
                    )
                    receiver_id = int(student.split(" - ")[0]) if student else None
                
                message = st.text_area("Message")
                
                if st.form_submit_button("Send Message"):
                    if message:
                        if message_type == "To Admin":
                            # Get admin ID
                            conn = get_db_connection()
                            c = conn.cursor()
                            c.execute("SELECT id FROM users WHERE role='admin' LIMIT 1")
                            admin_id = c.fetchone()[0]
                            conn.close()
                            
                            send_message(st.session_state.user["id"], admin_id, message)
                            show_disappearing_message("Message sent to admin!", "success")
                        elif message_type == "To Student" and receiver_id:
                            send_message(st.session_state.user["id"], receiver_id, message)
                            show_disappearing_message("Message sent to student!", "success")
                    else:
                        show_disappearing_message("Please enter a message", "warning")
        
        with tab2:
            messages = get_messages(st.session_state.user["id"])
            if messages:
                for msg in messages:
                    if msg[1] == st.session_state.user["id"]:  # Sent message
                        st.markdown(f"""
                        <div style="display: flex; justify-content: flex-end; margin-bottom: 10px;">
                            <div class="message-bubble user-message">
                                <div><strong>To:</strong> {msg[7]}</div>
                                <div>{msg[3]}</div>
                                <div style="font-size: 0.8rem; text-align: right;">{msg[4]}</div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:  # Received message
                        st.markdown(f"""
                        <div style="display: flex; justify-content: flex-start; margin-bottom: 10px;">
                            <div class="message-bubble assistant-message">
                                <div><strong>From:</strong> {msg[6]}</div>
                                <div>{msg[3]}</div>
                                <div style="font-size: 0.8rem;">{msg[4]}</div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.info("No messages yet")
    
    elif menu == "Teacher Profile":
        st.markdown('<h3 class="section-title">👤 My Profile</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.session_state.user["profile_pic"]:
                st.image(Image.open(BytesIO(st.session_state.user["profile_pic"])), width=150, caption="Current Profile Picture")
            else:
                st.image(Image.new('RGB', (150, 150), color='gray'), width=150, caption="No Profile Picture")
        
        with col2:
            # Get teacher details
            conn = get_db_connection()
            c = conn.cursor()
            c.execute("""SELECT t.subjects, t.qualification, t.phone, t.email, t.join_date 
                         FROM teachers t 
                         WHERE t.user_id=?""", (st.session_state.user["id"],))
            teacher_details = c.fetchone()
            conn.close()
            
            if teacher_details:
                st.markdown(f"""
                <div style="margin-top: 20px;">
                    <p><strong>Full Name:</strong> {st.session_state.user['full_name']}</p>
                    <p><strong>Class:</strong> {st.session_state.user['class_level'] if st.session_state.user['class_level'] else 'Not assigned'}</p>
                    <p><strong>Subjects:</strong> {teacher_details[0]}</p>
                    <p><strong>Qualification:</strong> {teacher_details[1]}</p>
                    <p><strong>Phone:</strong> {teacher_details[2]}</p>
                    <p><strong>Email:</strong> {teacher_details[3]}</p>
                    <p><strong>Join Date:</strong> {teacher_details[4]}</p>
                </div>
                """, unsafe_allow_html=True)

# Student Dashboard
else:
    st.sidebar.title("Student Dashboard")
    menu = st.sidebar.radio(
        "Menu",
        ["Learning Assistant", "Homework", "Timetable", "Messages", "My Profile"]
    )
    
    # Display student profile in sidebar
    with st.sidebar:
        if st.session_state.user["profile_pic"]:
            st.image(Image.open(BytesIO(st.session_state.user["profile_pic"])), width=100, caption=st.session_state.user["full_name"])
        else:
            st.image(Image.new('RGB', (100, 100), color='gray'), width=100, caption=st.session_state.user["full_name"])
        st.markdown(f"**Class:** {st.session_state.user['class_level']}")
        
        # Show unread message count
        unread_count = get_unread_message_count(st.session_state.user["id"])
        if unread_count > 0:
            st.markdown(f"**Unread Messages:** {unread_count}")
        
        with st.form("logout_form"):
            if st.form_submit_button("Logout"):
                st.session_state.logged_in = False
                st.session_state.user = None
                st.rerun()
    
    st.markdown(f'<div class="header-container"><h2>👤 Student Dashboard</h2></div>', unsafe_allow_html=True)
    
    if menu == "Learning Assistant":
        st.markdown('<h3 class="section-title">📚 Learning Assistant</h3>', unsafe_allow_html=True)
        
        # Display chat history
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                st.markdown(f"""
                <div class="stChatMessage user-message">
                    <div style="display: flex; align-items: center; gap: 10px;">
                        <div style="font-weight: bold; font-size: 1.2rem;">👤 You:</div>
                        <div>{message["content"]}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="stChatMessage assistant-message">
                    <div style="display: flex; align-items: center; gap: 10px;">
                        <div style="font-weight: bold; font-size: 1.2rem;">🏫 Assistant:</div>
                        <div>{message["content"]}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # Chat input
        user_prompt = st.chat_input("💬 Ask your educational question...")
        
        if user_prompt:
            # Add user message to chat
            st.session_state.chat_history.append({"role": "user", "content": user_prompt})
            
            # Prepare messages for LLM
            messages = [
                {
                    "role": "system", 
                    "content": f"""You are Danmay International Academy's educational assistant for a secondary student in {st.session_state.user['class_level']}.
                    
                    STRICT RULES:
                    1. ONLY respond to educational questions related to school subjects, homework, or school activities
                    2. For non-educational questions, respond: "I'm sorry, I can only assist with educational matters. Please ask about your school work or subjects."
                    3. Maintain a professional, encouraging tone suitable for secondary students
                    4. Adapt explanations to {st.session_state.user['class_level']} level
                    5. Never provide personal opinions or non-educational advice
                    
                    Current Subjects: {JSS_SUBJECTS if st.session_state.user['class_level'].startswith('JSS') else SSS_SUBJECTS}
                    
                    School Values: Excellence, Discipline, Moral Values"""
                },
                *st.session_state.chat_history
            ]

            # Get LLM response
            response = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=messages
            )

            assistant_response = response.choices[0].message.content
            st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})
            st.rerun()
    
    elif menu == "Homework":
        st.markdown('<h3 class="section-title">📝 Homework</h3>', unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["Submit Homework", "My Submissions"])
        
        with tab1:
            with st.form("homework_form"):
                subject = st.selectbox(
                    "Subject",
                    JSS_SUBJECTS if st.session_state.user['class_level'].startswith('JSS') else SSS_SUBJECTS
                )
                title = st.text_input("Title")
                description = st.text_area("Description")
                homework_file = st.file_uploader("Upload Homework File", type=["pdf", "docx", "txt"])
                
                if st.form_submit_button("Submit Homework"):
                    if subject and title and description:
                        file_data = homework_file.read() if homework_file else None
                        file_name = homework_file.name if homework_file else None
                        file_type = homework_file.type if homework_file else None
                        
                        submit_homework(
                            st.session_state.user["id"],
                            subject,
                            title,
                            description,
                            file_data,
                            file_name,
                            file_type
                        )
                        show_disappearing_message("Homework submitted successfully!", "success")
                    else:
                        show_disappearing_message("Please fill in all required fields", "warning")
        
        with tab2:
            homework_list = get_student_homework(st.session_state.user["id"])
            if homework_list:
                for hw in homework_list:
                    card_class = get_subject_card_class(hw[1])
                    with st.container():
                        status_class = "graded" if hw[7] == "graded" else "pending"
                        st.markdown(f"""
                        <div class="card {card_class}">
                            <div style="font-weight: bold; font-size: 1.1rem; color: var(--primary);">{hw[1]}: {hw[2]}</div>
                            <div>{hw[3]}</div>
                            <div style="font-size: 0.8rem; color: #666;">Submitted: {hw[5]}</div>
                            <div style="font-size: 0.8rem; color: #666;">Due: {hw[6]}</div>
                            <div>Status: <span class="status-badge {status_class}">{hw[7]}</span></div>
                            <div>Teacher: {hw[9]}</div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if hw[4]:  # If file exists
                            st.write(f"**Attached file:** {hw[4]}")
                        
                        if hw[8]:  # If feedback exists
                            st.markdown(f"**Feedback:** {hw[8]}")
            else:
                st.info("You haven't submitted any homework yet")
    
    elif menu == "Timetable":
        st.markdown('<h3 class="section-title">⏱️ My Timetable</h3>', unsafe_allow_html=True)
        
        timetable = get_timetable(st.session_state.user["class_level"])
        if timetable:
            render_timetable(timetable)
        else:
            st.info("Timetable not available for your class yet")
    
    elif menu == "Messages":
        st.markdown('<h3 class="section-title">✉️ Messages</h3>', unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["Contact Teacher", "My Messages"])
        
        with tab1:
            with st.form("contact_teacher_form"):
                # Get teachers for this student's class
                timetable = get_timetable(st.session_state.user["class_level"])
                if timetable:
                    teacher_ids = list(set([item[3] for item in timetable]))
                    teachers = []
                    for teacher_id in teacher_ids:
                        conn = get_db_connection()
                        c = conn.cursor()
                        c.execute("SELECT id, full_name FROM users WHERE id=?", (teacher_id,))
                        teacher = c.fetchone()
                        conn.close()
                        if teacher:
                            teachers.append(teacher)
                    
                    teacher = st.selectbox(
                        "Select Teacher",
                        [f"{t[0]} - {t[1]}" for t in teachers],
                        index=None,
                        placeholder="Select a teacher"
                    )
                    receiver_id = int(teacher.split(" - ")[0]) if teacher else None
                else:
                    st.info("No teachers assigned to your class yet")
                    receiver_id = None
                
                message = st.text_area("Message")
                
                if st.form_submit_button("Send Message"):
                    if message and receiver_id:
                        send_message(st.session_state.user["id"], receiver_id, message)
                        show_disappearing_message("Message sent to teacher!", "success")
                    else:
                        show_disappearing_message("Please select a teacher and enter a message", "warning")
        
        with tab2:
            messages = get_messages(st.session_state.user["id"])
            if messages:
                for msg in messages:
                    if msg[1] == st.session_state.user["id"]:  # Sent message
                        st.markdown(f"""
                        <div style="display: flex; justify-content: flex-end; margin-bottom: 10px;">
                            <div class="message-bubble user-message">
                                <div><strong>To:</strong> {msg[7]}</div>
                                <div>{msg[3]}</div>
                                <div style="font-size: 0.8rem; text-align: right;">{msg[4]}</div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:  # Received message
                        st.markdown(f"""
                        <div style="display: flex; justify-content: flex-start; margin-bottom: 10px;">
                            <div class="message-bubble assistant-message">
                                <div><strong>From:</strong> {msg[6]}</div>
                                <div>{msg[3]}</div>
                                <div style="font-size: 0.8rem;">{msg[4]}</div>
                                {f'<div style="font-size: 0.7rem; color: #eee;">(Broadcast to all students)</div>' if msg[8] else ''}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.info("No messages yet")
    
    elif menu == "My Profile":
        st.markdown('<h3 class="section-title">👤 My Profile</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.session_state.user["profile_pic"]:
                st.image(Image.open(BytesIO(st.session_state.user["profile_pic"])), width=150, caption="Current Profile Picture")
            else:
                st.image(Image.new('RGB', (150, 150), color='gray'), width=150, caption="No Profile Picture")
        
        with col2:
            st.markdown(f"""
            <div style="margin-top: 20px;">
                <p><strong>Username:</strong> {st.session_state.user['username']}</p>
                <p><strong>Full Name:</strong> {st.session_state.user['full_name']}</p>
                <p><strong>Class:</strong> {st.session_state.user['class_level']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Students can't edit their profile - only view
        st.info("Please contact the admin if you need to update your profile information")
        
        # Show parent information if available
        parent_info = get_parent_info(st.session_state.user["id"])
        if parent_info:
            st.markdown('<h3 class="section-title">👪 Parent Information</h3>', unsafe_allow_html=True)
            st.markdown(f"""
            <div class="parent-card">
                <p><strong>Parent Name:</strong> {parent_info[2]} ({parent_info[3]})</p>
                <p><strong>Address:</strong> {parent_info[4]}</p>
                <p><strong>Contact:</strong> {parent_info[5]} | {parent_info[6]}</p>
                <p><strong>Occupation:</strong> {parent_info[7]}</p>
                <p><strong>Nationality:</strong> {parent_info[8]}</p>
                <p><strong>Children in School:</strong> {parent_info[9]}</p>
                <p><strong>Emergency Contact:</strong> {parent_info[10]} ({parent_info[11]})</p>
            </div>
            """, unsafe_allow_html=True)
