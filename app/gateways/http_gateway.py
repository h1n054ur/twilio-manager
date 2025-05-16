import os
import time
import requests
from app.models.country_data import COUNTRY_DATA
from app.models.phone_number_model import NumberRecord

class HttpGateway:
    def __init__(self):
        from app.gateways.config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN
        self.account_sid = TWILIO_ACCOUNT_SID
        self.auth_token = TWILIO_AUTH_TOKEN
        self.base_url = f"https://api.twilio.com/2010-04-01/Accounts/{self.account_sid}"

    def get_number_types(self, country):
        # Fetch available phone number types for a country
        # For simplicity, return keys of COUNTRY_DATA pricing info
        return list(COUNTRY_DATA.get(country, {}).get('number_types', {}).keys())

    def search_batch(self, country, number_type, capabilities, pattern, locality, progress_callback):
        # Build query parameters
        results = []
        seen = set()  # Track seen phone numbers for uniqueness
        empty_rounds = 0
        page_size = 50
        next_page_uri = f"/AvailablePhoneNumbers/{country}/{number_type}.json?PageSize={page_size}"
        # Apply initial filters
        # capabilities filter will be applied client-side
        
        while len(results) < 500 and empty_rounds < 3 and next_page_uri:
            url = self.base_url + next_page_uri
            params = {}
            if pattern and not locality:
                # Digits search: treat pattern as Contains
                params['Contains'] = pattern
            if locality:
                # Locality search
                params['InRegion'] = locality
            # Make request
            resp = requests.get(url, auth=(self.account_sid, self.auth_token), params=params)
            resp.raise_for_status()
            data = resp.json()
            page_numbers = data.get('available_phone_numbers', [])
            new_count = 0
            for entry in page_numbers:
                number_str = entry.get('phone_number')
                if number_str not in seen:
                    seen.add(number_str)
                    # Map to NumberRecord
                    rec = NumberRecord(
                        phone_number=entry.get('phone_number'),
                        city=entry.get('locality'),
                        state=entry.get('region'),
                        type=entry.get('capabilities', {}).keys(),
                        price=entry.get('price'),
                        sid=sid
                    )
                    # Capabilities filter
                    caps = entry.get('capabilities', {})
                    if all(cap.upper() in caps and caps[cap.upper()] for cap in capabilities):
                        results.append(rec)
                        new_count += 1
            # Progress callback
            if progress_callback and new_count:
                progress_callback(new_count)
            # Check empty round
            if new_count == 0:
                empty_rounds += 1
            else:
                empty_rounds = 0
            # Next page
            next_page_uri = data.get('next_page_uri')
            # Wait between calls
            time.sleep(1)
        return results

    def search_advanced(self, number_type=None, locality=None, price_min=None, price_max=None):
        # Simple reuse of search_batch with broad parameters
        return self.search_batch(
            country='US',  # or parameterize as needed
            number_type=number_type or 'local',
            capabilities=[],
            pattern=None,
            locality=locality,
            progress_callback=None
        )