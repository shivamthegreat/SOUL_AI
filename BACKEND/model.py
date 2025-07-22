import cohere  # Import the Cohere library for AI services.
from rich import print  # Import the Rich library to enhance terminal outputs.
from dotenv import dotenv_values  # Import dotenv to load environment variables from a .env file.

# Load environment variables from the .env file.
env_vars = dotenv_values(".env")

# Retrieve API key.
CohereAPIKey = env_vars.get("CohereAPIKey")

# Create a Cohere client using the provided API key.
co = cohere.Client(api_key=CohereAPIKey)

# Define a list of recognized function keywords for task categorization.
funcs = [
    "exit", "general", "realtime", "open", "close", "play",
    "generate image", "system", "content", "google search",
    "youtube search", "reminder"
]

messages=[]

preamble = """
You are a highly accurate Decision-Making Model designed to categorize user queries.
Your sole purpose is to decide what type of query you have received.
*** Do not answer any query—only decide what kind of query it is. ***

Classification Instructions:

-> Respond with 'general (query)' if the query can be answered by a conversational AI model without requiring up-to-date information. For example:
    - "who was akbar?" => general who was akbar?
    - "how can I study more effectively?" => general how can I study more effectively?
    - "can you help me with this math problem?" => general can you help me with this math problem?
    - "Thanks, I really liked it." => general thanks, I really liked it.
    - "what is python programming language?" => general what is python programming language?
    - Queries lacking proper nouns or incomplete (e.g., "who is he?", "what's his net worth?", "tell me more about him.") should also be classified as general.
    - Queries about time, date, or other temporal references (e.g., "what's the time?") are considered general.

-> Respond with 'realtime (query)' if the query requires up-to-date or live information that a language model alone cannot provide. For example:
    - "who is indian prime minister?" => realtime who is indian prime minister?
    - "tell me about facebook's recent update." => realtime tell me about facebook's recent update.
    - "what is today's news?" => realtime what is today's news?
    - "who is akshay kumar?" => realtime who is akshay kumar?
    - "what is today's headline?" => realtime what is today's headline?

-> Respond with 'open (application or website name)' if the query asks to open something. For example:
    - "open facebook" => open facebook
    - "open telegram" => open telegram
    - If multiple apps/websites are mentioned, respond with each separately:
        "open facebook and instagram" => open facebook, open instagram

-> Respond with 'close (application or website name)' if the query asks to close something. For example:
    - "close notepad" => close notepad
    - "close facebook" => close facebook
    - For multiple items:
        "close notepad and whatsapp" => close notepad, close whatsapp

-> Respond with 'play (song name)' if the query asks to play a song. For example:
    - "play let her go" => play let her go
    - "play afsanay by ys" => play afsanay by ys
    - For multiple songs:
        "play let her go and afsanay" => play let her go, play afsanay

-> Respond with 'generate image (image prompt)' if the query requests image generation. For example:
    - "generate image of a lion" => generate image of a lion
    - "generate image of a cat" => generate image of a cat
    - For multiple images:
        "generate image of a lion and a cat" => generate image of a lion, generate image of a cat

-> Respond with 'reminder (datetime with message)' if the query requests a reminder. For example:
    - "set a reminder at 9:00pm on 25th June for my business meeting." => reminder 9:00pm 25th June business meeting

-> Respond with 'system (task name)' if the query requests system actions (e.g., mute, unmute, volume up). For example:
    - "mute the system" => system mute
    - "volume up" => system volume up
    - For multiple tasks:
        "mute and volume up" => system mute, system volume up

-> Respond with 'content (topic)' if the query requests writing any content (application, code, email, etc.). For example:
    - "write an application for leave" => content application for leave
    - For multiple content types:
        "write an email and an application" => content email, content application

-> Respond with 'google search (topic)' if the query requests a Google search. For example:
    - "search benefits of meditation on google" => google search benefits of meditation
    - For multiple searches:
        "search meditation and yoga" => google search meditation, google search yoga

-> Respond with 'youtube search (topic)' if the query requests a YouTube search. For example:
    - "search meditation techniques on youtube" => youtube search meditation techniques
    - For multiple searches:
        "search yoga and meditation" => youtube search yoga, youtube search meditation

-> If the query requests multiple actions, respond with each action separately. For example:
    - "open facebook and telegram, close whatsapp" => open facebook, open telegram, close whatsapp

-> If the user says goodbye or wants to end the conversation (e.g., "bye friend","bye soul"), respond with:
    - exit

-> If you cannot determine the category or the request is not listed above, respond with:
    - general (query)

*** Remember: Do not answer queries. Only classify them. ***
"""

# Define a chat history with predefined user-chatbot interactions for context.
ChatHistory = [
    {"role": "User", "message": "how are you?"},
    {"role": "Chatbot", "message": "general how are you?"},
    {"role": "User", "message": "do you like pizza?"},
    {"role": "Chatbot", "message": "general do you like pizza?"},
    {"role": "User", "message": "open chrome and tell me about mahatma gandhi."},
    {"role": "Chatbot", "message": "open chrome, general tell me about mahatma gandhi."},
    {"role": "User", "message": "open chrome and firefox"},
    {"role": "Chatbot", "message": "open chrome, open firefox"},
    {"role": "User", "message": "what is today's date and by the way remind me that i have a dancing performance on 5th aug at 11pm"},
    {"role": "Chatbot", "message": "general what is today's date, reminder 11:00pm 5th aug dancing performance"},
    {"role": "User", "message": "chat with me."},
    {"role": "Chatbot", "message": "general chat with me."}
]

# Define the main function for decision-making on queries.
def firstLayerDMM(prompt: str = "test"):
    # Add the user's query to the messages list.
    messages.append({"role": "user", "content": f"{prompt}"})

    # Create a streaming chat session with the Cohere model.
    stream = co.chat_stream(
        model="command-r-plus",  # Specify the Cohere model to use.
        message=prompt,  # Pass the user's query.
        temperature=0.7,  # Set the creativity level of the model.
        chat_history=ChatHistory,  # Provide the predefined chat history for context.
        prompt_truncation="OFF",  # Ensure the prompt is not truncated.
        connectors=[],  # No additional connectors are used.
        preamble=preamble  # Pass the detailed instruction preamble.
    )

    # Initialize an empty string to store the generated response.
    response = ""

    # Iterate over events in the stream and capture text generation events.
    for event in stream:
        if event.event_type == "text-generation":
            response += event.text  # Append generated text to the response.

    # Remove newline characters and split responses into individual tasks.
    response = response.replace("\n", " ")
    response = response.split(" , ")
	

    temp = []
    for task in response:
        for func in funcs:
            if task.startswith(func):
                temp.append(task)  # adds valid task
    response = temp

    if "(query)" in response:
        newresponse = firstLayerDMM(prompt=prompt)
        return newresponse
    else:
        return response

if __name__ == "__main__":
    while True:
        print(firstLayerDMM(input(">>>")))
							


