
import streamlit as st
import asyncio
import re

from database.db import get_connection, create_tables
# Initialize database tables
create_tables()
from database.operations import (
    register_student,
    create_project,
    save_agent_output
)

from agents.project_agent import project_recommendation_agent
from agents.research_agent import research_agent
from agents.architecture_agent import architecture_agent
from agents.technology_agent import technolgy_recommendation_agent
from agents.planning_agent import planning_agent
from agents.coding_agent import coding_agent
from agents.documentation_agent import documentation_agent
from agents.evaluation_agent import evaluation_agent

from mcp_server.server import mcp


# ==========================================================
# 1. PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="ProjectMentor AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ==========================================================
# 2. PROFESSIONAL PASTEL THEME
# ==========================================================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(
        135deg,
        #E9EAFB 0%,
        #EFF3FC 45%,
        #E5F3F1 100%
    );
    color: #24304A;
    font-family: "Segoe UI", sans-serif;
}

.block-container {
    max-width: 1450px;
    padding-top: 1.4rem;
    padding-bottom: 3rem;
}

[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #E2E5FA 0%,
        #E8EFFB 55%,
        #E0F0ED 100%
    );
    border-right: 1px solid #D5DCEF;
}

[data-testid="stSidebar"] .block-container {
    padding-top: 1.5rem;
}

h1, h2, h3, h4 {
    color: #202B46 !important;
    letter-spacing: -0.5px;
}

p, label, li {
    color: #52617C;
}

[data-testid="stCaptionContainer"] {
    color: #73819A;
}

[data-testid="stHeader"] {
    background: rgba(233,234,251,0.85);
}

.stTextInput input,
.stTextArea textarea {
    background: #F8F9FF !important;
    color: #26324D !important;
    border: 1px solid #CDD5EB !important;
    border-radius: 10px !important;
}

.stTextInput input:focus,
.stTextArea textarea:focus {
    border-color: #8178E8 !important;
    box-shadow: 0 0 0 2px rgba(99,91,190,0.12) !important;
}

.stSelectbox div[data-baseweb="select"],
.stMultiSelect div[data-baseweb="select"] {
    background: #F8F9FF !important;
    border-radius: 10px;
}

[data-testid="stForm"] {
    background: rgba(249,250,255,0.88);
    border: 1px solid #D7DDF0;
    border-radius: 16px;
    padding: 24px;
    box-shadow: 0 5px 20px rgba(61,76,120,0.05);
}

.stButton > button,
.stFormSubmitButton > button {
    background: #DCDDFB !important;
    color: #34317E !important;
    -webkit-text-fill-color: #34317E !important;
    border: 1px solid #BFC2F0 !important;
    border-radius: 10px !important;
    min-height: 44px;
    font-weight: 700 !important;
    transition: all 0.2s ease;
}

.stButton > button p,
.stFormSubmitButton > button p {
    color: #34317E !important;
    -webkit-text-fill-color: #34317E !important;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover {
    background: #C9CBF5 !important;
    color: #29266E !important;
    -webkit-text-fill-color: #29266E !important;
    border-color: #A8ABE9 !important;
    box-shadow: 0 4px 12px rgba(76,70,160,0.12);
    transform: translateY(-1px);
}

.stDownloadButton > button {
    background: #E1F0ED !important;
    color: #245C55 !important;
    border: 1px solid #B8DCD3 !important;
    border-radius: 9px !important;
    font-weight: 600;
}

[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(249,250,255,0.78);
    border: 1px solid #D9DFEF;
    border-radius: 15px;
}

[data-testid="stMetric"] {
    background: #F0F1FD;
    border: 1px solid #D9DDF2;
    border-radius: 12px;
    padding: 15px;
}

[data-testid="stTabs"] button {
    color: #596783;
    font-weight: 600;
}

[data-testid="stTabs"] button[aria-selected="true"] {
    color: #5146A5;
}

[data-testid="stExpander"] {
    background: #F7F8FE;
    border: 1px solid #D8DEEF;
    border-radius: 12px;
}

div[data-testid="stProgressBar"] > div > div {
    background: #7773D9;
}

hr {
    border-color: #D6DDEE;
}

@media (max-width: 900px) {
    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }
}

