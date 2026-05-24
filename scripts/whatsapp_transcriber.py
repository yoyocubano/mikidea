"""
Unified WhatsApp Audio Transcription Tool

This script provides a robust, configurable solution for transcribing WhatsApp audio messages.
It includes proper error handling, logging, dependency validation, and progress tracking.

Usage:
    python whatsapp_transcriber.py [--mode last|batch] [--limit N] [--model SIZE]
    
Requirements:
    - pip install openai-whisper python-dotenv tqdm
    - ffmpeg installed and available in PATH
"""

import os
import sys
import glob
import time
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Tuple, Optional, Dict, Any

# Third-party imports
try:
    import whisper
    from dotenv import load_dotenv
    from tqdm import tqdm
except ImportError as e:
    print(f"❌ Missing dependency: {e}")
    print("Install with: pip install openai-whisper python-dotenv tqdm")
    sys.exit(1)

# Load environment variables
load_dotenv()

# Configuration from environment or defaults
CONFIG = {
    "WHATSAPP_MEDIA_PATH": os.getenv(
        "WHATSAPP_MEDIA_PATH", 
        "/Users/yoyocubano/Library/Group Containers/group.net.whatsapp.WhatsApp.shared/Message/Media/"
    ),
    "OUTPUT_DIR": os.getenv(
        "OUTPUT_DIR",
        "/Users/yoyocubano/.gemini/antigravity/scratch/whatsapp_transcriptions"
    ),
    "MODEL_SIZE": os.getenv("MODEL_SIZE", "base"),
    "BATCH_LIMIT": int(os.getenv("BATCH_LIMIT", "10")),
    "VERBOSE": os.getenv("VERBOSE", "false").lower() == "true",
    "LOG_LEVEL": os.getenv("LOG_LEVEL", "INFO"),
}

