from models.model_router import get_model

def planning_agent(project_title,project_description,programming_languages,skill_level,model_type="gemini"):
    llm=get_model(model_type)
    prompt=f"""
    You are an experienced software project manager and academic mentor.

    Create a practical development plan for the following project.

    Project Title: {project_title}
    Project Description: {project_description}
    Programming Languages Known by Student: {programming_languages}
    Student Skill Level: {skill_level}

    Prepare the development plan using these sections:

    1. Project Overview
       Briefly explain the development goal.

    2. Development Phases
       Divide the project into logical phases.

    3. Tasks and Activities
       List the specific tasks under each phase.

    4. Technology Requirements
       Identify the tools, frameworks, libraries, and technologies
       suitable for the student's programming languages and skills.

    5. Task Priorities
       Classify tasks as High, Medium, or Low priority.

    6. Estimated Timeline
       Provide a realistic week-by-week development schedule.

    7. Expected Deliverables
       Explain what should be completed at the end of each phase.

    8. Testing Plan
       Describe how each major component should be tested.

    9. Final Milestones
       List the important milestones before project submission.

    Important instructions:
    - Adapt the plan to the student's programming languages.
    - Do not assume Python unless the student selects Python.
    - Do not force the student to learn an unrelated language.
    - Prefer free or open-source tools where possible.
    - Keep the plan achievable for the student's skill level.
    - Avoid unnecessary complexity.
    - Include both implementation and testing activities.
    """
    response=llm.invoke(prompt)
    if isinstance(response.content,str):
        return response.content
    if isinstance(response.content,list):
        return "\n".join(
            item["text"]
            for item in response.content
            if isinstance(item,dict) and "text" in item
        )
    return str(response.content)
if __name__=="__main__":
    print("DEVELOPMENT PLANNING AGENT")
    project_title=input("Enter your project title: ")
    project_description=input("Describe your project briefly: ")
    programming_languages=input("Enter your programming languages: ")
    skill_level=input("Enter skill level (Beginner/Intermediate/Advanced): ")
    model_type=input("Choose model (ollama/gemini): ").strip().lower()
    result=planning_agent(
        project_title,
        project_description,
        programming_languages,
        skill_level,
        model_type
    )
    print("\n DEVELOPMENT ROADMAP \n")
    print(result)