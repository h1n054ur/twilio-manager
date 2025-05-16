from app.gateways.twilio_gateway import TwilioGateway
from app.gateways.http_gateway import HttpGateway

class NumberService:
    def __init__(self):
        self.twilio = TwilioGateway()
        self.http = HttpGateway()

    def list_number_types(self, country):
        return self.http.get_number_types(country)

    def search_available(self, country, number_type, search_mode, pattern, locality, capabilities, progress_callback):
        return self.http.search_batch(country, number_type, capabilities, pattern, locality, progress_callback)

    def purchase_numbers(self, sids):
        results = []
        for sid in sids:
            try:
                self.twilio.purchase_number(sid)
                results.append(True)
            except Exception:
                results.append(False)
        return results

    def list_active_numbers(self):
        return self.twilio.list_numbers()

    def release_number(self, sid):
        return self.twilio.release_number(sid)

    def update_number_config(self, sid, cfg):
        return self.twilio.update_number_config(sid, cfg)

    def search_advanced(self, number_type=None, locality=None, price_min=None, price_max=None):
        return self.http.search_advanced(number_type, locality, price_min, price_max)