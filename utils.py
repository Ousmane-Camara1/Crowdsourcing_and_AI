import speech_recognition as sr
import csv
import time
import os

from kokoro import KPipeline
import sounddevice as sd

# Initialize TTS pipeline
pipeline = KPipeline(lang_code='a')  # English

def speak(text, gender="female"):
    print(f"AI: {text}")  # Visual feedback
    
    # Choose voice (adjust if your Kokoro setup has different voices)
    voice = "af_heart" if gender == "female" else "am_michael"

    try:
        # Generate and play audio
        generator = pipeline(text, voice=voice)
        
        for _, _, audio in generator:
            sd.play(audio, samplerate=24000)
            sd.wait()

    except Exception as e:
        print(f"TTS Error: {e}")


def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source, duration=1)
        
        start_time = time.time() # Start timer
        try:
            audio = r.listen(source, timeout=5)
            latency = time.time() - start_time # Calculate response delay
            text = r.recognize_google(audio)
            print(f"User said: {text} (Latency: {latency:.2f}s)")
            return text.lower(), latency
        except sr.WaitTimeoutError:
            print("Silence detected.")
            return None, 5.0 # Max timeout reached
        except sr.UnknownValueError:
            print("Could not understand audio.")
            return None, 0.0


def log_metric(question_id, event_type):
    with open('logs/dropoff_metrics.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            time.strftime("%Y-%m-%d %H:%M:%S"),
            question_id,
            event_type
        ])
