from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
load_dotenv()

def get_gemini_model():
    model=ChatGoogleGenerativeAI(
        model="gemini-3.8-flash",
        google_api_key=os.getenv("GEMINI_API_KEY"),
        temperature=0.7
    )
    return model
if __name__=="__main__":
    print("Testing Gemini connection...")

    llm=get_gemini_model()

    print("Sending request to Gemini...")

    response=llm.invoke("SUggest three innovative final year AI projects.")

    print("Gemini response received!")
    print(response.content)