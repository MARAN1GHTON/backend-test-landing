import json
import os
from datetime import datetime

METRICS_FILE = "data/metrics.json"

def _init_file(filepath: str, default_data: dict):
    if not os.path.exists(filepath):
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(default_data, f)

def save_contact_request(data: dict):
    _init_file(METRICS_FILE, {"total_requests": 0, "requests": []})
    
    with open(METRICS_FILE, 'r+', encoding='utf-8') as f:
        file_data = json.load(f)
        
        file_data["total_requests"] += 1
        
        # Save minimal data for metrics
        data["timestamp"] = datetime.utcnow().isoformat()
        file_data["requests"].append(data)
        
        f.seek(0)
        json.dump(file_data, f, indent=4, ensure_ascii=False)
        f.truncate()

def get_metrics() -> dict:
    _init_file(METRICS_FILE, {"total_requests": 0, "requests": []})
    with open(METRICS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)
