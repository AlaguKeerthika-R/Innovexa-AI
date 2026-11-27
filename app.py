import asyncio
import copy
import html
import re
import time

import streamlit as st

from database.db import get_connection, create_tables
# Initialize database tables
create_tables()
from database.operations import (
    register_student,
    create_project,
    save_agent_output
)

from user_auth import (
    EMAIL_RE,
    init_auth_tables,
    register_user,
    authenticate_user,
    validate_password
)
# Initialize the accounts table
init_auth_tables()

from agents.project_agent import project_recommendation_agent
from agents.research_agent import research_agent
from agents.architecture_agent import architecture_agent
from agents.technology_agent import technolgy_recommendation_agent
from agents.planning_agent import planning_agent
from agents.coding_agent import coding_agent
from agents.documentation_agent import documentation_agent
from agents.evaluation_agent import evaluation_agent

from mcp_server.server import mcp

from theme import THEME_CSS
from animations import (
    ANIM_CSS,
    ALL_AGENT_NAMES,
    agent_cards_html,
    agent_working_html,
    compact,
    get_agent,
    pipeline_tracker_html,
    stage_flow_html,
    terminal_html
)


# ==========================================================
# 1. PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Innovexa AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================================
# 2. THEME  (see theme.py and animations.py)
# ==========================================================

st.markdown(
    THEME_CSS + "\n\n" + ANIM_CSS,
    unsafe_allow_html=True
)


# ==========================================================
# 3. SESSION STATE
# ==========================================================

