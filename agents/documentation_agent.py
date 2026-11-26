
from models.model_router import get_model

def documentation_agent(
    project_title,
    project_description,
    programming_languages,
    skill_level,
    model_type="gemini"
):
    llm = get_model(model_type)

    prompt = f"""
    You are an experienced academic project documentation expert.

    Generate detailed academic documentation for the following project.

    Project Title: {project_title}
    Project Description: {project_description}
    Programming Languages: {programming_languages}
    Student Skill Level: {skill_level}

    Prepare the documentation using these sections:

    1. Abstract
       Summarize the project, its purpose, proposed solution,
       technologies, and expected outcome.

    2. Introduction
       Explain the project background, motivation, and objectives.

    3. Problem Statement
       Clearly describe the problem addressed by the project.

    4. Literature Review
       Discuss relevant existing approaches and technologies.
       Do not invent research papers, authors, or citations.

    5. Existing System
       Explain current approaches and their limitations.

    6. Proposed System
       Explain the proposed solution and its advantages.

    7. System Requirements
       List hardware and software requirements.

    8. System Design
       Explain the architecture, modules, database design,
       and workflow.

    9. Implementation
       Explain how the project can be implemented.
       Adapt the explanation to the selected programming languages.

    10. Testing
        Describe important testing methods and test cases.

    11. Advantages and Applications
        Explain the benefits and real-world applications.

    12. Conclusion and Future Enhancements
        Summarize the project and suggest future improvements.
    
    - Keep each section concise and focused.
    - Generate approximately 100-150 words per section.
    - Avoid repeating the same information.
    - Do not generate unnecessarily lengthy explanations.

    Important instructions:
    - Use formal academic language.
    - Keep the explanations clear and understandable.
    - Adapt the documentation to the actual project.
    - Do not assume Python unless it is selected.
    - Do not invent implementation results or test results.
    - Clearly label planned features as proposed if they
      have not yet been implemented.
    - Do not fabricate references or citations.
    - Make the content suitable for a final-year college project report.
    """

    response = llm.invoke(prompt)

    if isinstance(response.content, str):
        return response.content

    if isinstance(response.content, list):
        return "\n".join(
            item["text"]
            for item in response.content
            if isinstance(item, dict) and "text" in item
        )

    return str(response.content)


if __name__ == "__main__":
    print("===== DOCUMENTATION AGENT =====")

    project_title = input("Enter your project title: ")
    project_description = input("Describe your project briefly: ")
    programming_languages = input("Enter programming languages: ")
    skill_level = input(
        "Enter skill level (Beginner/Intermediate/Advanced): "
    )
    model_type = input("Choose model (ollama/gemini): ").strip().lower()

    result = documentation_agent(
        project_title,
        project_description,
        programming_languages,
        skill_level,
        model_type
    )

    print("\n===== PROJECT DOCUMENTATION =====\n")
    print(result)
