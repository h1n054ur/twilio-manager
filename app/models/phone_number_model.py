from dataclasses import dataclass
from typing import List

@dataclass
class NumberRecord:
    sid: str
    number: str
    city: str
    state: str
    type: str
    price: float

@dataclass
class SearchSession:
    unique_count: int
    empty_streaks: int
    batches: List[List[NumberRecord]]