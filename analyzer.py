from typing import List, Dict
import json
import os
import requests
import time
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

HIGH_RPM_KEYWORDS = [
    "make money online",
    "investing for beginners",
    "best software tools",
    "business tips"
]

def is_high_rpm(query: str) -> bool:
    return any(keyword in query.lower() for keyword in HIGH_RPM_KEYWORDS)

def cluster_and_dedup(queries: List[str]) -> List[Dict]:
    """Cluster keywords with retry logic and proper error handling"""
    max_retries = 3
    retry_delay = 5
    
    prompt = f"""Group these queries into clusters. For each:
- "title": Best representative title (60 chars max)
- "tags": 5-10 relevant tags
Return JSON format like: {{"clusters": [{{"title": "...", "tags": [...]}}]}}

Queries: {queries}"""
    
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                response_format={"type": "json_object"},
                messages=[{"role": "user", "content": prompt}]
            )
            content = response.choices[0].message.content
            result = json.loads(content)
            return result.get("clusters", [])
        
        except json.JSONDecodeError as e:
            print(f"⚠ JSON parsing failed (attempt {attempt + 1}): {str(e)}")
            print(f"   Response was: {content if 'content' in locals() else 'N/A'}")
            if attempt == max_retries - 1:
                return [{"title": q, "tags": []} for q in queries]
            time.sleep(retry_delay * (attempt + 1))
        
        except Exception as e:
            print(f"⚠ API error (attempt {attempt + 1}): {str(e)}")
            if attempt == max_retries - 1:
                return [{"title": q, "tags": []} for q in queries]
            time.sleep(retry_delay * (attempt + 1))

def score_query(query: str) -> float:
    """Score keyword based on competition"""
    try:
        api_key = os.getenv("YOUTUBE_API_KEY")
        if not api_key:
            print("⚠ YOUTUBE_API_KEY not set")
            return 0
        
        url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}&maxResults=5&key={api_key}"
        res = requests.get(url, timeout=10).json()
        
        total = res.get("pageInfo", {}).get("totalResults", 0)
        
        # Improved scoring: normalize to 0-100 range
        # Lower competition = higher score
        score = max(0, min(100, 100 - (total / 10000)))
        return score
    
    except Exception as e:
        print(f"⚠ YouTube API error for '{query}': {str(e)}")
        return 0

def filter_keywords(queries: List[str]) -> List[Dict]:
    """Process and score keywords"""
    if not queries:
        return []
    
    clusters = cluster_and_dedup(queries)
    scored = []
    
    for cluster in clusters:
        score = score_query(cluster["title"])
        
        # Apply high RPM multiplier
        if is_high_rpm(cluster["title"]):
            score *= 1.5
        
        scored.append({
            "query": cluster["title"],
            "title": cluster["title"],
            "tags": cluster.get("tags", []),
            "score": score
        })
    
    return sorted(scored, key=lambda x: x["score"], reverse=True)[:20]