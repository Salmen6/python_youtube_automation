# YouTube Automation Pipeline

**Automated Keyword Research → Metadata → Voiceovers → Thumbnails → Reporting**  

This project is an end-to-end YouTube automation system built to explore how far AI-driven content workflows can be pushed. It handles everything from keyword discovery to video metadata, audio generation, thumbnail creation, and daily reporting — with no manual input required.  
It also serves as a portfolio piece showcasing automation, API orchestration, and production-ready workflow design.

---

## 🧭 Overview

The system runs on a daily schedule and automatically:

- Discovers trending keyword opportunities using Google Autocomplete
- Clusters and scores keywords based on competition and RPM potential
- Generates full video metadata using GPT
- Produces AI voiceovers with ElevenLabs
- Designs thumbnails via the Canva API
- Logs all outputs to Google Sheets (with JSON fallback backups)

Whether you want to extend it, integrate additional AI models, or simply understand the structure, the project is designed to be readable and easy to modify.

---

## Workflow Diagram

<img src="https://github.com/user-attachments/assets/d1b33819-31b4-479f-bf6e-4e5222b90af9" width="600" />

---

## ✨ Features

### 🔍 Smart Keyword Discovery
- Reads configuration from `topics.json`
- Expands topics using recursive BFS keyword exploration
- Fetches real Google Autocomplete suggestions
- Produces clean, unique keyword lists

### 📊 Intelligent Keyword Analysis
- Clusters related keywords using GPT in JSON mode
- Scores each keyword based on YouTube search competition
- Boosts keywords with strong revenue potential
- Outputs the top-performing opportunities each day

### 📝 Automated Metadata Generation
- GPT-powered title, description, tags, script, and thumbnail text
- Designed for SEO performance
- All metadata is generated in a single optimized call

### 🎤 Voiceover Generation (ElevenLabs)
- Converts scripts into high-quality MP3 voiceovers
- Saves clean audio files to `/data/output/voiceovers`

### 🖼️ Thumbnail Generation (Canva API)
- Creates thumbnails from a predefined template
- Automatically inserts generated text and visuals
- Outputs production-ready PNG images

### 📑 Reporting to Google Sheets
- Records all metadata, scores, and output paths
- Includes backup logging to `backup_data.json`
- Ideal for tracking daily content opportunities

---

## 🧱 Project Structure

youtube_automation/
├── main.py # Orchestration + scheduler
├── scraper.py # Keyword discovery logic
├── analyzer.py # Clustering, scoring, filtering
├── google_sheets.py # Persistence + backups
├── topics.json # Config file
├── requirements.txt # Dependencies
├── setup.py # Packaging info
└── content/
├── script_gen.py # Metadata generation (GPT)
├── voiceover.py # ElevenLabs TTS
└── thumbnail.py # Canva API integration

yaml
Copy code

---

## ⚙️ Minimal Setup

Install dependencies:

```bash
pip install -r requirements.txt
Add your API keys (OpenAI, ElevenLabs, YouTube Data, Google, Canva).
Place your topics.json into the root directory.

Run the script:

bash
Copy code
python main.py
The default scheduler runs daily at 06:00.
You can modify the schedule in main.py.

🛠️ Tech Stack
Python 3.8+

OpenAI GPT-3.5/4

ElevenLabs TTS

Canva API (Thumbnail automation)

Google Sheets API

YouTube Data API

schedule (lightweight cron alternative)

📌 Status
This project is actively evolving but fully functional.
New modules, optimizations, and UI dashboards may be added later.

🧑‍💻 Credits
Created by Salmeen
Open to contributions, suggestions, and improvements.

📜 License
This project is licensed under the MIT License, making it free to use, modify, and exten