# Setup logging
def setup_logging(log_level: str) -> logging.Logger:
    """Configure structured logging with console and file output."""
    logger = logging.getLogger("whatsapp_transcriber")
    logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))
    
    # Console handler with colors
    console_handler = logging.StreamHandler(sys.stdout)
    console_format = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(message)s',
        datefmt='%H:%M:%S'
    )
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)
    
    # File handler (if output dir exists)
    try:
        log_file = Path(CONFIG["OUTPUT_DIR"]) / "transcription.log"
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_format = logging.Formatter(
            '%(asctime)s | %(name)s | %(levelname)-8s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_format)
        logger.addHandler(file_handler)
    except Exception:
        pass  # Skip file logging if directory doesn't exist yet
    
    return logger

logger = setup_logging(CONFIG["LOG_LEVEL"])


def validate_dependencies() -> bool:
    """Check that all required dependencies are available."""
    logger.debug("Validating dependencies...")
    
    # Check ffmpeg
    import subprocess
    try:
        subprocess.run(
            ["ffmpeg", "-version"], 
            capture_output=True, 
            timeout=5,
            check=True
        )
        logger.debug("✅ ffmpeg is available")
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        logger.error("❌ ffmpeg is not installed or not in PATH")
        logger.error("Install with: brew install ffmpeg (macOS) or apt-get install ffmpeg (Linux)")
        return False
    
    # Check Whisper model availability
    try:
        whisper.load_model(CONFIG["MODEL_SIZE"])
        logger.debug(f"✅ Whisper model '{CONFIG['MODEL_SIZE']}' loaded successfully")
    except Exception as e:
        logger.error(f"❌ Failed to load Whisper model: {e}")
        return False
    
    return True


def ensure_directories() -> bool:
    """Create output directories if they don't exist."""
    try:
        output_path = Path(CONFIG["OUTPUT_DIR"])
        output_path.mkdir(parents=True, exist_ok=True)
        logger.debug(f"✅ Output directory ready: {CONFIG['OUTPUT_DIR']}")
        return True
    except Exception as e:
        logger.error(f"❌ Cannot create output directory: {e}")
        return False


def validate_media_path() -> bool:
    """Verify the WhatsApp media path exists and is accessible."""
    media_path = Path(CONFIG["WHATSAPP_MEDIA_PATH"])
    
    if not media_path.exists():
        logger.error(f"❌ WhatsApp media path does not exist: {CONFIG['WHATSAPP_MEDIA_PATH']}")
        logger.error("Please update WHATSAPP_MEDIA_PATH in your .env file")
        return False
    
    if not os.access(media_path, os.R_OK):
        logger.error(f"❌ No read permission for: {CONFIG['WHATSAPP_MEDIA_PATH']}")
        return False
    
    logger.debug(f"✅ Media path validated: {CONFIG['WHATSAPP_MEDIA_PATH']}")
    return True


def find_audio_files(limit: int = 10) -> List[Path]:
    """Find the most recent .opus files in the WhatsApp media directory."""
    logger.debug(f"Searching for .opus files in {CONFIG['WHATSAPP_MEDIA_PATH']}")
    
    try:
        pattern = str(Path(CONFIG["WHATSAPP_MEDIA_PATH"]) / "**/*.opus")
        files = glob.glob(pattern, recursive=True)
        
        if not files:
            logger.warning("No .opus files found in WhatsApp media directory")
            return []
        
        # Sort by modification time (newest first)
        files.sort(key=lambda f: os.path.getmtime(f), reverse=True)
        
        logger.info(f"Found {len(files)} .opus files, selecting latest {min(limit, len(files))}")
        return [Path(f) for f in files[:limit]]
    
    except Exception as e:
        logger.error(f"Error searching for audio files: {e}")
        return []


def transcribe_audio(
    file_path: Path, 
    model: Any, 
    timestamp: Optional[str] = None
) -> Tuple[str, str, Optional[str]]:
    """
    Transcribe a single audio file.
    
    Returns:
        Tuple of (filename, transcribed_text, output_file_path)
    """
    filename = file_path.name
    
    try:
        logger.debug(f"Transcribing: {filename}")
        
        # Get file metadata
        file_mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
        
        # Perform transcription
        result = model.transcribe(str(file_path), verbose=CONFIG["VERBOSE"])
        text = result["text"].strip()
        
        if not text:
            logger.warning(f"No speech detected in {filename}")
            text = "[No speech detected]"
        
        # Generate output filename
        ts = timestamp or datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = file_path.stem
        output_filename = f"transcription_{ts}_{base_name}.txt"
        output_path = Path(CONFIG["OUTPUT_DIR"]) / output_filename
        
        # Write transcription to file
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(f"Archivo Original: {file_path}\n")
            f.write(f"Fecha de Grabación: {file_mtime.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Fecha de Transcripción: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Modelo Whisper: {CONFIG['MODEL_SIZE']}\n")
            f.write("-" * 50 + "\n")
            f.write(text + "\n")
        
        logger.debug(f"Saved transcription to {output_path}")
        return filename, text, str(output_path)
    
    except Exception as e:
        logger.error(f"Failed to transcribe {filename}: {e}")
        return filename, f"[Error: {str(e)}]", None


def save_summary(results: List[Tuple[str, str, Optional[str]]]) -> str:
    """Create a markdown summary of all transcriptions."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    summary_path = Path(CONFIG["OUTPUT_DIR"]) / f"RESUMEN_LOTE_{timestamp}.md"
    
    try:
        with open(summary_path, "w", encoding="utf-8") as f:
            f.write("# Resumen de Transcripciones por Lote\n\n")
            f.write(f"**Fecha**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Modelo**: {CONFIG['MODEL_SIZE']}\n")
            f.write(f"**Total de audios**: {len(results)}\n\n")
            f.write("---\n\n")
            
            for i, (filename, text, output_path) in enumerate(results, 1):
                f.write(f"## Audio {i}: {filename}\n\n")
                
                if output_path:
                    f.write(f"- **Archivo transcrito**: [{output_path}](file://{output_path})\n")
                else:
                    f.write("- **Estado**: Error en transcripción\n")
                
                f.write(f"- **Texto**: {text}\n\n")
                f.write("---\n\n")
        
        logger.info(f"Summary saved to {summary_path}")
        return str(summary_path)
    
    except Exception as e:
        logger.error(f"Failed to create summary: {e}")
        return ""


def run_transcription(mode: str = "last", limit: Optional[int] = None) -> Dict[str, Any]:
    """
    Main transcription runner.
    
    Args:
        mode: "last" for last 3 audios, "batch" for configurable limit
        limit: Override default limit
    
    Returns:
        Dictionary with results and statistics
    """
    logger.info("=" * 60)
    logger.info("🎙️ WhatsApp Audio Transcriber")
    logger.info("=" * 60)
    
    # Validate setup
    if not validate_dependencies():
        return {"success": False, "error": "Dependency validation failed"}
    
    if not ensure_directories():
        return {"success": False, "error": "Cannot create output directories"}
    
    if not validate_media_path():
        return {"success": False, "error": "Invalid media path"}
    
    # Determine limit based on mode
    if mode == "last":
        actual_limit = 3
        logger.info("Mode: Last 3 audios")
    else:  # batch
        actual_limit = limit or CONFIG["BATCH_LIMIT"]
        logger.info(f"Mode: Batch ({actual_limit} audios)")
    
    # Find audio files
    audio_files = find_audio_files(actual_limit)
    
    if not audio_files:
        logger.warning("No audio files to process")
        return {"success": True, "count": 0, "results": []}
    
    # Load Whisper model
    logger.info(f"Loading Whisper model: {CONFIG['MODEL_SIZE']}")
    try:
        model = whisper.load_model(CONFIG["MODEL_SIZE"])
    except Exception as e:
        logger.error(f"Failed to load model: {e}")
        return {"success": False, "error": str(e)}
    
    # Process audios with progress bar
    results = []
    errors = 0
    
    logger.info(f"Processing {len(audio_files)} audio(s)...")
    
    for i, audio_path in enumerate(tqdm(audio_files, desc="Transcribing", unit="audio")):
        logger.info(f"[{i+1}/{len(audio_files)}] {audio_path.name}")
        
        filename, text, output_path = transcribe_audio(audio_path, model)
        results.append((filename, text, output_path))
        
        if output_path is None:
            errors += 1
        
        # Preview first 100 chars
        preview = text[:100] + "..." if len(text) > 100 else text
        logger.info(f"📝 {preview}")
    
    # Create summary
    if results:
        summary_path = save_summary(results)
        logger.info(f"✅ Summary: {summary_path}")
    
    # Statistics
    stats = {
        "success": errors == 0,
        "total": len(audio_files),
        "processed": len(results),
        "errors": errors,
        "results": results,
    }
    
    logger.info("=" * 60)
    logger.info(f"🚀 Completed: {stats['processed']}/{stats['total']} audios")
    if errors > 0:
        logger.warning(f"⚠️ {errors} error(s) occurred")
    logger.info("=" * 60)
    
    return stats


def main():
    """CLI entry point with argument parsing."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Transcribe WhatsApp audio messages using Whisper AI"
    )
    parser.add_argument(
        "--mode", 
        choices=["last", "batch"], 
        default="last",
        help="Mode: 'last' for 3 audios, 'batch' for configurable limit (default: last)"
    )
    parser.add_argument(
        "--limit", 
        type=int, 
        default=None,
        help=f"Number of audios to process in batch mode (default: {CONFIG['BATCH_LIMIT']})"
    )
    parser.add_argument(
        "--model",
        type=str,
        default=None,
        choices=["tiny", "base", "small", "medium", "large"],
        help=f"Whisper model size (default: {CONFIG['MODEL_SIZE']})"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output from Whisper"
    )
    
    args = parser.parse_args()
    
    # Override config with CLI args
    if args.model:
        CONFIG["MODEL_SIZE"] = args.model
    if args.verbose:
        CONFIG["VERBOSE"] = True
    
    # Run transcription
    results = run_transcription(mode=args.mode, limit=args.limit)
    
    # Exit with appropriate code
    sys.exit(0 if results.get("success", False) else 1)


if __name__ == "__main__":
    main()
