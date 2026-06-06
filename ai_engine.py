import time
from google.genai import Client

client = Client(api_key="YOUR_API_KEY")  # put your key here temporarily

def generate_notes(prompt):
    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            return response.text

        except Exception as e:
            print("FULL ERROR:", repr(e))
            if attempt == 2:
                return f"Error: {repr(e)}"
            time.sleep(2)