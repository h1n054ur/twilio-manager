"""Adapter for Twilio SDK"""
import os
import time
from twilio.rest import Client
from .config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN

def get_client() -> Client:
    return Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

class TwilioGateway:
    def __init__(self):
        self.client = get_client()

    def list_numbers(self, filters=None):
        return self.client.incoming_phone_numbers.list(**(filters or {}))

    def purchase_number(self, sid):
        return self.client.incoming_phone_numbers(sid).update()

    def release_number(self, sid):
        return self.client.incoming_phone_numbers(sid).delete()

    def update_number_config(self, sid, cfg):
        return self.client.incoming_phone_numbers(sid).update(**cfg)

    def make_call(self, from_, to):
        return self.client.calls.create(from_=from_, to=to, url="")

    def send_sms(self, from_, to, body):
        return self.client.messages.create(from_=from_, to=to, body=body)

    def list_logs(self, log_type, sid):
        if log_type == 'sms':
            return self.client.messages.list(to=sid)
        elif log_type == 'call':
            return self.client.calls.list(to=sid)
        else:
            return []

    def list_events(self, event_type):
        # stub for diagnostics
        return []

    def get_usage(self):
        return self.client.usage.records.today.list()

    def get_billing(self):
        # stub for billing data
        return {}

    def list_api_keys(self):
        return self.client.new_keys.list()

    def create_api_key(self, friendly_name):
        return self.client.new_keys.create(friendly_name=friendly_name)

    def delete_api_key(self, sid):
        return self.client.new_keys(sid).delete()

    def list_webhooks(self):
        return []

    def toggle_sandbox(self):
        # stub toggling
        return True

    def generate_test_credentials(self):
        return {}

    def list_subaccounts(self):
        return self.client.api.accounts.list()

    def create_subaccount(self, friendly_name):
        return self.client.api.accounts.create(friendly_name=friendly_name)

    def switch_subaccount(self, sid):
        # stub: re-init client for new account
        global TWILIO_ACCOUNT_SID
        TWILIO_ACCOUNT_SID = sid
        self.client = get_client()
        return True

    def list_templates(self):
        return []

    def apply_template(self, template_sid, number_sids):
        return {sid: True for sid in number_sids}

    def remove_template(self, template_sid):
        return True

    def export_audit(self):
        return []

    def list_ip_acls(self):
        return []

    def add_ip_acl(self, ip_address):
        return True

    def remove_ip_acl(self, ip_address):
        return True