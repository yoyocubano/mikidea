# WhatsApp Audio Transcriber

Robust, configurable tool for transcribing WhatsApp audio messages using OpenAI Whisper.

## Features

✅ **Unified Solution**: Replaces both `transcribe_last_3.py` and `batch_transcribe_whatsapp.py`  
✅ **Environment Configuration**: No more hardcoded paths - use `.env` file  
✅ **Dependency Validation**: Checks for ffmpeg and Whisper models before running  
✅ **Structured Logging**: Console + file logging with configurable levels  
✅ **Progress Tracking**: Visual progress bars with tqdm  
✅ **Error Handling**: Comprehensive try-catch blocks with graceful failures  
✅ **CLI Interface**: Flexible command-line arguments  
✅ **Metadata Preservation**: Includes timestamps and model info in outputs  

## Installation

```bash
# Install Python dependencies
pip install openai-whisper python-dotenv tqdm

# Install ffmpeg (required for audio decoding)
# macOS:
brew install ffmpeg

# Linux:
sudo apt-get install ffmpeg

# Ubuntu/Debian:
sudo apt-get install ffmpeg libavcodec-extra
```

## Configuration

1. Copy the example environment file:
```bash
cd scripts
cp .env.example .env
```

2. Edit `.env` with your paths:
```env
WHATSAPP_MEDIA_PATH=/path/to/whatsapp/media
OUTPUT_DIR=/path/to/output/directory
MODEL_SIZE=base
BATCH_LIMIT=10
LOG_LEVEL=INFO
```

## Usage

### Quick Start (Last 3 Audios)
```bash
python whatsapp_transcriber.py
```

### Batch Mode (Last 10 Audios)
```bash
python whatsapp_transcriber.py --mode batch
```

### Custom Limit
```bash
python whatsapp_transcriber.py --mode batch --limit 5
```

### Different Model Size
```bash
# Faster but less accurate
python whatsapp_transcriber.py --model tiny

# Slower but more accurate
python whatsapp_transcriber.py --model medium
```

### Verbose Output
```bash
python whatsapp_transcriber.py --verbose
```

### Full Example
```bash
python whatsapp_transcriber.py --mode batch --limit 7 --model small --verbose
```

## CLI Options

| Option | Description | Default |
|--------|-------------|---------|
| `--mode` | `last` (3 audios) or `batch` (configurable) | `last` |
| `--limit` | Number of audios to process | 10 (from .env) |
| `--model` | Whisper model: tiny, base, small, medium, large | base |
| `--verbose` | Enable detailed Whisper output | False |

## Model Sizes

| Model | Relative Speed | Accuracy | VRAM Required |
|-------|---------------|----------|---------------|
| tiny  | ~32x          | Lower    | ~1 GB         |
| base  | ~16x          | Good     | ~1 GB         |
| small | ~6x           | Better   | ~2 GB         |
| medium| ~2x           | High     | ~5 GB         |
| large | 1x            | Highest  | ~10 GB        |

## Output Structure

```
output_directory/
├── transcription_20250101_120000_audio1.txt
├── transcription_20250101_120005_audio2.txt
├── transcription_20250101_120010_audio3.txt
├── RESUMEN_LOTE_20250101_120015.md
└── transcription.log
```

### Individual Transcription File Format
```
Archivo Original: /path/to/audio.opus
Fecha de Grabación: 2025-01-01 12:00:00
Fecha de Transcripción: 2025-01-01 12:05:00
Modelo Whisper: base
--------------------------------------------------
[Transcribed text here]
```

### Summary Markdown
Includes all transcriptions with links to individual files for easy reference.

## Migration from Old Scripts

### From `transcribe_last_3.py`:
```bash
# Old way:
python transcribe_last_3.py

# New way (same result):
python whatsapp_transcriber.py --mode last
```

### From `batch_transcribe_whatsapp.py`:
```bash
# Old way:
python batch_transcribe_whatsapp.py

# New way (same result):
python whatsapp_transcriber.py --mode batch
```

## Troubleshooting

### "ffmpeg not found"
```bash
# Install ffmpeg
brew install ffmpeg  # macOS
sudo apt-get install ffmpeg  # Linux
```

### "No .opus files found"
- Verify `WHATSAPP_MEDIA_PATH` in `.env` is correct
- Check that you have read permissions for the directory
- Ensure WhatsApp has actually received voice messages

### "Out of memory"
- Use a smaller model: `--model tiny` or `--model base`
- Reduce batch size: `--limit 3`

### Model download issues
```bash
# Pre-download models
python -c "import whisper; whisper.load_model('base')"
```

## Logging

Logs are written to:
- Console (real-time)
- File: `$OUTPUT_DIR/transcription.log`

Log levels: DEBUG, INFO, WARNING, ERROR

Configure in `.env`:
```env
LOG_LEVEL=DEBUG  # For detailed troubleshooting
```

## License

MIT License - Feel free to modify and distribute.

## Author

Aguilar-Guilarte AI Agent Toolkit
