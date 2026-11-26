
from database.operations import (
    register_student,
    create_project,
    save_agent_output,
    get_student_projects,
    get_agent_outputs
)

print("\nTesting ProjectMentor AI Database Integration")

student_id = register_student(
    "Workflow Test Student",
    "workflowtest@example.com",
    "Intermediate"
)

print("Student saved. ID:", student_id)

project_id = create_project(
    student_id,
    "Smart Attendance System",
    "Face recognition based attendance application.",
    "Python"
)

print("Project saved. ID:", project_id)

save_agent_output(
    project_id,
    "Project Recommendation Agent",
    "Three project recommendations generated successfully."
)

save_agent_output(
    project_id,
    "Research Agent",
    "Research analysis generated successfully."
)

print("\nSaved Projects:")
print(get_student_projects(student_id))

print("\nSaved Agent Outputs:")
print(get_agent_outputs(project_id))

print("\nDatabase integration test completed!")
