import pygame
import random
import asyncio
import os
import requests
from dotenv import dotenv_values

env_vars = dotenv_values(".env")
# You can also put voice_id in .env if you want
api_key = env_vars.get("ELEVENLABS_API_KEY")
voice_id = "yjJ45q8TVCrtMhEKurxY"

async def TextToAudioFile(text) -> None:
    file_path = r"Data/speech.mp3"
    if os.path.exists(file_path):
        os.remove(file_path)

    payload = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }

    response = requests.post(
        f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
        headers={
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": api_key
        },
        json=payload
    )

    if response.status_code == 200:
        with open(file_path, "wb") as f:
            f.write(response.content)
    else:
        raise Exception(f"ElevenLabs error {response.status_code}: {response.text}")

def TTS(Text, func=lambda r: True):
    while True:
        try:
            asyncio.run(TextToAudioFile(Text))
            pygame.mixer.init()
            pygame.mixer.music.load(r"Data/speech.mp3")
            pygame.mixer.music.play()

# Loop while audio is playing
            while pygame.mixer.music.get_busy():
              if func(True) == False:
                 break
            pygame.time.Clock().tick(10)

            return True

        finally:
            try:
                func(False)
                pygame.mixer.music.stop()
                pygame.mixer.quit()
            except Exception as e:
                print(f"Error in finally block: {e}")

def TextToSpeech(Text, func=lambda r: True):
    Data = str(Text).split(".")
    responses = [
        "The rest of the result has been printed to the chat screen, kindly check it out sir.",
        "The rest of the text is now on the chat screen, sir, please check it.",
        "You can see the rest of the text on the chat screen, sir.",
        "The remaining part of the text is now on the chat screen, sir.",
        "Sir, you'll find more text on the chat screen for you to see.",
        "The rest of the answer is now on the chat screen, sir.",
        "Sir, please look at the chat screen, the rest of the answer is there.",
        "You'll find the complete answer on the chat screen, sir.",
        "The next part of the text is on the chat screen, sir.",
        "Sir, please check the chat screen for more information.",
        "There's more text on the chat screen for you, sir.",
        "Sir, take a look at the chat screen for additional text.",
        "You'll find more to read on the chat screen, sir.",
        "Sir, check the chat screen for the rest of the text.",
        "The chat screen has the rest of the text, sir.",
        "There's more to see on the chat screen, sir, please look.",
        "Sir, the chat screen holds the continuation of the text.",
        "You'll find the complete answer on the chat screen, kindly check it out sir.",
        "Please review the chat screen for the rest of the text, sir.",
        "Sir, look at the chat screen for the complete answer."
    ]

    if len(Data) > 4 and len(Text) >= 250:
        snippet = ". ".join(Data[0:2]) + ". " + random.choice(responses)
        TTS(snippet, func)
    else:
        TTS(Text, func)

if __name__ == "__main__":
    try:
        text = input("Enter the text you want me to speak: ")
        TextToSpeech(
            text,
            lambda r: True
        )
    except Exception as e:
        print(f"An error occurred: {e}")
