from AppOpener import close, open as appopen  # Import AppOpener libraries
from webbrowser import open as webopen  # Import webbrowser for opening URLs
from pywhatkit import search, playonyt  # Import functions from pywhatkit
from dotenv import dotenv_values  # Import dotenv to read .env files
from bs4 import BeautifulSoup  # Import BeautifulSoup for web scraping
from rich import print  # Import rich for styled console output
from groq import Groq  # Import Groq for AI chat functionality
import webbrowser  # Import webbrowser for opening URLs
import subprocess  # Import subprocess for interacting with system
import requests  # Import requests for making HTTP requests
import keyboard  # Import keyboard for keyboard-related functions
import asyncio  # Import asyncio for asynchronous programming
import os
import psutil
import platform
import math
import datetime
import requests, webbrowser
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart



env_vars = dotenv_values(".env")
GroqAPIKey = env_vars.get("GroqAPIKey")  # Retrieve the Groq API key.

# Define CSS classes for parsing specific elements in HTML content.
classes = ["Z0Zubf", "hgKElc", "LTKOO sY7ric", "Z0LcW", "gsrt vk_bk FzvWSb YwPhnf", "pclqee", "tw-Data-text tw-text-small tw-ta",
           "LxZ6rdc", "OSr6uG LTKOO", "LzYEg6d", "webanswers-webanswers_table__webanswers-table", "dDoNo ikb4Bb gsrt", "sXLa0e",
           "LWkFke", "VQF4g", "qv3Wpe", "kno-rdesc", "SPZz6b"]

# Define a user-agent for making web requests.
useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'

# Initialize the Groq client with the API key.
client = Groq(api_key=GroqAPIKey)

# Predefined professional responses for user interactions.
professional_responses = [
    "Your satisfaction is my top priority; feel free to reach out if there's anything else I can help you with.",
    "I'm at your service for any additional questions or support you may need–don't hesitate to ask.",
]

# List to store chatbot messages.
messages = []

# System message to provide context to the chatbot.
SystemChatBot = [{"role": "system", "content": f"Hello, I am {os.environ['Username']}, You're a content writer. You have to write content like letter, email, blog, etc. You have to write content in a professional way. If the user asks you to write content, then you have to write it in a professional way."}]

# Function to perform a Google search.
def GoogleSearch(Topic):
    search(Topic)  # Use pywhatkit's search function to perform a Google search.
    return True  # Indicate success.

# Function to generate content using AI and save it to a file.
def Content(Topic):

    # Nested function to open a file in Notepad.
    def OpenNotepad(File):
        default_text_editor = 'notepad.exe'  # Default text editor.
        subprocess.Popen([default_text_editor, File])  # Open the file in Notepad.
    def ContentWriterAI(prompt):
        messages.append({"role": "user", "content": f"{prompt}"})  # Add the user's prompt to messages.

        completion = client.chat.completions.create(
            model="llama3-70b-8192",  # Add a comma here
            messages=SystemChatBot + messages,  # Include system instructions and chat history.
            max_tokens=2048,  # Limit the maximum tokens in the response.
            temperature=0.7,  # Adjust response randomness.
            top_p=1,  # Use nucleus sampling for response diversity.
            stream=True,  # Enable streaming response.
            stop=None  # Allow the model to determine stopping condition.
        )
        Answer = ""
        for chunk in completion:
              if chunk.choices[0].delta.content:  # Check for content in the current chunk.
               Answer += chunk.choices[0].delta.content  # Append the content to the answer.

        Answer = Answer.replace("</s>", "")  # Remove unwanted tokens from the response.
        messages.append({"role": "assistant", "content": Answer})  # Add the AI's response to messages.
        return Answer

    Topic: str = Topic.replace("Content ", "")  # Remove "Content " from the topic
    ContentByAI = ContentWriterAI(Topic)  # Generate content using AI.

# Save the generated content to a text file.
    with open(rf"Data\{Topic.lower().replace(' ', '')}.txt", "w", encoding="utf-8") as file:
      file.write(ContentByAI)  # Write the content
      file.close()

    OpenNotepad(rf"Data\{Topic.lower().replace(' ', '')}.txt")  # Open the file in Notepad.
    return True  # Indicate success.

# Function to search for a topic on YouTube.
def YouTubeSearch(Topic):
    Url4Search = f"https://www.youtube.com/results?search_query={Topic}"  # Construct the YouTube search URL.
    webbrowser.open(Url4Search)  # Open the search URL in a web browser.
    return True  # Indicate success.

