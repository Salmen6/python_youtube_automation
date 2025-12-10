import json
import requests
from typing import List, Set

def get_trending_topics() -> List[str]:
    """Read trending topics from topics.json"""
    try:
        with open("topics.json", "r") as f:
            data = json.load(f)
            return data.get("trending_topics", [])
    except FileNotFoundError:
        print("❌ topics.json not found. Please create it.")
        return []
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in topics.json: {str(e)}")
        return []

def get_search_prefixes() -> List[str]:
    """Read search prefixes from topics.json"""
    try:
        with open("topics.json", "r") as f:
            data = json.load(f)
            return data.get("search_prefixes", [])
    except FileNotFoundError:
        print("❌ topics.json not found. Please create it.")
        return []
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in topics.json: {str(e)}")
        return []

def get_suggestions(query: str) -> List[str]:
    """Get search suggestions from Google's API"""
    try:
        url = "https://suggestqueries.google.com/complete/search"
        params = {"client": "firefox", "ds": "yt", "q": query}
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            return response.json()[1]
        else:
            print(f"⚠ Google suggestions API returned {response.status_code} for '{query}'")
            return []
    
    except requests.Timeout:
        print(f"⚠ Timeout fetching suggestions for '{query}'")
        return []
    except Exception as e:
        print(f"⚠ Error fetching suggestions for '{query}': {str(e)}")
        return []

def explore_keywords(base: str, depth: int = 2, seen: Set[str] = None, max_iterations: int = 1000) -> List[str]:
    """Recursively explore keyword suggestions with safety limits"""
    if seen is None:
        seen = set()
    
    queue = [(base, 0)]
    results = []
    iterations = 0
    
    while queue and iterations < max_iterations:
        iterations += 1
        query, d = queue.pop(0)
        
        # Skip if already seen or depth exceeded
        if query in seen or d > depth:
            continue
        
        seen.add(query)
        suggestions = get_suggestions(query)
        results.extend(suggestions)
        
        # Only explore deeper if within depth limit
        if d < depth:
            for s in suggestions:
                if s not in seen:
                    queue.append((s, d + 1))
    
    if iterations >= max_iterations:
        print(f"⚠ Hit iteration limit ({max_iterations}) for '{base}'")
    
    return list(set(results))

def run_scraper(limit: int = 50) -> List[str]:
    """Main function to run the scraping process"""
    topics = get_trending_topics()
    prefixes = get_search_prefixes()
    
    if not topics or not prefixes:
        print("❌ Cannot scrape without topics and prefixes")
        return []
    
    # Generate queries like "how to * Instagram"
    prompts = []
    for prefix in prefixes:
        for topic in topics:
            prompts.append(prefix.replace("*", topic))
    
    print(f"📋 Generated {len(prompts)} search prompts")
    
    # Fetch suggestions for each prompt
    all_keywords = set()
    for i, prompt in enumerate(prompts, 1):
        print(f"  [{i}/{len(prompts)}] Exploring: {prompt}")
        keywords = explore_keywords(prompt)
        all_keywords.update(keywords)
        
        if len(all_keywords) >= limit:
            print(f"✅ Reached keyword limit ({limit})")
            break
    
    result = list(all_keywords)[:limit]
    print(f"✅ Scraped {len(result)} unique keywords")
    return result