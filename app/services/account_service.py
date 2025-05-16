from app.gateways.twilio_gateway import TwilioGateway

class AccountService:
    def __init__(self):
        self.twilio = TwilioGateway()

    def get_usage(self):
        return self.twilio.get_usage()

    def get_billing(self):
        return self.twilio.get_billing()

    def list_api_keys(self):
        return self.twilio.list_api_keys()

    def create_api_key(self, friendly_name):
        return self.twilio.create_api_key(friendly_name)

    def delete_api_key(self, sid):
        return self.twilio.delete_api_key(sid)

    def list_webhooks(self):
        return self.twilio.list_webhooks()

    def toggle_sandbox(self):
        return self.twilio.toggle_sandbox()

    def generate_test_credentials(self):
        return self.twilio.generate_test_credentials()

    def list_subaccounts(self):
        return self.twilio.list_subaccounts()

    def create_subaccount(self, friendly_name):
        return self.twilio.create_subaccount(friendly_name)

    def switch_subaccount(self, sid):
        return self.twilio.switch_subaccount(sid)

    def list_ip_acls(self):
        return self.twilio.list_ip_acls()

    def add_ip_acl(self, ip_address):
        return self.twilio.add_ip_acl(ip_address)

    def remove_ip_acl(self, ip_address):
        return self.twilio.remove_ip_acl(ip_address)

