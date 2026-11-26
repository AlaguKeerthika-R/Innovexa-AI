
from graph.workflow import create_workflow

# Create the LangGraph workflow
app = create_workflow()

# Initial project information
initial_state = {
    "student_id": None,
    "student_name": "Demo Student",
    "skill_level": "Intermediate",

    "project_id": None,
    "project_title": "Smart Attendance System",
    "project_description": "An application that automates student attendance using face recognition.",
    "domain": "Artificial Intelligence",
    "programming_languages": ["Python"],
    "requirements": "Develop a basic face recognition attendance module.",

    "model_type": "ollama",

    "project_recommendation": "",
    "research_output": "",
    "architecture_output": "",
    "technology_output": "",
    "planning_output": "",
    "coding_output": "",
    "documentation_output": "",
    "evaluation_output": "",

    "current_agent": "",
    "messages": [],
    "error": ""
}

print("\n========================================")
print("       PROJECTMENTOR AI WORKFLOW")
print("========================================")

print("\nStarting all eight agents...\n")

# Execute workflow and display progress
try:
    for event in app.stream(initial_state, stream_mode="updates"):

        for agent_name, output in event.items():

            print("\n----------------------------------------")
            print(f"{agent_name.upper()} AGENT COMPLETED")
            print("----------------------------------------")

            print("Output generated successfully.")

    print("\n========================================")
    print("       WORKFLOW COMPLETED!")
    print("========================================")

except Exception as e:
    print("\nWORKFLOW FAILED!")
    print("Error:", str(e))


