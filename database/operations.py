
from database.db import get_connection


# 1. Register a student
def register_student(name, email, skill_level):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            INSERT INTO students (name, email, skill_level)
            VALUES (?, ?, ?)
        """, (name, email, skill_level))

        connection.commit()
        student_id = cursor.lastrowid
        return student_id

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


# 2. Create a project
def create_project(student_id, title, description, programming_languages):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            INSERT INTO projects (
                student_id,
                project_title,
                project_description,
                programming_languages
            )
            VALUES (?, ?, ?, ?)
        """, (student_id, title, description, programming_languages))

        connection.commit()
        project_id = cursor.lastrowid
        return project_id

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


# 3. Save agent output
def save_agent_output(project_id, agent_name, output_content):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            INSERT INTO agent_outputs (
                project_id,
                agent_name,
                output_content
            )
            VALUES (?, ?, ?)
        """, (project_id, agent_name, output_content))

        connection.commit()

    finally:
        connection.close()


# 4. Add a development task
def add_project_task(project_id, task_name, description, priority):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            INSERT INTO project_tasks (
                project_id,
                task_name,
                description,
                priority
            )
            VALUES (?, ?, ?, ?)
        """, (project_id, task_name, description, priority))

        connection.commit()
        task_id = cursor.lastrowid
        return task_id

    finally:
        connection.close()


# 5. Update project status
def update_project_status(project_id, status):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            UPDATE projects
            SET status = ?
            WHERE project_id = ?
        """, (status, project_id))

        connection.commit()
        return cursor.rowcount > 0

    finally:
        connection.close()


# 6. Retrieve student projects
def get_student_projects(student_id):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT *
            FROM projects
            WHERE student_id = ?
            ORDER BY created_at DESC
        """, (student_id,))

        return [dict(row) for row in cursor.fetchall()]

    finally:
        connection.close()


# 7. Retrieve agent outputs
def get_agent_outputs(project_id):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT *
            FROM agent_outputs
            WHERE project_id = ?
            ORDER BY created_at DESC
        """, (project_id,))

        return [dict(row) for row in cursor.fetchall()]

    finally:
        connection.close()


# 8. Update task status
def update_task_status(task_id, status):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            UPDATE project_tasks
            SET task_status = ?
            WHERE task_id = ?
        """, (status, task_id))

        connection.commit()
        return cursor.rowcount > 0

    finally:
        connection.close()


# 9. Save generated file details
def save_generated_file(project_id, file_name, file_path, file_type):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            INSERT INTO generated_files (
                project_id,
                file_name,
                file_path,
                file_type
            )
            VALUES (?, ?, ?, ?)
        """, (project_id, file_name, file_path, file_type))

        connection.commit()

    finally:
        connection.close()
