import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("GOOGLE_API_KEY environment variable:", os.getenv('GOOGLE_API_KEY'))

try:
    import google.generativeai as genai
    api_key = os.getenv('GOOGLE_API_KEY')
    if api_key:
        genai.configure(api_key=api_key)
        print("Gemini API configured successfully")

        # List available models
        models = genai.list_models()
        print("Available models:")
        for model in models:
            print(f"  - {model.name}")
    else:
        print("No GOOGLE_API_KEY found in environment")
except ImportError:
    print("google-generativeai not installed")
except Exception as e:
    print(f"Error configuring Gemini: {e}")
