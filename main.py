from typing import List, Dict
import schedule
import time
import os
from dotenv import load_dotenv
from scraper import run_scraper
from analyzer import filter_keywords
from content.script_gen import generate_video_metadata
from content.voiceover import generate_voiceovers
from content.thumbnail import generate_thumbnails
from google_sheets import save_to_sheet
from startup_validator import validate_environment

load_dotenv()

# Configuration from environment
KEYWORD_LIMIT = int(os.getenv("KEYWORD_LIMIT", "20"))
SCHEDULE_TIME = os.getenv("SCHEDULE_TIME", "06:00")

def process_keyword(keyword: Dict) -> List:
    """Handle single keyword processing with error handling"""
    try:
        print(f"🔍 Processing: {keyword['query']}")
        
        # Generate content
        metadata = generate_video_metadata(keyword["query"])
        if not metadata:
            print(f"⚠ Metadata generation failed for {keyword['query']}")
            return None
        
        voice_path = generate_voiceovers(metadata["title"], metadata["script"])
        if not voice_path:
            print(f"⚠ Voiceover generation failed for {keyword['query']}")
            # Continue anyway - we can still save the metadata
        
        thumb_path = generate_thumbnails(metadata["thumbnail_text"], metadata["tags"])
        if not thumb_path:
            print(f"⚠ Thumbnail generation failed for {keyword['query']}")
            # Continue anyway
        
        return [
            keyword["query"],              # Original keyword
            metadata["title"],             # Optimized title
            metadata["thumbnail_text"],    # Thumbnail text
            metadata["description"],       # Video description
            ", ".join(metadata["tags"]),   # Tags as string
            metadata["script"],            # Full script
            voice_path or "FAILED",        # Voiceover path
            thumb_path or "FAILED",        # Thumbnail path
            "Done"                         # Status
        ]
    
    except Exception as e:
        print(f"❌ Failed on {keyword['query']}: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

def daily_job():
    """Main automation job"""
    print("\n" + "="*60)
    print("🚀 Starting automation job...")
    print("="*60)
    
    try:
        # Get and process keywords
        print("📊 Scraping keywords...")
        raw_keywords = run_scraper(limit=KEYWORD_LIMIT)
        print(f"✅ Found {len(raw_keywords)} raw keywords")
        
        print("🔍 Filtering and scoring keywords...")
        filtered_keywords = filter_keywords(raw_keywords)
        print(f"✅ Filtered to {len(filtered_keywords)} keywords")
        
        if not filtered_keywords:
            print("⚠ No keywords to process")
            return
        
        # Process all keywords
        results = []
        success_count = 0
        fail_count = 0
        
        for i, keyword in enumerate(filtered_keywords, 1):
            print(f"\n[{i}/{len(filtered_keywords)}] Processing keyword...")
            
            try:
                row = process_keyword(keyword)
                if row:
                    results.append(row)
                    success_count += 1
                else:
                    fail_count += 1
            except Exception as e:
                print(f"❌ Unexpected error processing keyword: {str(e)}")
                fail_count += 1
        
        # Save results
        if results:
            print(f"\n💾 Saving {len(results)} results to Google Sheets...")
            save_to_sheet(results)
            print(f"✅ Job finished. Success: {success_count}, Failed: {fail_count}")
        else:
            print("⚠ No results to save")
    
    except Exception as e:
        print(f"🔥 Critical job failure: {str(e)}")
        import traceback
        traceback.print_exc()
    
    print("="*60 + "\n")

if __name__ == "__main__":
    # Validate environment before starting
    validate_environment()
    
    # Run initial test
    print("🎯 Running initial test job...")
    daily_job()
    
    # Setup scheduler
    print(f"\n⏰ Scheduling daily job at {SCHEDULE_TIME}")
    schedule.every().day.at(SCHEDULE_TIME).do(daily_job)
    
    print("🔄 Scheduler running. Press Ctrl+C to stop.\n")
    while True:
        schedule.run_pending()
        time.sleep(60)