
from models.model_router import get_model


def project_recommendation_agent(
    domain,
    skill,
    level,
    model_type="gemini"
):

    llm = get_model(model_type)

    prompt = f"""
You are an expert academic project advisor.

A student has provided the following details:

Domain: {domain}
Skill Level: {skill}
Experience Level: {level}

Your task is to recommend EXACTLY THREE different academic projects.

IMPORTANT RULES:
1. Generate exactly 3 projects.
2. All three projects must belong to the selected domain.
3. Match the complexity to the student's skill level.
4. Each project must be different in its purpose and functionality.
5. Prefer practical and implementable academic projects.
6. Do not generate generic or duplicate ideas.
7. Do not ask the student for a project description yet.

Use this exact format:

PROJECT 1

Project Title:
Description:
Key Features:
Suggested Technologies:
Difficulty Level:
Why This Project Is Suitable:

PROJECT 2

Project Title:
Description:
Key Features:
Suggested Technologies:
Difficulty Level:
Why This Project Is Suitable:

PROJECT 3

Project Title:
Description:
Key Features:
Suggested Technologies:
Difficulty Level:
Why This Project Is Suitable:

Do not generate a fourth project.
Do not add an introduction or conclusion.
"""

    response = llm.invoke(prompt)

    return response.content


if __name__ == "__main__":

    result = project_recommendation_agent(
        domain="Artificial Intelligence",
        skill="Intermediate",
        level="Intermediate",
        model_type="gemini"
    )

    print(result)
