import os
import requests
import google.generativeai as genai

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API keys from .env
GEMINI_API_KEY = os.getenv("GEMINI_API")
ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API')

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# Function to generate text response
def generate_text(userinput):
    model = genai.GenerativeModel("gemini-1.5-flash")
    try:
        response = model.generate_content(userinput)
        return response.text
    except Exception as e:
        print(f"Error occurred in generating text: {e}")
        return None

# Function to generate voice from text
def generate_voice(response):
    voice_id = "EXAVITQu4vr4xnSDxMaL"

    try:
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        headers = {
            "xi-api-key": ELEVENLABS_API_KEY,
            "Content-Type": "application/json"
        }
        data = {
            "text": response,
            "voice_settings": {
                "stability": 0.75,
                "similarity_boost": 0.85
            }
        }

        r = requests.post(url, headers=headers, json=data)

        if r.status_code == 200:
            audio_file = "audiofile.mp3"
            with open(audio_file, "wb") as f:
                f.write(r.content)
            print("Audio file generated successfully.")
            return audio_file
        else:
            print(f"Error in API call: {r.status_code}")
            return None

    except Exception as e:
        print(f"Error occurred in generating audio: {e}")
        return None

# Main function
def main():
    while True:
        userinput = input("Enter your text (type 'exit' to end):\n")
        

        if userinput.lower() == "exit":
            break

        response = generate_text(userinput)
        
        if response:
            print("\nResponse:")
            print(response)
            
            # Clean up response text (remove special formatting like asterisks)
            response_cleaned = response.replace("*", "")

            print(response_cleaned)

            # Generate voice from the cleaned response
            generate_voice(response_cleaned)

           

if __name__ == "__main__":
    main()
