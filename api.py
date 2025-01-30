import requests
import google.generativeai as genai
import elevenlabs
import os
import time
# Set an environment variable
os.environ["API_KEY"] ='API_KEY'
genai.configure(api_key=os.environ["API_KEY"])

#function for generating text response
def generate_text(userinput):
    model = genai.GenerativeModel ("gemini-1.5-flash")
    try:
        response = model.generate_content(userinput)
        return response.text
    except Exception as e:
     print(f"error occured in generating text : {e}")

#generating voice from text
def generate_voice(response):
   elevenlabs_api = "API_KEY"
   voice_id = "EXAVITQu4vr4xnSDxMaL"
   #voice_id = "bella"
   try:
      url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
      headers = {
        "xi-api-key": elevenlabs_api,
        "Content-Type": "application/json"
      }
      data = {
        "text": response,
        "voice_settings": {
            "stability": 0.75,
            "similarity_boost": 0.85
         }
      }
      r = requests.post(url, headers= headers, json = data)
      #count=0 #count of audio files
      if r.status_code==200:
          with open("audiofile.mp3", "wb") as f:
                f.write(r.content)
                print("Audio file generated successfully.")
                return "audiofile.mp3"
      else:
         print(f"error in api {r.status_code}")
   
   except Exception as e:
    print(f"error occured in generating audio : {e}")


def main():
   while True:
      userinput = input("enter your text (type 'exit' to end) :\n ")

      if userinput == "exit":
         break
      
      else:
        response = generate_text(userinput).strip("*")#generate response text method
        print("response :")
        print(response)#print response
        
        #generate_voice(response)#generate audio method
        audio=generate_voice(response)#generate audio method
        
        #time.sleep(5)
        #os.system(f"start {audio}")
       # time.sleep(2)
       # os.remove(f"{audio}")  # Remove the audio file after playing

        
      

if __name__ == "__main__":
   main()