import os
from pathlib import Path
from elevenlabs import ElevenLabs
from dotenv import load_dotenv

load_dotenv()

client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

def _slugify(text):
    """Sanitize text for filename usage"""
    return text.lower().replace(" ", "_").replace("/", "_").replace(":", "_").replace("?", "")[:100]

def generate_voiceovers(title, text):
    """Generate voiceover with proper path handling"""
    try:
        # Create output directory
        output_dir = Path("data/output/voiceovers")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate audio
        audio = client.text_to_speech.convert(
            text=text,
            voice_id=os.getenv("VOICE_ID"),
            model_id="eleven_multilingual_v2",
            output_format="mp3_44100_128"
        )
        
        # Save with sanitized filename
        safe_title = _slugify(title)
        path = output_dir / f"{safe_title}.mp3"
        
        with open(path, "wb") as f:
            for chunk in audio:
                f.write(chunk)
        
        return str(path)
    
    except Exception as e:
        print(f"❌ Voiceover generation failed for '{title}': {str(e)}")
        return None