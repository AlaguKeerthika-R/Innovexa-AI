from models.model_router import get_model

def coding_agent(
        project_title,
        project_description,
        programming_language,
        module_name,
        module_requirements,
        skill_level,
        model_type="gemini"
):
    llm=get_model(model_type)
    prompt=f"""
     You are an expert software developer and programming mentor.

    Generate working source code for one module of the following project.

    Project Title: {project_title}
    Project Description: {project_description}
    Programming Language: {programming_language}
    Module Name: {module_name}
    Module Requirements: {module_requirements}
    Student Skill Level: {skill_level}

    Follow these instructions:

    1. Generate code strictly in {programming_language}.
    2. Implement only the requested module, not the entire project.
    3. Make the code practical, readable, and executable.
    4. Use technologies and libraries suitable for the selected language.
    5. Include necessary imports and dependencies.
    6. Handle common errors and invalid inputs.
    7. Do not use Python unless Python is the selected language.
    8. Avoid unnecessary complexity.

    Structure your response using these sections:

    1. Module Overview
       Explain what this module does.

    2. Required Dependencies
       List the libraries, packages, or tools required.

    3. Source Code
       Provide the complete code in a code block.
       Mention the appropriate filename.

    4. Code Explanation
       Explain the important parts of the code in beginner-friendly language.

    5. Execution Instructions
       Explain how to compile or run the code.

    6. Expected Output
       Show a sample output.

    7. Testing
       Provide at least three test cases.

    Important:
    - Ensure the generated source code matches the selected language.
    - Do not mix programming languages.
    - Do not provide pseudocode instead of actual implementation.
    - If additional project files are necessary, identify them clearly.
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
    print("CODING AGENT")
    project_title=input("Enter your project title: ")
    project_description=input("Describe your project briefly: ")
    programming_languages=input("Enter programming languages: ")
    module_name=input("Enter the module name: ")
    module_requirements=input("Describe what this module should do: ")
    skill_level=input("Enter skill level (Beginner/Intermediate/Advanced): ")
    model_type=input("Choose model (ollama/gemini): ").strip().lower()
    result=coding_agent(
        project_title,
        project_description,
        programming_languages,
        module_name,
        module_requirements,
        skill_level,
        model_type
    )
    print("\n GENERATED CODE AND EXPLANATION \n")
    print(result)