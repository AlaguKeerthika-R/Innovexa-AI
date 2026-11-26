from models.model_router import get_model

def architecture_agent(project_title,project_description,model_type="gemini"):
    llm=get_model(model_type)
    prompt=f"""
    You are a senior software architect and technical project mentor.

    Design a complete software architecture for the following project.

    Project Title: {project_title}
    Project Description: {project_description}

    Prepare the architecture with these sections:

    1. System Overview
       Explain how the complete application works.

    2. Architecture Components
       Identify the frontend, backend, database, AI models,
       APIs, and other important components.
       Prefer Python-compatible technologies.

    3. Component Responsibilities
       Explain the responsibility of each component.

    4. System Workflow
       Describe the complete process step by step,
       from user input to final output.

    5. Database Design
       Suggest suitable tables, their fields, and relationships.
       Explain why each table is needed.

    6. AI Integration
       Explain how the AI models and agents interact
       with the application.

    7. Architecture Diagram
       Provide a clear text-based architecture diagram
       using arrows to show communication between components.

    8. Security Considerations
       Suggest authentication, authorization, input validation,
       and protection of sensitive information.

    Keep the design practical and achievable for a final-year
    computer science project.

    Use Python-based technologies wherever possible.
    Avoid unnecessary complexity.
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
    print("ARCHITECTURE DESIGN AGENT")
    project_title=input("Enter your project title: ")
    project_description=input("Describe your project briefly: ")
    model_type=input("Choose model (Ollama/gemini): ").strip().lower()
    result=architecture_agent(
        project_title,
        project_description,
        model_type
    )
    print("\n SYSTEM ARCHITECTURE \n")
    print(result)