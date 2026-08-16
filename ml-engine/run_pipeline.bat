@echo off
cd /d "C:\Users\elidr\Documents\pfa\V2\CyberThreatDetection-DevOps\ml-engine"
call venv\Scripts\activate.bat
python src\run_pipeline.py >> logs\pipeline.log 2>&1