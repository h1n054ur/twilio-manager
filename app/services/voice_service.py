from app.gateways.twilio_gateway import TwilioGateway

class VoiceService:
    def __init__(self):
        self.twilio = TwilioGateway()

    def make_call(self, from_, to):
        return self.twilio.make_call(from_, to)