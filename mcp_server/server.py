from mcp.server.mcpserver import MCPServer

from database.operations import save_agent_output, add_project_task
from database.db import get_connection

mcp = MCPServer("ProjectMentor AI", version="1.0.0")


@mcp.tool()
def save_project_plan(project_id: int, plan: str) -> str:
    """Save the generated development plan for a project."""
    save_agent_output(project_id, "Planning Agent", plan)
    return "Project plan saved successfully."


@mcp.tool()
def create_project_task(
    project_id: int,
    task_name: str,
    description: str,
    priority: str
) -> str:
    """Create a development task for a project."""
    task_id = add_project_task(
        project_id, task_name, description, priority
    )
    return f"Project task created successfully. Task ID: {task_id}"


@mcp.tool()
def get_project_checklist(project_id: int) -> list:
    """Retrieve all development tasks for a project."""
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT task_id, task_name, description,
                   priority, task_status
            FROM project_tasks
            WHERE project_id = ?
        """, (project_id,))

        return [dict(row) for row in cursor.fetchall()]
    finally:
        connection.close()


if __name__ == "__main__":
    mcp.run(transport="stdio")
