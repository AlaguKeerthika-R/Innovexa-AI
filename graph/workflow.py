import asyncio
from mcp_server.server import mcp
from langgraph.graph import StateGraph, START, END

from graph.state import ProjectState

from agents.project_agent import project_recommendation_agent
from agents.research_agent import research_agent
from agents.architecture_agent import architecture_agent
from agents.technology_agent import technolgy_recommendation_agent
from agents.planning_agent import planning_agent
from agents.coding_agent import coding_agent
from agents.documentation_agent import documentation_agent
from agents.evaluation_agent import evaluation_agent

from database.operations import (
    register_student,
    create_project,
    save_agent_output,
    update_project_status
)


def get_languages(state):
    languages = state.get("programming_languages", ["Python"])

    if isinstance(languages, list):
        return ", ".join(languages)

    return languages


# Create student and project records
def database_setup_node(state: ProjectState):

    student_id = state.get("student_id")

    if not student_id:
        student_id = register_student(
            state.get("student_name", "Demo Student"),
            state.get("email", "demo@example.com"),
            state.get("skill_level", "Beginner")
        )

    project_id = create_project(
        student_id,
        state["project_title"],
        state["project_description"],
        get_languages(state)
    )

    print("\nStudent and project saved in database.", flush=True)

    return {
        "student_id": student_id,
        "project_id": project_id
    }


def save_output(state, agent_name, output):
    project_id = state.get("project_id")

    if project_id:
        save_agent_output(project_id, agent_name, output)


def project_node(state: ProjectState):
    print("\nRunning Project Recommendation Agent...", flush=True)

    result = project_recommendation_agent(
        domain=state.get("domain", "Computer Science"),
        skill=state.get("skill_level", "Beginner"),
        level=state.get("skill_level", "Beginner"),
        model_type=state.get("model_type", "ollama")
    )

    save_output(state, "Project Recommendation Agent", result)

    return {"project_recommendation": result}


def research_node(state: ProjectState):
    print("\nRunning Research Agent...", flush=True)

    result = research_agent(
        project_title=state["project_title"],
        project_description=state["project_description"],
        model_type=state.get("model_type", "ollama")
    )

    save_output(state, "Research Agent", result)

    return {"research_output": result}


def architecture_node(state: ProjectState):
    print("\nRunning Architecture Agent...", flush=True)

    result = architecture_agent(
        project_title=state["project_title"],
        project_description=state["project_description"],
        model_type=state.get("model_type", "ollama")
    )

    save_output(state, "Architecture Agent", result)

    return {"architecture_output": result}


def technology_node(state: ProjectState):
    print("\nRunning Technology Recommendation Agent...", flush=True)

    result = technolgy_recommendation_agent(
        project_title=state["project_title"],
        project_description=state["project_description"],
        skill_level=state.get("skill_level", "Beginner"),
        model_type=state.get("model_type", "ollama")
    )

    save_output(state, "Technology Recommendation Agent", result)

    return {"technology_output": result}


def planning_node(state: ProjectState):
    print("\nRunning Planning Agent...", flush=True)

    result = planning_agent(
        project_title=state["project_title"],
        project_description=state["project_description"],
        programming_languages=get_languages(state),
        skill_level=state.get("skill_level", "Beginner"),
        model_type=state.get("model_type", "ollama")
    )

    # Save the plan using the MCP tool
    mcp_result = asyncio.run(
        mcp.call_tool(
            "save_project_plan",
            {
                "project_id": state["project_id"],
                "plan": result
            }
        )
    )

    print("Planning Agent called MCP save_project_plan tool.", flush=True)
    print(mcp_result, flush=True)

    return {"planning_output": result}

def coding_node(state: ProjectState):
    print("\nRunning Coding Agent...", flush=True)

    languages = state.get("programming_languages", ["Python"])

    if isinstance(languages, list):
        programming_language = languages[0] if languages else "Python"
    else:
        programming_language = languages

    result = coding_agent(
        project_title=state["project_title"],
        project_description=state["project_description"],
        programming_language=programming_language,
        module_name="Core Module",
        module_requirements=state.get(
            "requirements",
            "Implement the core functionality."
        ),
        skill_level=state.get("skill_level", "Beginner"),
        model_type=state.get("model_type", "ollama")
    )

    save_output(state, "Coding Agent", result)

    return {"coding_output": result}


def documentation_node(state: ProjectState):
    print("\nRunning Documentation Agent...", flush=True)

    result = documentation_agent(
        project_title=state["project_title"],
        project_description=state["project_description"],
        programming_languages=get_languages(state),
        skill_level=state.get("skill_level", "Beginner"),
        model_type=state.get("model_type", "ollama")
    )

    save_output(state, "Documentation Agent", result)

    return {"documentation_output": result}


def evaluation_node(state: ProjectState):
    print("\nRunning Evaluation Agent...", flush=True)

    result = evaluation_agent(
        project_title=state["project_title"],
        project_description=state["project_description"],
        programming_languages=get_languages(state),
        skill_level=state.get("skill_level", "Beginner"),
        model_type=state.get("model_type", "ollama")
    )

    save_output(state, "Evaluation Agent", result)

    return {"evaluation_output": result}


def completion_node(state: ProjectState):
    update_project_status(state["project_id"], "Completed")
    print("\nProject workflow completed and saved!", flush=True)
    return {}


def create_workflow():

    workflow = StateGraph(ProjectState)

    workflow.add_node("database_setup", database_setup_node)
    workflow.add_node("project", project_node)
    workflow.add_node("research", research_node)
    workflow.add_node("architecture", architecture_node)
    workflow.add_node("technology", technology_node)
    workflow.add_node("planning", planning_node)
    workflow.add_node("coding", coding_node)
    workflow.add_node("documentation", documentation_node)
    workflow.add_node("evaluation", evaluation_node)
    workflow.add_node("completion", completion_node)

    workflow.add_edge(START, "database_setup")
    workflow.add_edge("database_setup", "project")
    workflow.add_edge("project", "research")
    workflow.add_edge("research", "architecture")
    workflow.add_edge("architecture", "technology")
    workflow.add_edge("technology", "planning")
    workflow.add_edge("planning", "coding")
    workflow.add_edge("coding", "documentation")
    workflow.add_edge("documentation", "evaluation")
    workflow.add_edge("evaluation", "completion")
    workflow.add_edge("completion", END)

    return workflow.compile()
