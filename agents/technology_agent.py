from models.model_router import get_model

def technolgy_recommendation_agent(project_title, project_description,skill_level,model_type="gemini"):
    llm=get_model(model_type)
    prompt=f"""
    You are an expert AI technology consultant and software developer.

    Recommend the best technologies for the following academic project.

    Project Title: {project_title}
    Project Description: {project_description}
    Student Skill Level: {skill_level}

    Prepare the recommendations under these sections:

    1. Programming Languages
       Recommend suitable programming languages.

    2. Frontend Technologies
       Suggest suitable Python-compatible frontend frameworks.

    3. Backend Technologies
       Recommend backend frameworks and explain their uses.

    4. AI and Machine Learning Libraries
       Suggest suitable AI models, libraries, and frameworks.

    5. Database Technologies
       Recommend relational and vector databases if required.

    6. Development Tools
       Suggest useful IDEs, version control tools, and testing tools.

    7. Technology Comparison
       Compare the recommended technologies with alternatives.

    8. Final Technology Stack
       Provide one recommended technology stack for this project.

    9. Learning Resources
       Suggest official documentation and beginner-friendly
       learning resources.

    Important instructions:
    - Prefer Python-based technologies.
    - Consider the student's skill level.
    - Prefer free and open-source technologies.
    - Avoid unnecessary technologies.
    - Explain why each recommendation is suitable.
    - Do not recommend technologies that are unrelated
      to the project requirements.
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
    print("TECHNOLOGY RECOMMENDATION AGENT")
    project_title=input("Enter your project title: ")
    project_description=input("Describe your project briefly: ")
    skill_level=input("Enter skill level (Beginner/Intermediate/Advanced): ")
    model_type=input("Choose model (ollama/gemini): ").strip().lower()
    result=technolgy_recommendation_agent(
        project_title,
        project_description,
        model_type
    )
    print("\n TECHNOLOGY RECOMMENDATION AGENT\n")
    print(result)