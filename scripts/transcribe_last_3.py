import os
import glob
import time
import whisper

# === CONFIGURATION ===
WHATSAPP_MEDIA_PATH = "/Users/yoyocubano/Library/Group Containers/group.net.whatsapp.WhatsApp.shared/Message/Media/"
OUTPUT_DIR = "/Users/yoyocubano/.gemini/antigravity/scratch/whatsapp_transcriptions"
MODEL_SIZE = "base"

def get_latest_audios(limit=3):
    """Find the most recent .opus files in the WhatsApp media directory."""
    files = glob.glob(os.path.join(WHATSAPP_MEDIA_PATH, "**/*.opus"), recursive=True)
    if not files:
        return []
    files.sort(key=os.path.getmtime, reverse=True)
    return files[:limit]

def main():
    print("📱 Transcriptor de Últimos 3 Audios")
    audios = get_latest_audios(3)
    if not audios:
        print("❌ No se encontraron audios.")
        return

    model = whisper.load_model(MODEL_SIZE)
    results = []
    
    for i, audio in enumerate(audios):
        print(f"\n🎬 {i+1}/3: {os.path.basename(audio)}")
        result = model.transcribe(audio, verbose=False)
        text = result["text"].strip()
        results.append((audio, text))
        print(f"📝: {text[:100]}...")

    # Save to a specific file for analysis
    analysis_path = "/Users/yoyocubano/.gemini/antigravity/scratch/last_3_transcriptions.txt"
    with open(analysis_path, "w", encoding="utf-8") as f:
        for audio, text in results:
            f.write(f"FILE: {os.path.basename(audio)}\n")
            f.write(f"TEXT: {text}\n\n")
    print(f"\n✅ Guardado en {analysis_path}")

if __name__ == "__main__":
    main()
