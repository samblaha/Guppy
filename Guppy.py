import speech_recognition as sr
import openai
import gtts
import os
from playsound import playsound





client = openai.OpenAI()  # Create the OpenAI API client


def listen_for_wake_word():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        print("Listening for 'Guppy'...")
        while True:
            audio = r.listen(source)
            try:
                text = r.recognize_google(audio).lower()
                if "guppy" in text:
                    print("Wake word detected.")
                    return True
            except sr.UnknownValueError:
                pass

def listen_for_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for command...")
        audio = r.listen(source)
        try:
            command_text = r.recognize_google(audio).lower()
            print(f"Command received: {command_text}")
            return command_text
        except sr.UnknownValueError:
            print("Could not understand the command.")
            return None


def get_response(command):
    try:
        messages = []
        user_message = {

            
            "role": "system",
            "content": "You are a helpful assistant, that is very sassy."
            ,
            "role": "user",
            "content": command,
        }
        messages.append(user_message)

        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=150,
            temperature=0.7,
            # Optional: You can keep the other parameters (top_p, frequency_penalty, presence_penalty)
            stop=["\n"]  # Adjust as necessary
        )

        # Try accessing content attribute (recommended approach)
       

        response_text = completion.choices[0].message.content
        return response_text

    except Exception as e:
        print(f"An error occurred: {e}")
        return "Sorry, I couldn't process that request."




def speak(text):
    tts = gtts.gTTS(text, lang='en')
    tts.save('response.mp3')
    playsound('response.mp3')
    os.remove('response.mp3')

def main():
    while True:
        if listen_for_wake_word():
            command = listen_for_command()
            if command:
                response = get_response(command)
                speak(response)

if __name__ == "__main__":
    main()
