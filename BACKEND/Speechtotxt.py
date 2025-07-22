from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
#from webdriver_manager.chrome import ChromeDriverManager
from dotenv import dotenv_values
import os
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' 
import mtranslate as mt

env_vars = dotenv_values(".env")
InputLanguage = env_vars.get("InputLanguage")

chromedriver_path = r"C:\WebDriver\bin\chromedriver.exe"
chrome_binary_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

HtmlCode = '''<!DOCTYPE html>
<html lang="en">
<head>
    <title>Speech Recognition</title>
</head>
<body>
    <button id="start" onclick="startRecognition()">Start Recognition</button>
    <button id="end" onclick="stopRecognition()">Stop Recognition</button>
    <p id="output"></p>
    <script>
        const output = document.getElementById('output');
        let recognition;

        function startRecognition() {
            recognition = new webkitSpeechRecognition() || new SpeechRecognition();
            recognition.lang = '';
            recognition.continuous = true;

            recognition.onresult = function(event) {
                const transcript = event.results[event.results.length - 1][0].transcript;
                output.textContent += transcript;
            };

            recognition.onend = function() {
                recognition.start();
            };
            recognition.start();
        }

        function stopRecognition() {
            recognition.stop();
            output.innerHTML = "";
        }
    </script>
</body>
</html>'''

HtmlCode = str(HtmlCode).replace("recognition.lang = '';", f"recognition.lang = '{InputLanguage}';")
os.makedirs("Data", exist_ok=True)
with open(r"DataVoice.html", "w") as f:
    f.write(HtmlCode)

current_dir = os.getcwd()
link = f"{current_dir}/Data/DataVoice.html"

# add queue options for the monotone
chrome_options = Options()
chrome_options.binary_location = chrome_binary_path
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
chrome_options.add_argument(f"user-agent={user_agent}")
chrome_options.add_argument("--use-fake-ui-for-media-stream")
chrome_options.add_argument("--use-fake-device-for-media-stream")
chrome_options.add_argument("--headless=new")

# Use the specified chromedriver path instead of ChromeDriverManager
service = Service(executable_path=chromedriver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.get("https://www.google.com")


TempDirPath = rf"{current_dir}/Frontend/Files"
os.makedirs(TempDirPath, exist_ok=True)
# function to get the session's status by writing it to a file
def SetAssistantStatus(Status):


    file_path = os.path.join(TempDirPath, "Frontend", "Files", "Status.data")
    with open(file_path, "w", encoding="utf-8") as file:
    #     ...

    # with open(f'{TempDirPath}/Status.data', "w", encoding='utf-8') as file:
        file.write(Status)

# function to modify a query to ensure proper punctuation and formatting
def QueryModifier(Query):
    new_query = Query.lower().strip()
    query_words = new_query.split()
    question_words = ['how','is', 'what', 'who', 'where', 'when', 'why', 'which', 'whose', 'whom', 'can you', "what's", "where's", "how's", 'can you']

    # check if the query is uncertain and add a question mark if necessary
    if any(word in new_query for word in question_words):
        if query_words[-1][-1] not in ['.', '?', '!']:
            new_query = new_query[:-1] + '?'
    else:
        new_query+= '.'

    return new_query.capitalize()
# function to translate a query to English
def UniversalTranslator(Query):
    english_translation = mt.translate(Query, 'en', 'auto')
    return english_translation  

def SpeechRecognition():
    # Open the HTML file in the browser
    driver.get("file:///" + link)
    # Start speech recognition by clicking the start button
    driver.find_element(by=By.ID, value="start").click()

    while True:
        try:
            # Get the recognized text from the HTML output element
            Text = driver.find_element(by=By.ID, value="output").text

            if Text:
                # Stop recognition by clicking the stop button
                driver.find_element(by=By.ID, value="end").click()

                # If the input language is English, return the modified query
                if InputLanguage.lower() == "en" or "en" in InputLanguage.lower():
                    return QueryModifier(Text)
                else:
                    # If the input language is not English, translate the text and return it
                    SetAssistantStatus("Translating...")
                    return QueryModifier(UniversalTranslator(Text))

        except Exception as e:
            pass

# # # Main execution block
if __name__ == "__main__":
     while True:
      Text = SpeechRecognition()
      print(Text)    