defaults = {
    "user": None,
    "auth_attempts": 0,
    "auth_lock_until": 0.0,
    "active_page": "Dashboard",
    "previous_page": "Dashboard",
    "stage": 1,
    "student": None,
    "recommendations": None,
    "recommendation_titles": [],
    "selected_project": None,
    "project_details": None,
    "outputs": None,
    "durations": {},
    "project_id": None
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = copy.deepcopy(value)


# ==========================================================
# 4. HELPER FUNCTIONS
# ==========================================================

esc = html.escape


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
    st.session_state.durations = {}
    st.session_state.project_id = None
    st.session_state.active_page = "Create Project"


def sign_out():

    for key, value in defaults.items():
        st.session_state[key] = copy.deepcopy(value)


def go_back(page):

    st.session_state.active_page = page
    st.rerun()


def to_text(result):
    """Agents may return a string or a list of content blocks."""

    if isinstance(result, str):
        return result

    if isinstance(result, list):
        return "\n".join(
            item["text"]
            for item in result
            if isinstance(item, dict) and "text" in item
        )

    return str(result)


def page_header(kicker, title, subtitle=""):

    sub = f"<p>{subtitle}</p>" if subtitle else ""

    st.markdown(
        compact(
            f"""
            <div class="pm-pagehead">
            <div class="pm-kicker">{kicker}</div>
            <h1>{title}</h1>
            {sub}
            </div>
            """
        ),
        unsafe_allow_html=True
    )


def section_title(text):

    st.markdown(
        f'<div class="pm-section">{text}</div>',
        unsafe_allow_html=True
    )


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
# 5. SIGN IN / SIGN UP PAGE
# ==========================================================

def render_auth_page():

    # No sidebar on the login screen.
    st.markdown(
        "<style>"
        "[data-testid='stSidebar'],"
        "[data-testid='stSidebarCollapsedControl'],"
        "[data-testid='collapsedControl']{display:none!important;}"
        "</style>",
        unsafe_allow_html=True
    )

    left, right = st.columns([1.15, 1], gap="large")

    with left:

        st.markdown(
            compact(
                f"""
                <div class="pm-auth">
                <div class="pm-badge"><span class="pm-pulse"></span>8 AI agents online</div>
                <h1>Build your final-year project <span class="pm-grad">with an AI team</span>.</h1>
                <p class="lead">
                From the first idea to research, architecture, code, documentation
                and evaluation, a team of specialised agents guides every step.
                </p>
                {terminal_html("pipeline.log", "innovexa login")}
                </div>
                """
            ),
            unsafe_allow_html=True
        )

    with right:

        st.write("")
        st.write("")

        with st.container(border=True):

            st.markdown(
                compact(
                    """
                    <div class="pm-brand" style="margin:6px 0 10px">
                    <div class="pm-logo">🎓</div>
                    <div><b>Innovexa<span class="pm-grad">.ai</span></b>
                    <small>sign in to your workspace</small></div>
                    </div>
                    """
                ),
                unsafe_allow_html=True
            )

            tab_in, tab_up = st.tabs(["Sign in", "Create account"])

            # ---------------- SIGN IN ----------------

            with tab_in:

                with st.form("signin_form"):

                    si_email = st.text_input(
                        "Email address",
                        placeholder="you@example.com",
                        key="si_email"
                    )

                    si_password = st.text_input(
                        "Password",
                        type="password",
                        placeholder="Your password",
                        key="si_password"
                    )

                    signin = st.form_submit_button(
                        "Sign in →",
                        use_container_width=True
                    )

                if signin:

                    wait = int(
                        st.session_state.auth_lock_until - time.time()
                    )

                    if wait > 0:

                        st.error(
                            f"Too many failed attempts. "
                            f"Please try again in {wait} seconds."
                        )

                    elif not si_email.strip() or not si_password:

                        st.error("Please enter your email and password.")

                    else:

                        ok, message, user = authenticate_user(
                            si_email,
                            si_password
                        )

                        if ok:

                            st.session_state.auth_attempts = 0
                            st.session_state.user = user
                            st.session_state.active_page = "Dashboard"
                            st.rerun()

                        else:

                            st.session_state.auth_attempts += 1

                            if st.session_state.auth_attempts >= 5:
                                st.session_state.auth_lock_until = (
                                    time.time() + 60
                                )
                                st.session_state.auth_attempts = 0

                            st.error(message)

            # ---------------- SIGN UP ----------------

            with tab_up:

                with st.form("signup_form"):

                    su_name = st.text_input(
                        "Full name",
                        placeholder="Your full name",
                        key="su_name"
                    )

                    su_email = st.text_input(
                        "Email address",
                        placeholder="you@example.com",
                        key="su_email"
                    )

                    col1, col2 = st.columns(2)

                    su_password = col1.text_input(
                        "Password",
                        type="password",
                        placeholder="Min. 8 characters",
                        key="su_password"
                    )

                    su_confirm = col2.text_input(
                        "Confirm password",
                        type="password",
                        placeholder="Repeat password",
                        key="su_confirm"
                    )

                    st.caption(
                        "Use at least 8 characters with a letter and a number."
                    )

                    signup = st.form_submit_button(
                        "Create account →",
                        use_container_width=True
                    )

                if signup:

                    if not su_name.strip() or not su_email.strip():

                        st.error("Please enter your name and email address.")

                    elif not EMAIL_RE.match(su_email.strip()):

                        st.error("Please enter a valid email address.")

                    elif su_password != su_confirm:

                        st.error("The two passwords do not match.")

                    else:

                        problem = validate_password(su_password)

                        if problem:

                            st.error(problem)

                        else:

                            ok, message, user = register_user(
                                su_name,
                                su_email,
                                su_password
                            )

                            if ok:

                                st.session_state.user = user
                                st.session_state.active_page = "Dashboard"
                                st.rerun()

                            else:

                                st.error(message)


if st.session_state.user is None:
    render_auth_page()
    st.stop()


# ==========================================================
# 6. SIDEBAR  (signed-in users only)
# ==========================================================

user = st.session_state.user
first_name = user["full_name"].split()[0]

with st.sidebar:

    st.markdown(
        compact(
            """
            <div class="pm-brand">
            <div class="pm-logo">🎓</div>
            <div><b>Innovexa<span class="pm-grad">.ai</span></b>
            <small>v2.0 · agent studio</small></div>
            </div>
            """
        ),
        unsafe_allow_html=True
    )

    st.divider()

    section_title("workspace")

    navigation_items = [
        ("Dashboard", "🏠"),
        ("Create Project", "✨"),
        ("My Projects", "📁"),
        ("Agent Workspace", "🤖")
    ]

    for page, icon in navigation_items:

        is_active = st.session_state.active_page == page

        if st.button(
            f"{icon}  {page}",
            key=f"nav_{page}",
            use_container_width=True,
            type="primary" if is_active else "secondary"
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
        section_title("current profile")
        st.markdown(f"**{esc(st.session_state.student['name'])}**")
        st.caption(st.session_state.student["domain"])
        st.caption(st.session_state.student["skill_level"])

    st.divider()

    st.markdown(
        compact(
            f"""
            <div class="pm-user">
            <div class="pm-avatar">{esc(first_name[0].upper())}</div>
            <div><b>{esc(user['full_name'])}</b><small>{esc(user['email'])}</small></div>
            </div>
            """
        ),
        unsafe_allow_html=True
    )

    if st.button(
        "Sign out",
        key="sign_out",
        use_container_width=True
    ):

        sign_out()
        st.rerun()


# ==========================================================
# 7. DASHBOARD
# ==========================================================

if st.session_state.active_page == "Dashboard":

    st.markdown(
        compact(
            f"""
            <div class="pm-hero">
            <div>
            <div class="pm-badge"><span class="pm-pulse"></span>Hi {esc(first_name)} · all agents online</div>
            <h1>Turn ideas into <span class="pm-grad">ship-ready projects</span>.</h1>
            <p class="lead">
            Discover project ideas that match your skills, pick the one you like
            and let eight specialised AI agents research, design, plan, code,
            document and evaluate it with you.
            </p>
            </div>
            {terminal_html("pipeline.log", "innovexa start --agents 8")}
            </div>
            """
        ),
        unsafe_allow_html=True
    )

    st.write("")

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "✨  Discover project ideas",
            key="dashboard_discover",
            use_container_width=True
        ):

            reset_project()
            st.rerun()

    with col2:

        if st.button(
            "📁  Open my projects",
            key="dashboard_projects",
            use_container_width=True
        ):

            navigate("My Projects")
            st.rerun()

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT COUNT(*) AS total
            FROM projects p
            JOIN students s ON p.student_id = s.student_id
            WHERE s.email = ?
            """,
            (user["email"],)
        )
        my_projects = cursor.fetchone()["total"]

        cursor.execute("SELECT COUNT(*) AS total FROM projects")
        total_projects = cursor.fetchone()["total"]

    finally:
        connection.close()

    section_title("overview")

    col1, col2, col3 = st.columns(3)

    col1.metric("Your Projects", my_projects)
    col2.metric("Projects On Platform", total_projects)
    col3.metric("AI Agents", len(ALL_AGENT_NAMES))

    section_title("meet your agent team")

    st.markdown(agent_cards_html(), unsafe_allow_html=True)

    section_title("how it works")

    steps = [
        ("01", "Discover", "Get three personalised project ideas."),
        ("02", "Select", "Choose the project you like best."),
        ("03", "Configure", "Describe what the project should do."),
        ("04", "Develop", "Watch the agents build your package.")
    ]

    cards = "".join(
        f'<div class="pm-card"><span class="no">{n}</span><b>{t}</b><small>{d}</small></div>'
        for n, t, d in steps
    )

    st.markdown(
        f'<div class="pm-grid c4">{cards}</div>',
        unsafe_allow_html=True
    )


# ==========================================================
# 8. CREATE PROJECT
# ==========================================================

elif st.session_state.active_page == "Create Project":

    page_header(
        "~/innovexa / create",
        "Create your next project",
        "Tell us about yourself, pick an idea and configure it."
    )

    st.markdown(
        stage_flow_html(st.session_state.stage),
        unsafe_allow_html=True
    )

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
                    value=user["full_name"],
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

                st.text_input(
                    "Email Address (from your account)",
                    value=user["email"],
                    disabled=True
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

            if not name.strip() or not languages:

                st.error(
                    "Please enter your name and choose at least "
                    "one programming language."
                )

            else:

                st.session_state.student = {
                    "name": name.strip(),
                    "email": user["email"],
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
                    "Our Project Advisor agent will generate "
                    "three project ideas based on your profile."
                )

                animation_slot = st.empty()

                if st.button(
                    "✨ Generate 3 Project Ideas",
                    use_container_width=True
                ):

                    animation_slot.markdown(
                        agent_working_html("Project Advisor Agent", 0),
                        unsafe_allow_html=True
                    )

                    try:

                        result = to_text(
                            project_recommendation_agent(
                                domain=student["domain"],
                                skill=student["skill_level"],
                                level=student["skill_level"],
                                model_type=student["model_type"]
                            )
                        )

                        st.session_state.recommendations = result

                        st.session_state.recommendation_titles = (
                            extract_project_titles(result)
                        )

                        st.rerun()

                    except Exception as e:

                        animation_slot.empty()

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
# 9. MY PROJECTS  (always the signed-in user's own projects)
# ==========================================================

elif st.session_state.active_page == "My Projects":

    page_header(
        "~/innovexa / projects",
        "My Projects",
        "Your academic projects and everything the agents generated."
    )

    if st.button("← Back to Dashboard", key="projects_back"):
        go_back("Dashboard")

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT student_id, name
            FROM students
            WHERE email = ?
            """,
            (user["email"],)
        )

        student_record = cursor.fetchone()

        if student_record is None:

            st.info(
                "You haven't created any projects yet. "
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

                section_title("generated ai guidance")

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

                        icon = get_agent(output["agent_name"])["icon"]

                        with st.expander(
                            f"{icon}  {output['agent_name']}"
                        ):

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

    page_header(
        "~/innovexa / workspace",
        "AI Development Workspace",
        "Eight agents, one pipeline, one complete project package."
    )

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

        chips = "".join(
            f'<span class="pm-chip">{esc(c)}</span>'
            for c in [
                student["domain"],
                student["skill_level"],
                *student["languages"]
            ]
        )

        st.markdown(
            compact(
                f"""
                <div class="pm-project">
                <div class="pm-kicker">selected project</div>
                <h2>{esc(details['title'])}</h2>
                {chips}
                </div>
                """
            ),
            unsafe_allow_html=True
        )

        # Pipeline order = the 7 agents after the Project Advisor,
        # which already ran when the ideas were generated.

        if st.session_state.outputs is None:

            tracker_slot = st.empty()
            stage_slot = st.empty()

            states = ["done"] + ["pending"] * (len(ALL_AGENT_NAMES) - 1)

            tracker_slot.markdown(
                pipeline_tracker_html(ALL_AGENT_NAMES, states),
                unsafe_allow_html=True
            )

            st.info(
                "Run the development pipeline to generate research, "
                "architecture, technology recommendations, planning, "
                "code, documentation and evaluation."
            )

            if st.button(
                "▶ Start AI Development Pipeline",
                use_container_width=True
            ):

                durations = {}
                outputs = {}
                current = 0

                try:

                    student_id = get_student_id(student)

                    project_id = create_project(
                        student_id,
                        details["title"],
                        details["description"],
                        ", ".join(student["languages"])
                    )

                    st.session_state.project_id = project_id

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

                    pipeline = [

                        ("Research Agent", lambda: research_agent(
                            details["title"],
                            details["description"],
                            student["model_type"]
                        )),

                        ("Architecture Agent", lambda: architecture_agent(
                            details["title"],
                            details["description"],
                            student["model_type"]
                        )),

                        ("Technology Recommendation Agent",
                         lambda: technolgy_recommendation_agent(
                             details["title"],
                             details["description"],
                             student["skill_level"],
                             student["model_type"]
                         )),

                        ("Planning Agent", run_planning),

                        ("Coding Agent", lambda: coding_agent(
                            project_title=details["title"],
                            project_description=details["description"],
                            programming_language=", ".join(
                                student["languages"]
                            ),
                            module_name="Core Project Implementation",
                            module_requirements=details["requirements"],
                            skill_level=student["skill_level"],
                            model_type=student["model_type"]
                        )),

                        ("Documentation Agent",
                         lambda: documentation_agent(
                             project_title=details["title"],
                             project_description=details["description"],
                             programming_languages=", ".join(
                                 student["languages"]
                             ),
                             skill_level=student["skill_level"],
                             model_type=student["model_type"]
                         )),

                        ("Evaluation Agent", lambda: evaluation_agent(
                            project_title=details["title"],
                            project_description=details["description"],
                            programming_languages=", ".join(
                                student["languages"]
                            ),
                            skill_level=student["skill_level"],
                            model_type=student["model_type"]
                        ))
                    ]

                    for position, (agent_name, function) in enumerate(
                        pipeline,
                        start=1
                    ):

                        current = position
                        states[position] = "active"

                        tracker_slot.markdown(
                            pipeline_tracker_html(
                                ALL_AGENT_NAMES, states, durations
                            ),
                            unsafe_allow_html=True
                        )

                        # The CSS animation keeps playing in the browser
                        # while Python waits for the model to answer.
                        stage_slot.markdown(
                            agent_working_html(
                                agent_name,
                                position,
                                len(ALL_AGENT_NAMES)
                            ),
                            unsafe_allow_html=True
                        )

                        started = time.time()

                        result = to_text(function())

                        durations[agent_name] = time.time() - started
                        outputs[agent_name] = result

                        save_agent_output(
                            project_id,
                            agent_name,
                            result
                        )

                        states[position] = "done"

                    st.session_state.durations = durations
                    st.session_state.outputs = outputs

                    st.rerun()

                except Exception as e:

                    if current:
                        states[current] = "error"

                    tracker_slot.markdown(
                        pipeline_tracker_html(
                            ALL_AGENT_NAMES, states, durations
                        ),
                        unsafe_allow_html=True
                    )

                    stage_slot.empty()

                    st.error(f"Pipeline error: {e}")

                    st.warning(
                        "Some outputs may already have been saved. "
                        "Check the terminal before running again."
                    )

        else:

            outputs = st.session_state.outputs
            durations = st.session_state.durations

            st.markdown(
                pipeline_tracker_html(
                    ALL_AGENT_NAMES,
                    ["done"] * len(ALL_AGENT_NAMES),
                    durations
                ),
                unsafe_allow_html=True
            )

            st.write("")

            st.success(
                f"Development package ready · "
                f"Project ID: {st.session_state.project_id}"
            )

            col1, col2, col3 = st.columns(3)

            col1.metric("Completed Agents", len(outputs))
            col2.metric("Project ID", st.session_state.project_id)
            col3.metric(
                "Total Run Time",
                f"{sum(durations.values()):.0f}s"
            )

            section_title("your ai-generated results")

            tabs = st.tabs(
                [
                    f"{get_agent(name)['icon']} {get_agent(name)['short']}"
                    for name in outputs.keys()
                ]
            )

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
                file_name="Innovexa_AI_Report.txt",
                mime="text/plain",
                use_container_width=True
            )
