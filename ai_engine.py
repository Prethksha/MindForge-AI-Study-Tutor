import time
import streamlit as st
from google.genai import Client
from dotenv import load_dotenv

import os
load_dotenv()
client = Client(api_key=os.getenv("GEMINI_API_KEY")) 

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