def note(text):
    date = datetime.datetime.now()
    file_name = str(date).replace(":", "-") + "-note.txt"
    with open(file_name, "w") as f:
        f.write(text)
    notepad = "C:/Windows/notepad.exe"
    subprocess.Popen([notepad, file_name])
    return True  # Indicate success.



def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])

def system_stats():
    # CPU Info
    cpu_usage = psutil.cpu_percent(interval=1)
    physical_cores = psutil.cpu_count(logical=False)
    total_cores = psutil.cpu_count(logical=True)
    cpu_freq = psutil.cpu_freq()
    cpu_name = platform.processor()

    # Memory Info
    virtual_mem = psutil.virtual_memory()
    memory_used = convert_size(virtual_mem.used)
    memory_total = convert_size(virtual_mem.total)

    # Disk Info (Assume main disk is C:)
    disk = psutil.disk_usage('/')
    disk_used = convert_size(disk.used)
    disk_total = convert_size(disk.total)

    # Battery Info
    battery = psutil.sensors_battery()
    battery_percent = battery.percent if battery else "No battery detected"

    # Compose result
    final_res = (
        f"CPU: {cpu_name}\n"
        f"Usage: {cpu_usage}%\n"
        f"Cores: {physical_cores} physical / {total_cores} logical\n"
        f"Frequency: {round(cpu_freq.current, 2)} MHz\n\n"
        f"RAM: {memory_used} used out of {memory_total}\n"
        f"Disk: {disk_used} used out of {disk_total}\n"
        f"Battery Level: {battery_percent}%"
    )
    return final_res


def send_mail(subject, body, receiver_email):
    sender_email = "soulai7771@gmail.com" 
    sender_password = "xaejuqjmsgqtfrwu" 

    if not sender_email or not sender_password:
        raise ValueError("Email credentials not set in .env")

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message.as_string())

    return True



# Function to play a video on YouTube.
def PlayYouTube(query):
    playonyt(query)  # Use pywhatkit's playonyt function to play the video.
    return True  # Indicate success.


       
        # Nested function to perform a Google search and retrieve HTML.
import os, subprocess, webbrowser, requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus

import os, subprocess, webbrowser, requests, platform
from bs4 import BeautifulSoup
from urllib.parse import quote_plus

import os
import platform
import subprocess
import webbrowser
from urllib.parse import quote_plus

def OpenApp(app_name):
    """
    Attempts to open a desktop app. If not available, searches Google for a download link and opens it.
    Handles Windows, macOS, and Linux systems.
    """
    # Normalize app name for case-insensitive matching
    app_name_lower = app_name.lower()
    
    # Platform-specific handling
    current_os = platform.system()
    is_windows = (current_os == 'Windows')
    is_macos = (current_os == 'Darwin')
    is_linux = (current_os == 'Linux')

    # Special app handling with URI schemes
    special_apps = {
        "microsoft store": "ms-windows-store:",
        "settings": "ms-settings:" if is_windows else "gnome-control-center" if is_linux else "x-apple.systempreferences:",
    }

    # Try to open the app
    try:
        # Handle special apps first
        if app_name_lower in special_apps:
            handler = special_apps[app_name_lower]
            if is_windows:
                os.system(f'start {handler}')
            elif is_macos:
                subprocess.Popen(['open', handler])
            elif is_linux:
                subprocess.Popen([handler])
            print(f"✅ Opened: {app_name}")
            return True
        
        # Handle regular applications
        if is_windows:
            os.startfile(app_name)  # Works for executables in PATH
        elif is_macos:
            # macOS applications (.app bundles)
            subprocess.Popen(['open', '-a', app_name])
        else:  # Linux
            # Try both desktop entries and direct execution
            subprocess.Popen([app_name])
        print(f"✅ Opened: {app_name}")
        return True

    except Exception as e:
        print(f"❌ Failed to open '{app_name}': {e}")
        return search_download_link(app_name)


def search_download_link(app_name):
    """Fallback to Google search for download links"""
    try:
        query = quote_plus(f"{app_name} official download site")
        url = f"https://www.google.com/search?q={query}"
        
        # Try to open directly in browser (more reliable than parsing)
        print(f"🔍 Searching for download: {app_name}")
        webbrowser.open(url)
        return url
        
    except Exception as ex:
        print(f"❌ Fallback search failed: {ex}")
        return False

        
