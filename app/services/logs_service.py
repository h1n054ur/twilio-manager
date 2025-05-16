from app.gateways.twilio_gateway import TwilioGateway

class LogsService:
    def __init__(self):
        self.twilio = TwilioGateway()

    def list_logs(self, log_type, sid):
        return self.twilio.list_logs(log_type, sid)

    def list_events(self, event_type):
        return self.twilio.list_events(event_type)