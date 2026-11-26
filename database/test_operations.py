
from database.operations import (
    register_student,
    create_project,
    save_agent_output,
    get_student_projects,
    get_agent_outputs
)

# Register a student
student_id = register_student(
    "Demo Student",
    "demo@example.com",
    "Intermediate"
)

print("Student registered:", student_id)

# Create a project
project_id = create_project(
    student_id,
    "Smart Attendance System",
    "An AI-based student attendance application.",
    "Python"
)

print("Project created:", project_id)

# Save agent output
save_agent_output(
    project_id,
    "Project Recommendation Agent",
    "Smart Attendance System project recommendation."
)

print("\nStudent Projects:")
for project in get_student_projects(student_id):
    print(project)

print("\nAgent Outputs:")
for output in get_agent_outputs(project_id):
    print(output)
