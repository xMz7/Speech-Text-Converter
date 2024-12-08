import sounddevice as sd
import queue
import vosk
import json

# تحميل نموذج اللغة العربية
model_path = "C:/Users/hhhaa/OneDrive/Desktop/Projects/vosk-model-ar-mgb2-0.4"  # استبدل هذا بالمسار الفعلي للمجلد
model = vosk.Model(model_path)

# إعداد الميكروفون
q = queue.Queue()

def callback(indata, frames, time, status):
    if status:
        print(status)
    q.put(bytes(indata))

with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                       channels=1, callback=callback):
    rec = vosk.KaldiRecognizer(model, 16000)
    print("ابدأ بالتحدث...")

    while True:
        data = q.get()
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            print("النص المحول:", result.get("text", ""))
