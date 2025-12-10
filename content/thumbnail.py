import os
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

LOGO_URLS = {
    "instagram": "https://yourcdn.com/logos/instagram.png",
    "tiktok": "https://yourcdn.com/logos/tiktok.png",
    "notion": "https://yourcdn.com/logos/notion.png",
    "default": "https://yourcdn.com/logos/default.png"
}

def _slugify(text):
    return text.lower().replace(" ", "_").replace("/", "_")[:100]

def _extract_app_name(text):
    text = text.lower()
    for app in LOGO_URLS:
        if app in text:
            return app
    return "default"

def generate_thumbnails(thumbnail_text: str, tags: list) -> str:
    """Generate thumbnail using prepared thumbnail text"""
    try:
        template_id = os.getenv("CANVA_TEMPLATE_ID")
        if not template_id:
            raise Exception("Missing CANVA_TEMPLATE_ID")
        
        headers = {
            "Authorization": f"Bearer {os.getenv('CANVA_API_KEY')}",
            "Content-Type": "application/json"
        }
        
        app = _extract_app_name(thumbnail_text)
        logo_url = LOGO_URLS.get(app, LOGO_URLS["default"])
        
        design_payload = {
            "template_id": template_id,
            "title": thumbnail_text,
            "components": [
                {"id": "title_text", "type": "TEXT", "properties": {"text": thumbnail_text}},
                {"id": "app_logo", "type": "IMAGE", "properties": {"url": logo_url}}
            ]
        }
        
        # Create the design
        design_res = requests.post(
            "https://api.canva.com/rest/v1/designs",
            headers=headers,
            json=design_payload,
            timeout=30
        )
        design = design_res.json()
        if "id" not in design:
            raise Exception(f"Design failed: {design}")
        
        # Export the design
        export_res = requests.post(
            f"https://api.canva.com/rest/v1/designs/{design['id']}/export",
            headers=headers,
            json={"format": "PNG"},
            timeout=30
        )
        export = export_res.json()
        if "url" not in export:
            raise Exception(f"Export failed: {export}")
        
        # Download the PNG
        response = requests.get(export["url"], timeout=30)
        
        # Create output directory
        output_dir = Path("data/output/thumbnails")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        out_path = output_dir / f"{_slugify(thumbnail_text)}.png"
        with open(out_path, "wb") as f:
            f.write(response.content)
        
        return str(out_path)
    
    except Exception as e:
        print(f"❌ Thumbnail generation failed: {str(e)}")
        return None