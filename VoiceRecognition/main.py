import speech_recognition as sr
import socket

from online_googleAudio import onlineTranscribe
from offline_whisper import offlineTranscribe

def is_connected():
    try:
        # Tries to connect to Google's DNS server
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except socket.error:
        return False

# Create a Recognizer instance and use the microphone as the audio source
recognizer = sr.Recognizer()
text = ""

try:
     with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.2)
except OSError as e:
    print(f"Microphone is not available or accessible: {e}")

# Continuously listen for speech and transcribe it until user says "exit"
while True:
    if is_connected():
        print("Internet connection detected. Using online transcription.")
        text = onlineTranscribe(sr, recognizer)
        if text and text == "exit":
            break
    else:
        print("No internet connection. Using offline transcription.")
        text = offlineTranscribe(sr, recognizer)
        if text and text == "exit":
            break
