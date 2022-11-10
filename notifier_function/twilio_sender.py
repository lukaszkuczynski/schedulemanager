from twilio.rest import Client
import os


class TwilioSender:
    def __init__(self) -> None:
        account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.notifier_from = os.getenv("NOTIFIER_FROM")
        self.notifier_to = os.getenv("NOTIFIER_TO")
        self.client = Client(account_sid, auth_token)

    def send_message(self, msg):
        message = self.client.messages.create(
            from_=self.notifier_from, body=msg, to=self.notifier_to
        )
        return message.sid

