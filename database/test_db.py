
from database.db import get_connection

connection = get_connection()
cursor = connection.cursor()

# Insert a student
cursor.execute("""
    INSERT INTO students (name, email, skill_level)
    VALUES (?, ?, ?)
""", ("Test Student", "test@example.com", "Intermediate"))

student_id = cursor.lastrowid

# Insert a project
cursor.execute("""
    INSERT INTO projects (
        student_id,
        project_title,
        project_description,
        programming_languages
    )
    VALUES (?, ?, ?, ?)
""", (
    student_id,
    "IntelliHire",
    "AI-powered recruitment platform",
    "Java"
))

connection.commit()

# Retrieve project details
cursor.execute("""
    SELECT
        students.name,
        projects.project_title,
        projects.programming_languages,
        projects.status
    FROM projects
    JOIN students
    ON projects.student_id = students.student_id
""")

projects = cursor.fetchall()

print("\n===== STORED PROJECT DETAILS =====")

for project in projects:
    print("Student:", project["name"])
    print("Project:", project["project_title"])
    print("Language:", project["programming_languages"])
    print("Status:", project["status"])

connection.close()
