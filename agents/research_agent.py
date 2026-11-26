from models.model_router import get_model
def research_agent(project_title,project_description,model_type="gemini"):
    llm=get_model(model_type)
    prompt = f"""
    You are an experienced academic research analyst.

    Analyze the following final-year computer science project.

    Project Title: {project_title}
    Project Description: {project_description}

    Prepare a research analysis with these sections:

    1. Problem Identification
       Explain the real-world problem this project addresses.

    2. Existing System
       Explain how this problem is currently handled.

    3. Limitations of Existing System
       Identify the disadvantages of existing approaches.

    4. Research Objectives
       List five clear objectives for this project.

    5. Research Gap
       Identify potential gaps that this project could address.
       Clearly distinguish possible research gaps from gaps
       verified through published research.

    6. Proposed Innovation
       Suggest improvements that can make this project different
       from existing solutions.

    7. Expected Research Contribution
       Explain what this project can contribute.

    Keep the analysis academic, practical, beginner-friendly,
    and suitable for a final-year computer science project.

    Do not invent research papers, authors, citations, or statistics.
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
    print("RESEARCH ANALYSIS AGENT")
    project_title=input("Enter your project title: ")
    project_description=input("Describe your project briefly: ")
    model_type=input("Choose model (ollama/gemini): ").strip().lower()
    result=research_agent(
        project_title,
        project_description,
        model_type
    )
    print("\n RESEARCH ANALYSIS \n")
    print(result)