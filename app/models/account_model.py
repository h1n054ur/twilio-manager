from dataclasses import dataclass

@dataclass
class UsageStats:
    usage: float
    cost: float
    projection: float