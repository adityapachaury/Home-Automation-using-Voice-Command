import speech_recognition as sr
import requests

ESP_IP = "http://10.27.150.131"   # 👈 Replace with your ESP8266 IP

def send_command(command):
    try:
        if command == "on":
            r = requests.get(f"{ESP_IP}/ON", timeout=5)
            print("✅ Light turned ON (sent 1 to ESP) | Status:", r.status_code)
        elif command == "off":
            r = requests.get(f"{ESP_IP}/OFF", timeout=5)
            print("✅ Light turned OFF (sent 0 to ESP) | Status:", r.status_code)
    except Exception as e:
        pass
        # print("⚠ Failed to send command to ESP8266:", e)

OFF_KEYWORDS = ["off light", "turn off the light", "turn off light", "good night","light off","off the light","light turn off"]
ON_KEYWORDS  = ["on light", "turn on the light","turn on light", "good morning","light on","on the light","light turn on"]

def live_voice_to_text():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    print("🎤 Voice to Light Control Started...\n")
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        print("✅ Mic ready, start speaking...")

        while True:
            try:
                audio = recognizer.listen(source, timeout=2, phrase_time_limit=3)
                text = recognizer.recognize_google(audio).lower()
                print(f"🗣 You said: {text}")

                if any(k in text for k in ON_KEYWORDS):
                    send_command("on")

                elif any(k in text for k in OFF_KEYWORDS):
                    send_command("off")

            except sr.WaitTimeoutError:
                print("⏳ Waiting for your voice...")
            except sr.UnknownValueError:
                print("❌ Could not understand...")
            except KeyboardInterrupt:
                print("\n🛑 Stopped by user.")
                break

if __name__ == "__main__":
    live_voice_to_text()

