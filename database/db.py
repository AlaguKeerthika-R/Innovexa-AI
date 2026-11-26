
import sqlite3
import os

# Database file location
DATABASE_PATH = os.path.join(
    os.path.dirname(__file__),
    "projectmentor.db"
)

# Establish database connection
def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


# Create all database tables
def create_tables():
    connection = get_connection()
    cursor = connection.cursor()

    # 1. Students table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,
            skill_level TEXT
        )
    """)

    # 2. Projects table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            project_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            project_title TEXT NOT NULL,
            project_description TEXT,
            programming_languages TEXT,
            status TEXT DEFAULT 'Created',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id)
                REFERENCES students(student_id)
        )
    """)

    # 3. Agent outputs table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS agent_outputs (
            output_id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER,
            agent_name TEXT,
            output_content TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (project_id)
                REFERENCES projects(project_id)
        )
    """)

    # 4. Project tasks table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS project_tasks (
            task_id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER,
            task_name TEXT NOT NULL,
            description TEXT,
            priority TEXT,
            task_status TEXT DEFAULT 'Pending',
            FOREIGN KEY (project_id)
                REFERENCES projects(project_id)
        )
    """)

    # 5. Generated files table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS generated_files (
            file_id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER,
            file_name TEXT,
            file_path TEXT,
            file_type TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (project_id)
                REFERENCES projects(project_id)
        )
    """)

    connection.commit()
    connection.close()

    print("All 5 database tables created successfully!")


# Test database creation
if __name__ == "__main__":
    create_tables()
