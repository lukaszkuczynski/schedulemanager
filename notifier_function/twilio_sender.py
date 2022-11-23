from twilio.rest import Client
import os


class TwilioSender:
    def __init__(self) -> None:
        account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.notifier_from = os.getenv("NOTIFIER_FROM")
        self.notifier_to = os.getenv("NOTIFIER_TO")
        self.client = Client(account_sid, auth_token)

    def send_message_to(self, msg, to_number):
        number_with_channel = f"whatsapp:{to_number}"
        message = self.client.messages.create(
            from_=self.notifier_from, body=msg, to=number_with_channel
        )
        return message


if __name__ == "__main__":
    sender = TwilioSender()
    msg = sender.send_message(
        """
        Your package has been shipped. It will be delivered in zcxczczxczx business days.
        """
    )
    print(msg)
