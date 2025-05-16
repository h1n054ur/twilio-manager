"""Search & purchase logic"""
import time
from typing import List, Optional
from app.gateways.http_gateway import search_batch
from app.models.phone_number_model import NumberRecord, SearchSession
from app.gateways.twilio_gateway import purchase_number

def search_available_numbers(country: str, number_type: str, capabilities: list, pattern: str = '', locality: Optional[str] = None) -> List[NumberRecord]:
    session = SearchSession(unique_count=0, empty_streaks=0, batches=[])
    page_token = None
    unique_sids = set()

    while session.unique_count < 500 and session.empty_streaks < 3:
        data = search_batch(country, number_type, capabilities, page_size=50, page_token=page_token)
        page_token = data.get('next_page_uri', None)
        batch = []
        for rec in data.get('available_phone_numbers', []):
            sid = rec.get('sid')
            number = rec.get('phone_number')
            city = rec.get('locality')
            state = rec.get('region')
            price = rec.get('price')
            if pattern and pattern not in number:
                continue
            if locality and city != locality:
                continue
            if sid in unique_sids:
                continue
            unique_sids.add(sid)
            batch.append(NumberRecord(sid=sid, number=number, city=city, state=state, type=number_type, price=price))
        if batch:
            session.batches.append(batch)
            session.unique_count += len(batch)
            session.empty_streaks = 0
        else:
            session.empty_streaks += 1
        time.sleep(1)
    return [num for batch in session.batches for num in batch]

def purchase_numbers(sids: List[str]) -> List:
    results = []
    for sid in sids:
        result = purchase_number(sid)
        results.append(result)
    return results