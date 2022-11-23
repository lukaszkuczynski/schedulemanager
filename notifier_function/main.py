import functions_framework
import base64
import os
import json
from google.cloud import pubsub_v1
from twilio_sender import TwilioSender

publisher = pubsub_v1.PublisherClient()
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
MANAGER_TOPIC_NAME = os.getenv("MANAGER_TOPIC_NAME")
THIS_FUNCTION_CALLER_ID = "notifier"  # envvar it!

twilioSender = TwilioSender()


@functions_framework.cloud_event
def entrypoint(nofifier_event):
    print(
        f"Received event with ID: {nofifier_event['id']} and data {nofifier_event.data}"
    )
    print("decoding")
    decoded = base64.b64decode(nofifier_event.data["message"]["data"]).decode()
    print("Hello, " + decoded + "!")
    print(decoded)
    events = json.loads(decoded)["data"]["message"]
    print(f"events: {events}")
    # send_test_message()
    result = send_all_messages(events)
    return result


def call_the_manager(response):
    topic_path = publisher.topic_path(PROJECT_ID, MANAGER_TOPIC_NAME)
    message_json = json.dumps(
        {"data": {"message": response, "caller": THIS_FUNCTION_CALLER_ID},}
    )
    message_bytes = message_json.encode("utf-8")
    try:
        publish_future = publisher.publish(topic_path, data=message_bytes)
        publish_future.result()  # Verify the publish succeeded
        return "Message published."
    except Exception as e:
        print(e)
        return (e, 500)


def send_test_message():
    msg_text = """hello dear Participant 111,
this is the list of your shifts from the upcoming schedule 2222.
Please verify with the main program and add to your calendar.
Enjoy!"""
    whatsapp_no = os.getenv("NOTIFIER_TO")
    msg_response = twilioSender.send_message_to(msg_text, whatsapp_no)
    print(msg_response)


def send_all_messages(messages):
    for msg in messages:
        print(f"will send this msg : {msg}")
        msg_text = msg["message_text"]
        whatsapp_no = msg["whatsapp_no"]
        msg_response = twilioSender.send_message_to(msg_text, whatsapp_no)
        print(msg_response)
    return 0


def design_msg_approved(holes):
    shifts_txt = ",".join(holes)
    message_text = f"""
    Your package has been shipped. It will be delivered in {shifts_txt} business days.
    """
    return message_text


def design_msg(holes):
    shifts_txt = ",".join(holes)
    message_text = f"""
       The following is the list of free shifts you can take for the period of {{1}}. Days and hours: {{2}}
    """
    return message_text


def send_notifications():
    result = "OK"
    return result
