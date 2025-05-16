from dataclasses import dataclass
from datetime import datetime

@dataclass
class LogEntry:
    timestamp: datetime
    direction: str
    status: str
    details: str