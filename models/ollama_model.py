from langchain_ollama import ChatOllama

def get_ollama_model():
    model=ChatOllama(
        model="qwen2.5:1.5b",
        temperature=0.7
    )
    return model 
if __name__=="__main__":
    llm=get_ollama_model()
    response=llm.invoke("Suggest three final year computer science projects.")
    print(response.content)