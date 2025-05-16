"""Optional file-based JSON logger"""
import json
from datetime import datetime
from pathlib import Path

LOG_PATH = Path('file_logs.json')

class FileLogger:
    def __init__(self, path: Path = LOG_PATH):
        self.path = path
        if not self.path.exists():
            self.path.write_text("[]")

    def log(self, record: dict):
        data = json.loads(self.path.read_text())
        record['timestamp'] = datetime.utcnow().isoformat()
        data.append(record)
        self.path.write_text(json.dumps(data, indent=2))