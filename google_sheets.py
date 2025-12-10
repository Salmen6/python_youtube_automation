from typing import List
import os
import gspread
import json
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

def sanitize_data(value):
    """Ensure data fits in Sheets cells"""
    if isinstance(value, str):
        return value[:49000]  # Sheets cell limit
    return str(value) if value is not None else ""

def save_to_sheet(rows: List[List]):
    """Save with backup system and improved error handling"""
    try:
        # Validate credentials file exists
        creds_file = os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE")
        if not creds_file:
            raise Exception("GOOGLE_SERVICE_ACCOUNT_FILE not set in environment")
        
        if not os.path.exists(creds_file):
            raise Exception(f"Credentials file not found: {creds_file}")
        
        # Initialize Google Sheets
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            creds_file,
            scope
        )
        client = gspread.authorize(creds)
        
        # Open or create sheet
        try:
            sheet = client.open("YouTube Automation Output").sheet1
        except gspread.exceptions.SpreadsheetNotFound:
            print("⚠ Sheet not found. Please create 'YouTube Automation Output' in Google Sheets")
            raise
        
        # Initialize headers if needed
        if not sheet.get_all_values():
            sheet.append_row([
                "Keyword", "Title", "Thumbnail Text",
                "Description", "Tags", "Script",
                "Voiceover Path", "Thumbnail Path",
                "Status", "Timestamp"
            ])
        
        # Process rows
        for row in rows:
            clean_row = [sanitize_data(item) for item in row]
            clean_row.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            sheet.append_row(clean_row)
        
        print(f"✅ Saved {len(rows)} rows to Google Sheets")
    
    except Exception as e:
        print(f"❌ Sheets error: {str(e)}")
        
        # Local backup with rotation
        try:
            backup_dir = Path("data/backups")
            backup_dir.mkdir(parents=True, exist_ok=True)
            
            # Date-based filename for rotation
            backup_file = backup_dir / f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            with open(backup_file, "w") as f:
                json.dump({
                    "data": rows,
                    "timestamp": str(datetime.now())
                }, f, indent=2)
            
            print(f"✅ Saved to backup: {backup_file}")
        
        except Exception as backup_error:
            print(f"❌ Backup failed: {str(backup_error)}")