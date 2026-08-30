import time
from voice import speak, listen
from main import ask_jarvis

WAKE_WORD = "jarvis"

def run_voice_mode():
    history = []
    speak("Jarvis online. Say my name to wake me, or type your command.")
    
    print(f"\nListening for wake word: '{WAKE_WORD}'")
    print("Or press Enter to type your command\n")
    
    while True:
        print("(Waiting... say 'jarvis' or press Enter)")
        user_input = listen(timeout=5)
        
        # Check for wake word
        if user_input and WAKE_WORD in user_input.lower():
            speak("Yes? I'm listening.")
            user_input = listen(timeout=10)
        
        # Also allow Enter key for text input
        # (Handled by fallback in listen() on RequestError)
        
        if not user_input:
            continue
            
        if any(word in user_input.lower()
               for word in ["shutdown", "goodbye", "turn off"]):
            speak("Shutting down. Goodbye.")
            break
        
        speak("Let me think about that.")
        reply = ask_jarvis(user_input, history)
        speak(reply)
        time.sleep(0.5)

def run_text_mode():
    history = []
    print("\n  Jarvis online (text mode). Type 'exit' to quit.\n")
    while True:
        user = input("You: ").strip()
        if not user: continue
        if user.lower() in ["exit", "quit", "bye"]:
            print("Jarvis: Goodbye."); break
        print("Jarvis: thinking...\n")
        reply = ask_jarvis(user, history)
        print(f"Jarvis: {reply}\n")

if __name__ == "__main__":
    print("=== JARVIS AI ===")
    print("1. Voice mode (microphone)")
    print("2. Text mode (keyboard)")
    choice = input("Choose (1 or 2): ").strip()
    if choice == "1":
        run_voice_mode()
    else:
        run_text_mode()