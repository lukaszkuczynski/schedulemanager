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


@functions_framework.cloud_event
def entrypoint(nofifier_event):
    sender = TwilioSender()
    print(
        f"Received event with ID: {nofifier_event['id']} and data {nofifier_event.data}"
    )
    print("decoding")
    decoded = base64.b64decode(nofifier_event.data["message"]["data"]).decode()
    print("Hello, " + decoded + "!")
    print(decoded)
    events = json.loads(decoded)["data"]["message"]
    print(f"events: {events}")
    msg = design_msg(events)
    print(f"will send this msg : {msg}")
    sender.send_message(msg)
    # call_the_manager(send_notifications())


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


def design_msg(holes):
    shifts_txt = ",".join(holes)
    message_text = f"""
        There are following days where shifts are free. {shifts_txt}
    """
    return message_text


def send_notifications():
    result = "OK"
    return result
