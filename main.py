import speech_recognition as sr
import os
import webbrowser
from openai import OpenAI
from config import apikey
import datetime
import random
import pyttsx3  # ✅ for Windows text-to-speech

# Initialize OpenAI client
client = OpenAI(api_key=apikey)
chatStr = ""


def say(text):
    """Use pyttsx3 for cross-platform speech (works on Windows)."""
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)  # 0 = male, 1 = female (optional)
    engine.say(text)
    engine.runAndWait()


def chat(query):
    """Chat with AI using new OpenAI v1 API."""
    global chatStr
    print(chatStr)
    chatStr += f"User: {query}\nJarvis: "

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are Jarvis, a helpful AI assistant."},
            {"role": "user", "content": chatStr}
        ],
        temperature=0.7,
        max_tokens=256
    )

    message = response.choices[0].message.content.strip()
    say(message)
    chatStr += f"{message}\n"
    return message


def ai(prompt):
    """Generate AI response and save to file."""
    text = f"OpenAI response for Prompt: {prompt}\n*************************\n\n"

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are Jarvis, a helpful AI assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=256
    )

    text += response.choices[0].message.content

    if not os.path.exists("Openai"):
        os.mkdir("Openai")
    filename = f"Openai/{random.randint(1, 9999999)}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)

    say("I have created your AI file successfully.")


def takeCommand():
    """Listen to user voice and return recognized text."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except Exception:
            say("Sorry, I did not catch that.")
            return "None"


if __name__ == '__main__':
    print("Welcome to Jarvis A.I")
    say("Welcome to Jarvis A.I")

    while True:
        query = takeCommand().lower()
        if query == "none":
            continue

        # Open websites
        sites = [
            ["youtube", "https://www.youtube.com"],
            ["wikipedia", "https://www.wikipedia.com"],
            ["google", "https://www.google.com"]
        ]
        for site in sites:
            if f"open {site[0]}" in query:
                say(f"Opening {site[0]}")
                webbrowser.open(site[1])
                break

        # Play music (update your own path)
        if "open music" in query:
            musicPath = r"C:\Users\aparn\Downloads\music.mp3"
            os.startfile(musicPath)

        # Tell time
        elif "the time" in query:
            hour = datetime.datetime.now().strftime("%H")
            minute = datetime.datetime.now().strftime("%M")
            say(f"Sir, the time is {hour} hours and {minute} minutes.")

        # AI prompt
        elif "using artificial intelligence" in query:
            ai(prompt=query)

        # Quit Jarvis
        elif "jarvis quit" in query:
            say("Goodbye, sir!")
            break

        # Reset chat
        elif "reset chat" in query:
            chatStr = ""
            say("Chat memory reset.")

        # Default chat
        else:
            print("Chatting...")
            chat(query)