</style>
""", unsafe_allow_html=True)


# ==========================================================
# 3. SESSION STATE
# ==========================================================

defaults = {
    "active_page": "Dashboard",
    "previous_page": "Dashboard",
    "stage": 1,
    "student": None,
    "history_email": "",
    "recommendations": None,
    "recommendation_titles": [],
    "selected_project": None,
    "project_details": None,
    "outputs": None,
    "project_id": None
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ==========================================================
# 4. HELPER FUNCTIONS
# ==========================================================

def navigate(page):

    st.session_state.previous_page = (
        st.session_state.active_page
    )

    st.session_state.active_page = page


def reset_project():

    st.session_state.stage = 1
    st.session_state.student = None
    st.session_state.recommendations = None
    st.session_state.recommendation_titles = []
    st.session_state.selected_project = None
    st.session_state.project_details = None
    st.session_state.outputs = None
    st.session_state.project_id = None
    st.session_state.active_page = "Create Project"


def go_back(page):

    st.session_state.active_page = page
    st.rerun()


def extract_project_titles(text):

    titles = re.findall(
        r"Project\s*Title\s*:\s*(.+)",
        text,
        flags=re.IGNORECASE
    )

    cleaned = []

    for title in titles:

        title = re.sub(r"\*\*", "", title)
        title = title.strip().strip("#").strip()

        if title and title not in cleaned:
            cleaned.append(title)

    return cleaned[:3]


def get_student_id(student):

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            "SELECT student_id FROM students WHERE email = ?",
            (student["email"],)
        )

        existing = cursor.fetchone()

        if existing:
            return existing["student_id"]

    finally:
        connection.close()

    return register_student(
        student["name"],
        student["email"],
        student["skill_level"]
    )


def save_plan_using_mcp(project_id, plan):

    result = asyncio.run(
        mcp.call_tool(
            "save_project_plan",
            {
                "project_id": project_id,
                "plan": str(plan)
            }
        )
    )

    if getattr(result, "is_error", False):
        raise RuntimeError("MCP could not save the project plan.")

    return plan


# ==========================================================
# 5. SIDEBAR
# ==========================================================

with st.sidebar:

    st.markdown("## 🎓 ProjectMentor AI")
    st.caption("Your intelligent project companion")

    st.divider()

    st.markdown("### WORKSPACE")

    navigation_items = [
        ("Dashboard", "🏠"),
        ("Create Project", "✨"),
        ("My Projects", "📁"),
        ("Agent Workspace", "🤖")
    ]

    for page, icon in navigation_items:

        if st.button(
            f"{icon}  {page}",
            key=f"nav_{page}",
            use_container_width=True
        ):

            navigate(page)
            st.rerun()

    st.divider()

    if st.button(
        "＋ New Project",
        key="new_project_sidebar",
        use_container_width=True
    ):

        reset_project()
        st.rerun()

    if st.session_state.student:

        st.divider()
        st.markdown("### CURRENT PROFILE")
        st.markdown(f"**{st.session_state.student['name']}**")
        st.caption(st.session_state.student["domain"])
        st.caption(st.session_state.student["skill_level"])

    st.divider()
    st.caption("ProjectMentor AI · Version 1.0")


# ==========================================================
# 6. COMMON PAGE HEADER
# ==========================================================

st.caption("PROJECTMENTOR AI  /  INTELLIGENT PROJECT DEVELOPMENT")

if st.session_state.active_page == "Dashboard":
    st.title("Welcome to your workspace")

elif st.session_state.active_page == "Create Project":
    st.title("Create your next project")

elif st.session_state.active_page == "My Projects":
    st.title("My Projects")

elif st.session_state.active_page == "Agent Workspace":
    st.title("AI Development Workspace")

st.divider()


# ==========================================================
# 7. DASHBOARD
# ==========================================================

if st.session_state.active_page == "Dashboard":

    with st.container(border=True):

        st.markdown("### Turn your ideas into reality.")

        st.write(
            "Find academic project ideas that match your skills, "
            "choose the right one and develop it with an AI-powered "
            "team of specialized agents."
        )

        if st.button(
            "✨ Discover Project Ideas",
            use_container_width=True
        ):

            navigate("Create Project")
            st.rerun()

    st.write("")

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute("SELECT COUNT(*) AS total FROM projects")
        total_projects = cursor.fetchone()["total"]

        cursor.execute("SELECT COUNT(*) AS total FROM students")
        total_students = cursor.fetchone()["total"]

    finally:
        connection.close()

    col1, col2, col3 = st.columns(3)

    col1.metric("Projects Created", total_projects)
    col2.metric("Registered Students", total_students)
    col3.metric("AI Agents Available", 8)

    st.write("")
    st.markdown("### What would you like to do?")

    col1, col2 = st.columns(2)

    with col1:

        with st.container(border=True):

            st.markdown("### 💡 Discover Projects")

            st.write(
                "Get three personalized project recommendations "
                "based on your skills and interests."
            )

            if st.button(
                "Explore Ideas →",
                key="dashboard_discover",
                use_container_width=True
            ):

                navigate("Create Project")
                st.rerun()

    with col2:

        with st.container(border=True):

            st.markdown("### 📂 View Your Projects")

            st.write(
                "Access your saved projects and previously generated "
                "development guidance."
            )

            if st.button(
                "View Projects →",
                key="dashboard_projects",
                use_container_width=True
            ):

                navigate("My Projects")
                st.rerun()

    st.write("")
    st.markdown("### How ProjectMentor AI works")

    workflow_cols = st.columns(4)

    workflow = [
        ("01", "Discover", "Get personalized project ideas."),
        ("02", "Select", "Choose the project you like."),
        ("03", "Configure", "Describe your project requirements."),
        ("04", "Develop", "Get guidance from AI agents.")
    ]

    for col, item in zip(workflow_cols, workflow):

        with col:

            with st.container(border=True):

                st.markdown(f"### {item[0]}")
                st.markdown(f"**{item[1]}**")
                st.caption(item[2])


# ==========================================================
# 8. CREATE PROJECT
# ==========================================================

elif st.session_state.active_page == "Create Project":

    if st.button("← Back to Dashboard", key="create_back"):
        go_back("Dashboard")

    # ------------------------------------------------------
    # STAGE 1 - STUDENT PROFILE
    # ------------------------------------------------------

    if st.session_state.stage == 1:

        st.markdown("### Tell us about yourself")

        st.write(
            "Your profile helps us recommend projects suitable "
            "for your knowledge and interests."
        )

        with st.form("student_form"):

            col1, col2 = st.columns(2)

            with col1:

                name = st.text_input(
                    "Full Name",
                    placeholder="Enter your full name"
                )

                skill_level = st.selectbox(
                    "Experience Level",
                    ["Beginner", "Intermediate", "Advanced"]
                )

                domain = st.selectbox(
                    "Area of Interest",
                    [
                        "Artificial Intelligence",
                        "Machine Learning",
                        "Web Development",
                        "Cyber Security",
                        "Data Science",
                        "Internet of Things",
                        "Computer Science"
                    ]
                )

            with col2:

                email = st.text_input(
                    "Email Address",
                    placeholder="you@example.com"
                )

                languages = st.multiselect(
                    "Preferred Programming Languages",
                    [
                        "Python",
                        "Java",
                        "C",
                        "C++",
                        "JavaScript",
                        "C#"
                    ],
                    default=["Python"]
                )

                model_type = st.selectbox(
                    "AI Provider",
                    ["gemini", "ollama"],
                    format_func=lambda x:
                        "Google Gemini" if x == "gemini"
                        else "Local Ollama"
                )

            st.divider()

            submitted = st.form_submit_button(
                "Discover My Project Ideas →",
                use_container_width=True
            )

        if submitted:

            if not name.strip() or not email.strip() or not languages:

                st.error(
                    "Please enter your name, email and programming languages."
                )

            elif not re.match(
                r"^[^@\s]+@[^@\s]+\.[^@\s]+$",
                email.strip()
            ):

                st.error("Please enter a valid email address.")

            else:

                st.session_state.student = {
                    "name": name.strip(),
                    "email": email.strip(),
                    "skill_level": skill_level,
                    "domain": domain,
                    "languages": languages,
                    "model_type": model_type
                }

                st.session_state.stage = 2
                st.rerun()

    # ------------------------------------------------------
    # STAGE 2 - THREE PROJECT RECOMMENDATIONS
    # ------------------------------------------------------

    elif st.session_state.stage == 2:

        student = st.session_state.student

        st.markdown("### Your project preferences")

        col1, col2, col3 = st.columns(3)

        col1.metric("Domain", student["domain"])
        col2.metric("Experience", student["skill_level"])
        col3.metric("Languages", len(student["languages"]))

        st.divider()

        if st.session_state.recommendations is None:

            with st.container(border=True):

                st.markdown("### Discover projects made for you")

                st.write(
                    "Our AI recommendation agent will generate "
                    "three project ideas based on your profile."
                )

                if st.button(
                    "✨ Generate 3 Project Ideas",
                    use_container_width=True
                ):

                    try:

                        with st.spinner(
                            "Analyzing your profile and generating ideas..."
                        ):

                            result = project_recommendation_agent(
                                domain=student["domain"],
                                skill=student["skill_level"],
                                level=student["skill_level"],
                                model_type=student["model_type"]
                            )

                            st.session_state.recommendations = str(result)

                            st.session_state.recommendation_titles = (
                                extract_project_titles(str(result))
                            )

                        st.rerun()

                    except Exception as e:

                        st.error(
                            f"Recommendation generation failed: {e}"
                        )

        else:

            st.markdown("### Recommended project ideas")

            st.markdown(st.session_state.recommendations)

            st.divider()

            titles = st.session_state.recommendation_titles

            if titles:

                st.markdown("### Select one project")

                selected = st.radio(
                    "Choose your preferred project",
                    titles,
                    label_visibility="collapsed"
                )

                if st.button(
                    "Continue with Selected Project →",
                    use_container_width=True
                ):

                    st.session_state.selected_project = selected
                    st.session_state.stage = 3
                    st.rerun()

            else:

                st.warning(
                    "Project titles could not be extracted. "
                    "Enter your preferred title below."
                )

                selected = st.text_input("Project Title")

                if st.button("Continue →"):

                    if selected.strip():

                        st.session_state.selected_project = selected.strip()
                        st.session_state.stage = 3
                        st.rerun()

                    else:
                        st.error("Please enter a project title.")

        if st.button("← Back to Student Profile"):
            st.session_state.stage = 1
            st.rerun()

    # ------------------------------------------------------
    # STAGE 3 - PROJECT CONFIGURATION
    # ------------------------------------------------------

    elif st.session_state.stage == 3:

        st.markdown("### Configure your selected project")

        st.info(
            f"Selected project: {st.session_state.selected_project}"
        )

        with st.form("project_details_form"):

            title = st.text_input(
                "Project Title",
                value=st.session_state.selected_project
            )

            description = st.text_area(
                "Project Description",
                placeholder="Explain what your project should do...",
                height=140
            )

            requirements = st.text_area(
                "Additional Requirements",
                placeholder="Mention the features, modules and constraints...",
                height=110
            )

            submitted = st.form_submit_button(
                "Create Development Workspace →",
                use_container_width=True
            )

        if submitted:

            if not title.strip() or not description.strip():

                st.error(
                    "Project title and description are required."
                )

            else:

                st.session_state.project_details = {
                    "title": title.strip(),
                    "description": description.strip(),
                    "requirements": requirements.strip()
                }

                st.session_state.stage = 4
                navigate("Agent Workspace")
                st.rerun()

        if st.button("← Back to Recommendations"):
            st.session_state.stage = 2
            st.rerun()


# ==========================================================
# 9. MY PROJECTS - CORRECT DATABASE COLUMNS
# ==========================================================

elif st.session_state.active_page == "My Projects":

    if st.button("← Back to Dashboard", key="projects_back"):
        go_back("Dashboard")

    st.caption("YOUR PERSONAL PROJECT LIBRARY")

    current_student = st.session_state.student

    if current_student:

        student_email = current_student["email"]

    else:

        st.markdown("### Find your projects")

        with st.form("project_history_form"):

            entered_email = st.text_input(
                "Registered Email Address",
                placeholder="you@example.com"
            )

            search_projects = st.form_submit_button(
                "View My Projects",
                use_container_width=True
            )

        if not search_projects:

            st.info(
                "Enter the email address used when creating "
                "your projects to access your project history."
            )

            st.stop()

        if not entered_email.strip():

            st.warning("Please enter your email address.")
            st.stop()

        student_email = entered_email.strip()

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT student_id, name
            FROM students
            WHERE email = ?
            """,
            (student_email.strip(),)
        )

        student_record = cursor.fetchone()

        if student_record is None:

            st.info(
                "No account was found with this email address. "
                "Create your first project to get started."
            )

            if st.button("＋ Create New Project"):
                reset_project()
                st.rerun()

        else:

            cursor.execute(
                """
                SELECT
                    project_id,
                    project_title,
                    project_description,
                    programming_languages,
                    status,
                    created_at
                FROM projects
                WHERE student_id = ?
                ORDER BY project_id DESC
                """,
                (student_record["student_id"],)
            )

            projects = cursor.fetchall()

            if projects:

                st.markdown(
                    f"### Welcome back, {student_record['name']}"
                )

                st.caption(
                    "Your academic projects and development history."
                )

                col1, col2 = st.columns(2)

                col1.metric("Your Projects", len(projects))

                col2.metric(
                    "Student ID",
                    student_record["student_id"]
                )

                st.divider()

                project_options = {
                    f"{p['project_title']} · Project #{p['project_id']}":
                    p["project_id"]
                    for p in projects
                }

                selected_label = st.selectbox(
                    "Select a project",
                    list(project_options.keys())
                )

                selected_id = project_options[selected_label]

                selected_project = next(
                    p for p in projects
                    if p["project_id"] == selected_id
                )

                with st.container(border=True):

                    st.markdown(
                        f"### {selected_project['project_title']}"
                    )

                    st.caption(
                        f"Project ID: {selected_id} · "
                        f"Status: {selected_project['status']}"
                    )

                    st.write(
                        selected_project["project_description"]
                    )

                    st.caption(
                        "Programming Languages: "
                        f"{selected_project['programming_languages']}"
                    )

                    st.caption(
                        f"Created: {selected_project['created_at']}"
                    )

                st.markdown("### Generated AI Guidance")

                cursor.execute(
                    """
                    SELECT agent_name, output_content
                    FROM agent_outputs
                    WHERE project_id = ?
                    """,
                    (selected_id,)
                )

                saved_outputs = cursor.fetchall()

                if saved_outputs:

                    for index, output in enumerate(saved_outputs):

                        with st.expander(output["agent_name"]):

                            st.markdown(output["output_content"])

                            st.download_button(
                                "Download Report",
                                data=output["output_content"],
                                file_name=(
                                    output["agent_name"].replace(" ", "_")
                                    + ".txt"
                                ),
                                mime="text/plain",
                                key=f"history_{selected_id}_{index}"
                            )

                else:

                    st.info(
                        "No AI-generated reports are available "
                        "for this project yet."
                    )

            else:

                st.markdown("### No projects yet")

                st.write(
                    f"Welcome, {student_record['name']}! "
                    "You haven't created any projects yet."
                )

                st.info(
                    "Once you create a project, it will appear here."
                )

                if st.button(
                    "✨ Create Your First Project",
                    key="first_project_create"
                ):

                    reset_project()
                    st.rerun()

    finally:
        connection.close()


