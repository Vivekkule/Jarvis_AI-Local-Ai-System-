import pyttsx3
import speech_recognition as sr

# Text-to-speech setup
tts_engine = pyttsx3.init()
tts_engine.setProperty("rate", 170)    # speaking speed
tts_engine.setProperty("volume", 0.9)

# Try to set a better voice
voices = tts_engine.getProperty("voices")
for voice in voices:
    if "zira" in voice.name.lower() or "david" in voice.name.lower():
        tts_engine.setProperty("voice", voice.id)
        break

def speak(text: str):
    print(f"Jarvis: {text}")
    # Clean text for speech (remove code blocks etc)
    clean = text.replace("[TOOL:", "").replace("]", "")
    if len(clean) > 500:
        clean = clean[:500] + "... response truncated for speech."
    tts_engine.say(clean)
    tts_engine.runAndWait()

def listen(timeout: int = 8) -> str:
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening... (speak now)")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=15)
        except sr.WaitTimeoutError:
            return ""
    try:
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        print("Speech service unavailable, using text input")
        return input("You (type): ")