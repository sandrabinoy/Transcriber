def onlineTrancribe(sr, recognizer): 
    while True:
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source, duration=0.2)
        
            try:
                audio = recognizer.listen(source)

                print("Transcribing with Google Audio...")
                text = recognizer.recognize_google(audio)
                text = text.lower()

                if text == "exit":
                    print(f"You said: {text}. Exiting")
                    break
                else:
                    print(f"You said: {text}")

            except sr.WaitTimeoutError:
                print("No speech detected within the timeout period.")
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio.")
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")