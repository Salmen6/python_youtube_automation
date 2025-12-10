import os
import json
from openai import OpenAI
from typing import Dict
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_video_metadata(keyword: str) -> Dict:
    """Generate all video metadata in one API call"""
    prompt = f"""
Create complete YouTube video metadata for: "{keyword}"

Return JSON with:
- title (SEO-optimized, 60 chars max)
- thumbnail_text (4-6 attention-grabbing words)
- description (3-4 lines with CTA)
- tags (5-10 relevant keywords)
- script (250 words with hook/steps/CTA)

Example:
{{
  "title": "How to Delete Instagram Account Permanently (2024 Guide)",
  "thumbnail_text": "DELETE Instagram NOW",
  "description": "Step-by-step guide to permanently delete...",
  "tags": ["instagram", "delete account", "social media"],
  "script": "[Full script text]"
}}
"""
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        content = response.choices[0].message.content
        return json.loads(content)
    
    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing failed for metadata: {str(e)}")
        print(f"   Response was: {content if 'content' in locals() else 'N/A'}")
        return {
            "title": keyword,
            "thumbnail_text": keyword[:25],
            "description": "",
            "tags": [],
            "script": f"Script for: {keyword}"
        }
    
    except Exception as e:
        print(f"❌ Metadata generation failed: {str(e)}")
        return {
            "title": keyword,
            "thumbnail_text": keyword[:25],
            "description": "",
            "tags": [],
            "script": f"Script for: {keyword}"
        }