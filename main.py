import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")


if len(sys.argv) < 2:
    raise ValueError("Missing prompt. Usage: python script.py '<your prompt here>'")

if "--help" in sys.argv:
    print("Usage: python main.py '<your prompt>' [--verbose]")
    sys.exit(0)

user_prompt = sys.argv[1]

messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

client = genai.Client(api_key=api_key)
try:
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages
    )
    response_text = response.text
except Exception as e:
    print(f"Error from Gemini API: {e}")
    sys.exit(1)

response_text = response.text
prompt_tokens = response.usage_metadata.prompt_token_count
response_tokens = response.usage_metadata.candidates_token_count

if "--verbose" in sys.argv:
    print(f"""
    ============================================================================
    
    User prompt: {user_prompt}
    Prompt tokens: {prompt_tokens}
    Response tokens: {response_tokens}
    Response: {response_text}
    
    ============================================================================
""")
else:
    print(f"""
   {response_text}
    """)

