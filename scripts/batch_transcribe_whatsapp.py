import os
import glob
import time
import whisper
import sys

# === CONFIGURATION ===
WHATSAPP_MEDIA_PATH = "/Users/yoyocubano/Library/Group Containers/group.net.whatsapp.WhatsApp.shared/Message/Media/"
OUTPUT_DIR = "/Users/yoyocubano/.gemini/antigravity/scratch/whatsapp_transcriptions"
MODEL_SIZE = "base"

def get_latest_audios(limit=10):
    """Find the most recent .opus files in the WhatsApp media directory."""
    files = glob.glob(os.path.join(WHATSAPP_MEDIA_PATH, "**/*.opus"), recursive=True)
    if not files:
        return []
    
    # Sort by modification time (latest first)
    files.sort(key=os.path.getmtime, reverse=True)
    return files[:limit]

def transcribe_audio(file_path, model):
    """Transcribe a single audio file using a pre-loaded Whisper model."""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    print(f"\n🎬 Procesando: {os.path.basename(file_path)}")
    
    # Whisper uses ffmpeg internally to decode opus
    result = model.transcribe(file_path, verbose=False)
    text = result["text"].strip()
    
    # Save output
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filename = os.path.basename(file_path).split('.')[0]
    out_path = os.path.join(OUTPUT_DIR, f"transcription_{timestamp}_{filename}.txt")
    
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(f"Archivo Original: {file_path}\n")
        f.write(f"Fecha: {time.ctime(os.path.getmtime(file_path))}\n")
        f.write("-" * 30 + "\n")
        f.write(text)
        
    return text, out_path

def main():
    print("📱 Transcriptor por Lote de WhatsApp (Últimos 10)")
    print("-" * 50)
    
    audios = get_latest_audios(10)
    
    if not audios:
        print("❌ No se encontraron audios recientes.")
        return

    print(f"✅ Se encontraron {len(audios)} audios recientes. Cargando modelo...")
    model = whisper.load_model(MODEL_SIZE)
    
    results = []
    
    for i, audio in enumerate(audios):
        try:
            mtime = time.ctime(os.path.getmtime(audio))
            print(f"\n[{i+1}/10] {os.path.basename(audio)} ({mtime})")
            text, path = transcribe_audio(audio, model)
            print(f"📝 Transcripción: {text[:100]}...")
            results.append((audio, text, path))
        except Exception as e:
            print(f"❌ Error procesando {audio}: {e}")

    # Create a summary file
    summary_path = os.path.join(OUTPUT_DIR, f"RESUMEN_LOTE_{time.strftime('%Y%m%d_%H%M%S')}.md")
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write("# Resumen de Transcripciones por Lote\n\n")
        for audio, text, path in results:
            f.write(f"### Audio: {os.path.basename(audio)}\n")
            f.write(f"- **Archivo**: `{audio}`\n")
            f.write(f"- **Resultado**: [Ver archivo](file://{path})\n")
            f.write(f"- **Texto**: {text}\n\n")
            f.write("---\n\n")

    print("\n" + "="*50)
    print(f"🚀 Proceso completado. Resumen guardado en:\n{summary_path}")
    print("="*50)

if __name__ == "__main__":
    main()
