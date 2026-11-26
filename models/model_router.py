from models.ollama_model import get_ollama_model
from models.gemini_model import get_gemini_model

def get_model(model_type="ollama"):
    if model_type=="ollama":
        return get_ollama_model()
    elif model_type=="gemini":
        return get_gemini_model()
    else:
        raise ValueError("Invalid model type")
if __name__=="__main__":
    llm=get_model("ollama")
    response=llm.invoke("What is Artificial Intelligence?")
    print(response.content)