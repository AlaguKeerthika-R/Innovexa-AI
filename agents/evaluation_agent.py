
from models.model_router import get_model

def evaluation_agent(
    project_title,
    project_description,
    programming_languages,
    skill_level,
    model_type="ollama"
):
    llm = get_model(model_type)

    prompt = f"""
    You are an experienced academic project evaluator and technical mentor.

    Evaluate the following student project.

    Project Title: {project_title}
    Project Description: {project_description}
    Programming Languages: {programming_languages}
    Student Skill Level: {skill_level}

    Evaluate the project using these sections:

    1. Project Overview
       Briefly summarize the project.

    2. Problem Relevance
       Evaluate the importance of the problem being addressed.

    3. Innovation and Uniqueness
       Identify innovative aspects and possible improvements.

    4. Technical Feasibility
       Evaluate whether the project can be implemented using
       the selected programming languages and technologies.

    5. Architecture Evaluation
       Evaluate the proposed system structure and modules.

    6. Technology Evaluation
       Assess whether the selected technologies are appropriate.

    7. Implementation Challenges
       Identify possible technical difficulties.

    8. Testing and Validation
       Recommend important test cases and validation methods.

    9. Strengths and Weaknesses
       List the major strengths and weaknesses.

    10. Improvement Suggestions
        Provide practical recommendations.

    11. Overall Project Assessment
        Give an overall assessment of project readiness.

    Important instructions:
    - Consider the student's skill level.
    - Do not assume Python unless selected.
    - Do not invent completed features or test results.
    - Clearly distinguish proposed features from implemented features.
    - Give constructive and realistic feedback.
    - Avoid unnecessary complexity.
    - Do not give an arbitrary numerical score without explaining it.
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
    print("===== PROJECT EVALUATION AGENT =====")

    project_title = input("Enter your project title: ")
    project_description = input("Describe your project briefly: ")
    programming_languages = input("Enter programming languages: ")
    skill_level = input(
        "Enter skill level (Beginner/Intermediate/Advanced): "
    )
    model_type = input("Choose model (ollama/gemini): ").strip().lower()

    result = evaluation_agent(
        project_title,
        project_description,
        programming_languages,
        skill_level,
        model_type
    )

    print("\n===== PROJECT EVALUATION REPORT =====\n")
    print(result)
