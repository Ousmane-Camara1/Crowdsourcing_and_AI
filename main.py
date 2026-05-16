import json
import time
from utils import speak, listen, log_metric

def run_voice_survey(survey_path, voice_gender):
    print(f"--- STARTING VOICE AI SURVEY: {survey_path} ---")
    
    # Dynamically load the JSON selected from the UI
    with open(survey_path) as f:
        survey = json.load(f)

    # 1. LEGITIMACY & TRANSPARENCY
    intro = (
        f"Hello, I am an AI from {survey['metadata']['organization']}. "
        f"This survey takes {survey['metadata']['estimated_minutes']} minutes."
    )
    speak(intro, voice_gender)
    time.sleep(0.5)

    # 2. CONSENT GATE
    speak("Do you agree to participate? Please say Yes or No.", voice_gender)
    time.sleep(0.3)

    consent, _ = listen() # Adjusted to unpack tuple from latency patch

    if consent is None or not any(word in consent for word in ["yes", "yeah", "yep", "sure", "ok"]):
        log_metric("START", "CONSENT_DENIED")
        speak("I understand. Have a nice day.", voice_gender)
        return

    speak("Great, thank you. Let's begin.", voice_gender)
    time.sleep(0.4)

    # 3. MODULAR QUESTION LOOP
    for q in survey['questions']:
        if q.get('is_sensitive', False):
            speak("Your answer to this next question is anonymous.", voice_gender)
            time.sleep(0.3)

        attempts = 0
        response = None

        while response is None and attempts < 3:
            speak(q['text'], voice_gender)
            time.sleep(0.3)

            response, latency = listen()

            if latency > 0.0:
                log_metric(q['id'], f"LATENCY_{latency:.2f}S")

            if response is None:
                speak("I'm sorry, I didn't hear you. Let me repeat that.", voice_gender)
                attempts += 1
                time.sleep(0.3)

        if response is None:
            log_metric(q['id'], "TIMEOUT_SKIP")
            continue

        print("Processing...")

        if any(word in response for word in ["skip", "pass", "next"]):
            log_metric(q['id'], "USER_EXPLICIT_SKIP")
            speak("Moving on.", voice_gender)
            continue

        if any(word in response for word in ["stop", "exit", "quit", "cancel"]):
            log_metric(q['id'], "USER_WITHDRAWAL")
            speak("Ending survey. Your data is protected.", voice_gender)
            return

        log_metric(q['id'], "COMPLETED")

    # 4. DATA MINIMIZATION / END
    speak("Thank you. We are now anonymizing your responses.", voice_gender)
    speak("Your participation helps us improve community health initiatives. Have a great day!", voice_gender)