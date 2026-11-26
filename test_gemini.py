
from dotenv import load_dotenv
from google import genai
from google.genai import types
import os

load_dotenv()

print("Connecting to Gemini...")

try:
    client = genai.Client(
        api_key=os.getenv("GEMINI_API_KEY"),
        http_options=types.HttpOptions(timeout=60000)
    )

    print("Sending request...")

    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents="Reply with only the word Hello."
    )

    print("Response received!")
    print(response.text)

except Exception as e:
    print("Error:", type(e).__name__)
    print(e)