# Function to close an application.
def CloseApp(app):    
    if 'chrome' in app:
        pass
    else:
        try:
            close(app, match_closest=True, output=True, throw_error=True)  # Attempt to close the app.
            return True  # Indicate success.
        except:
            print(f"Failed to close {app}.")  # Print an error message if closing fails.
            return False  # Indicate failure.
        
def SystemCommand(command):

    def mute():
        keyboard.press_and_release("volume mute")  # Mute the system volume using keyboard shortcut.
        return True  # Indicate success.
    def unmute():
        keyboard.press_and_release("volume unmute")  # Unmute the system volume using keyboard shortcut.
        return True  # Indicate success.    
    def volume_up():
        keyboard.press_and_release("volume up") # Increase the system volume using keyboard shortcut.               
        return True  # Indicate success.
    def volume_down():
        keyboard.press_and_release("volume down")               
        return True 
    # Decrease the system volume using keyboard shortcut.

   
    if command.lower() == "mute":
        return mute()   
    elif command.lower() == "unmute":   
        return unmute()
    elif command.lower() == "volume up":    
        return volume_up()
    elif command.lower() == "volume down":
        return volume_down()
    else:   
        print(f"Unknown command: {command}")
        return False  # Indicate failure for unknown commands.  
    
async def TranslateandExecute(commmands: list[str]):
    func =[]
    for command in commmands:
       if command.startswith("open "):
           if "open it " in command:
               pass
           if "open file" == command:
               pass
           else:
                fun=asyncio.to_thread(OpenApp, command.removeprefix("open "))
                func.append(fun)
       elif command.startswith("general "):
           pass
       elif command.startswith("realtime "):
           pass
       elif command.startswith("close "):
           fun=asyncio.to_thread(CloseApp, command.removeprefix("close "))
           func.append(fun)
       elif command.startswith("system stats"):
           fun=asyncio.to_thread(system_stats)
           func.append(fun)    
       elif command.startswith("search "):
           fun=asyncio.to_thread(GoogleSearch, command.removeprefix("search "))
           func.append(fun)
       elif command.startswith("content "): 
           fun=asyncio.to_thread(Content, command.removeprefix("content "))
           func.append(fun) 
       elif command.startswith("youtube search "): 
           fun=asyncio.to_thread(YouTubeSearch, command.removeprefix("youtube "))
           func.append(fun)
       elif command.startswith("play "):    
           fun=asyncio.to_thread(PlayYouTube, command.removeprefix("play "))
           func.append(fun)
       elif command.startswith("system "):
           fun=asyncio.to_thread(SystemCommand, command.removeprefix("system "))
           func.append(fun) 
       elif command.startswith("note "):
           fun=asyncio.to_thread(note, command.removeprefix("note "))
           func.append(fun)    
       elif command.startswith("google search "):
           fun=asyncio.to_thread(GoogleSearch, command.removeprefix("google search "))
           func.append(fun)   
       else:
              print(f"Unknown command: {command}")
    results = await asyncio.gather(*func)  # Execute all functions concurrently.
    for result in results:
        if isinstance(result, str):
            yield result  # If the result is a string, yield it.
        else:
            yield result       


async def Automation(commands: list[str]):
    async for result in TranslateandExecute(commands):  # 
        pass

    return True  # Indicate success.

#Content("write a application for vijaya for not attending francis desil class on wednesday ") #example usage of Content function
#GoogleSearch("Ajay Sai Singh")  # Example usage of GoogleSearch function
#PlayYouTube("Tu jane na")  # Example usage of PlayYouTube function
#OpenApp("excel","notepad","microsoft store","whatsapp")  # Example usage of OpenApp function
#GoogleSearch("Ajay Sai Singh :)")  # Example usage of GoogleSearch function
#CloseApp("word")  # Example usage of CloseApp function     
#if __name__ == "__main__":
#    asyncio.run(Automation(["open facebook", "open instagram", "open telegram", "play afsanay", "content song for me"]))
#note("Rohan this is note function")  # Example usage of note function
#print(system_stats())  # Example usage of system_stats function
# send_mail(
#      subject="Test Email",
#      body="This is a test email sent from the automation script.",
#      receiver_email="rohanprabhakar98@gmail.com")
