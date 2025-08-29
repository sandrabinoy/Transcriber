import speech_recognition as sr
import socket

from online_googleAudio import onlineTrancribe
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

# Continuously listen for speech and transcribe it until user says "exit"
if is_connected():
    onlineTrancribe(sr, recognizer)
else:
    offlineTranscribe(sr, recognizer)