import whisper
import numpy as np
import io

# Global variable to store the loaded model to avoid reloading on each call
_offline_model = None

def _load_whisper_model():
    global _offline_model
    if _offline_model is None:
        print("Loading offline Whisper model...")
        try:
            _offline_model = whisper.load_model("base")
            print("Whisper model loaded successfully.")
        except Exception as e:
            print(f"Failed to load Whisper model: {e}")
            _offline_model = False
    return _offline_model

def offlineTranscribe(sr, recognizer):
    offline_model = _load_whisper_model()
    if not offline_model:
        print("Offline model is not available.")
        return ""
    
    try:
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source, duration=0.2)
            audio = recognizer.listen(source)

        print("Transcribing with Whisper...")
        # Convert the audio data to a NumPy array for Whisper
        audio_buffer = io.BytesIO(audio.get_wav_data())
        audio_np = np.frombuffer(audio_buffer.read(), dtype=np.int16).flatten().astype(np.float32) / 32768.0
        
        # Transcribe the audio using the local Whisper model
        result = offline_model.transcribe(audio_np, fp16=False)
        text = result['text'].strip().lower()
        
        if text == "exit":
            print(f"You said: {text}. Exiting")
            return text
        else:
            print(f"You said: {text}")
            return text

    except sr.WaitTimeoutError:
        print("No speech detected within the timeout period.")
    except sr.UnknownValueError:
        print("Whisper could not understand audio.")
    except sr.RequestError as e:
        print(f"Could not request results from Whisper service; {e}")
    except OSError as e:
        print(f"Microphone is not available or accessible: {e}")
    except Exception as e:
        print(f"An error occurred during offline transcription: {e}")
