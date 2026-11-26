
from typing import TypedDict, Optional, List


class ProjectState(TypedDict):

    # Student information
    student_id: Optional[int]
    student_name: str
    skill_level: str

    # Project information
    project_id: Optional[int]
    project_title: str
    project_description: str
    domain: str
    programming_languages: List[str]
    requirements: str

    # Model selection
    model_type: str

    # Agent outputs
    project_recommendation: str
    research_output: str
    architecture_output: str
    technology_output: str
    planning_output: str
    coding_output: str
    documentation_output: str
    evaluation_output: str

    # Workflow tracking
    current_agent: str
    messages: List[str]
    error: str
