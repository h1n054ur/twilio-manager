from app.gateways.twilio_gateway import TwilioGateway

class MessagingService:
    def __init__(self):
        self.twilio = TwilioGateway()

    def send_sms(self, from_, to, body):
        return self.twilio.send_sms(from_, to, body)