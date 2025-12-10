"""
Startup validator to check all required dependencies before running
Add this import to main.py: from startup_validator import validate_environment
Call validate_environment() at the start of main.py before anything else
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

REQUIRED_ENV_VARS = {
    "OPENAI_API_KEY": "OpenAI API key for GPT-3.5",
    "YOUTUBE_API_KEY": "YouTube Data API v3 key",
    "ELEVENLABS_API_KEY": "ElevenLabs API key for voiceovers",
    "VOICE_ID": "ElevenLabs voice ID",
    "CANVA_API_KEY": "Canva API key for thumbnails",
    "CANVA_TEMPLATE_ID": "Canva template ID",
    "GOOGLE_SERVICE_ACCOUNT_FILE": "Path to Google service account JSON"
}

REQUIRED_FILES = [
    "topics.json"
]

REQUIRED_DIRS = [
    "data/output/voiceovers",
    "data/output/thumbnails",
    "data/backups"
]

def validate_environment() -> bool:
    """
    Validates all required environment variables, files, and directories.
    Returns True if all checks pass, exits with error message if any fail.
    """
    print("🔍 Validating environment...")
    errors = []
    
    # Check environment variables
    for var, description in REQUIRED_ENV_VARS.items():
        value = os.getenv(var)
        if not value:
            errors.append(f"❌ Missing env var: {var} ({description})")
        elif var == "GOOGLE_SERVICE_ACCOUNT_FILE":
            # Special check: verify file exists
            if not os.path.exists(value):
                errors.append(f"❌ File not found: {value} (specified in {var})")
    
    # Check required files
    for file in REQUIRED_FILES:
        if not os.path.exists(file):
            errors.append(f"❌ Missing required file: {file}")
    
    # Create required directories
    for directory in REQUIRED_DIRS:
        try:
            Path(directory).mkdir(parents=True, exist_ok=True)
        except Exception as e:
            errors.append(f"❌ Cannot create directory {directory}: {str(e)}")
    
    # Report results
    if errors:
        print("\n" + "="*60)
        print("🔥 ENVIRONMENT VALIDATION FAILED")
        print("="*60)
        for error in errors:
            print(error)
        print("\n💡 To fix:")
        print("1. Create a .env file with all required API keys")
        print("2. Create topics.json with trending_topics and search_prefixes")
        print("3. Obtain Google service account JSON file")
        print("="*60 + "\n")
        sys.exit(1)
    
    print("✅ Environment validation passed")
    return True

def create_sample_topics_json():
    """Helper to create sample topics.json if missing"""
    sample_content = {
        "trending_topics": [
            "TikTok",
            "Discord",
            "CapCut",
            "Photoshop",
            "Notion",
            "Instagram"
        ],
        "search_prefixes": [
            "how to *",
            "what is *",
            "best way to *",
            "why *"
        ]
    }
    
    import json
    with open("topics.json", "w") as f:
        json.dump(sample_content, f, indent=2)
    
    print("✅ Created sample topics.json")

if __name__ == "__main__":
    # Can run standalone to check environment
    validate_environment()
    print("🎉 All checks passed! Ready to run automation.")