# ==========================================================
# 10. AGENT DEVELOPMENT WORKSPACE
# ==========================================================

elif st.session_state.active_page == "Agent Workspace":

    if st.button(
        "← Back to Project Configuration",
        key="workspace_back"
    ):

        navigate("Create Project")
        st.session_state.stage = 3
        st.rerun()

    if st.session_state.stage != 4:

        st.info(
            "Create and configure a project before opening "
            "its development workspace."
        )

        if st.button("Create a Project →"):
            navigate("Create Project")
            st.rerun()

    else:

        student = st.session_state.student
        details = st.session_state.project_details

        st.markdown(f"## {details['title']}")

        st.caption(
            f"{student['domain']} · {student['skill_level']} · "
            f"{', '.join(student['languages'])}"
        )

        st.divider()

        agent_names = [
            "Research Agent",
            "Architecture Agent",
            "Technology Recommendation Agent",
            "Planning Agent",
            "Coding Agent",
            "Documentation Agent",
            "Evaluation Agent"
        ]

        st.markdown("### Your AI development team")

        agent_cols = st.columns(4)

        for i, agent_name in enumerate(agent_names):

            with agent_cols[i % 4]:

                with st.container(border=True):

                    st.caption(f"AGENT {i + 1}")
                    st.markdown(f"**{agent_name}**")
                    st.caption("Specialized AI assistant")

        st.write("")

        if st.session_state.outputs is None:

            st.info(
                "Run the development pipeline to generate research, "
                "architecture, technology recommendations, planning, "
                "code, documentation and evaluation."
            )

            if st.button(
                "▶ Start AI Development Pipeline",
                use_container_width=True
            ):

                try:

                    student_id = get_student_id(student)

                    project_id = create_project(
                        student_id,
                        details["title"],
                        details["description"],
                        ", ".join(student["languages"])
                    )

                    st.session_state.project_id = project_id

                    outputs = {}

                    progress = st.progress(0)

                    status = st.status(
                        "Starting AI agents...",
                        expanded=True
                    )

                    def execute_agent(agent_name, function):

                        status.write(f"Running {agent_name}...")

                        result = str(function())

                        outputs[agent_name] = result

                        save_agent_output(
                            project_id,
                            agent_name,
                            result
                        )

                        progress.progress(
                            len(outputs) / len(agent_names)
                        )

                        status.write(f"Completed: {agent_name}")

                    # RESEARCH AGENT

                    execute_agent(
                        "Research Agent",
                        lambda: research_agent(
                            details["title"],
                            details["description"],
                            student["model_type"]
                        )
                    )

                    # ARCHITECTURE AGENT

                    execute_agent(
                        "Architecture Agent",
                        lambda: architecture_agent(
                            details["title"],
                            details["description"],
                            student["model_type"]
                        )
                    )

                    # TECHNOLOGY RECOMMENDATION AGENT

                    execute_agent(
                        "Technology Recommendation Agent",
                        lambda: technolgy_recommendation_agent(
                            details["title"],
                            details["description"],
                            student["skill_level"],
                            student["model_type"]
                        )
                    )

                    # PLANNING AGENT + MCP

                    def run_planning():

                        plan = planning_agent(
                            project_title=details["title"],
                            project_description=details["description"],
                            programming_languages=", ".join(
                                student["languages"]
                            ),
                            skill_level=student["skill_level"],
                            model_type=student["model_type"]
                        )

                        save_plan_using_mcp(project_id, plan)

                        return plan

                    execute_agent(
                        "Planning Agent",
                        run_planning
                    )

                    # CODING AGENT

                    execute_agent(
                        "Coding Agent",
                        lambda: coding_agent(
                            project_title=details["title"],
                            project_description=details["description"],
                            programming_language=", ".join(
                                student["languages"]
                            ),
                            module_name="Core Project Implementation",
                            module_requirements=details["requirements"],
                            skill_level=student["skill_level"],
                            model_type=student["model_type"]
                        )
                    )

                    # DOCUMENTATION AGENT

                    execute_agent(
                        "Documentation Agent",
                        lambda: documentation_agent(
                            project_title=details["title"],
                            project_description=details["description"],
                            programming_languages=", ".join(
                                student["languages"]
                            ),
                            skill_level=student["skill_level"],
                            model_type=student["model_type"]
                        )
                    )

                    # EVALUATION AGENT

                    execute_agent(
                        "Evaluation Agent",
                        lambda: evaluation_agent(
                            project_title=details["title"],
                            project_description=details["description"],
                            programming_languages=", ".join(
                                student["languages"]
                            ),
                            skill_level=student["skill_level"],
                            model_type=student["model_type"]
                        )
                    )

                    st.session_state.outputs = outputs

                    status.update(
                        label="All development agents completed!",
                        state="complete",
                        expanded=False
                    )

                    st.rerun()

                except Exception as e:

                    st.error(f"Pipeline error: {e}")

                    st.warning(
                        "Some outputs may already have been saved. "
                        "Check the terminal before running again."
                    )

        else:

            outputs = st.session_state.outputs

            st.success(
                f"Development package ready · "
                f"Project ID: {st.session_state.project_id}"
            )

            col1, col2, col3 = st.columns(3)

            col1.metric("Completed Agents", len(outputs))
            col2.metric("Project ID", st.session_state.project_id)
            col3.metric("Generated Reports", len(outputs))

            st.divider()

            st.markdown("### Explore your AI-generated results")

            tabs = st.tabs(list(outputs.keys()))

            for tab, (agent_name, output) in zip(
                tabs,
                outputs.items()
            ):

                with tab:

                    st.markdown(f"### {agent_name}")
                    st.markdown(output)

                    st.download_button(
                        f"Download {agent_name}",
                        data=output,
                        file_name=(
                            agent_name.replace(" ", "_") + ".txt"
                        ),
                        mime="text/plain",
                        key=f"output_{agent_name}"
                    )

            st.divider()

            complete_report = "\n\n".join(
                f"# {name}\n\n{output}"
                for name, output in outputs.items()
            )

            st.download_button(
                "⬇ Download Complete Development Report",
                data=complete_report,
                file_name="ProjectMentor_AI_Report.txt",
                mime="text/plain",
                use_container_width=True
            )
