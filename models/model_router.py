
def get_model(model_type="gemini"):
    if model_type == "ollama":
        from models.ollama_model import get_ollama_model
        return get_ollama_model()

    elif model_type == "gemini":
        from models.gemini_model import get_gemini_model
        return get_gemini_model()

    else:
        raise ValueError("Invalid model type")
