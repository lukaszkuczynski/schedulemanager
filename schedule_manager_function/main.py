import functions_framework
from google.cloud import pubsub_v1
import os
import json
import base64

# Instantiates a Pub/Sub client
publisher = pubsub_v1.PublisherClient()
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
HOLEFINDER_TOPIC_NAME = os.getenv("HOLEFINDER_TOPIC_NAME")
NOTIFIER_TOPIC_NAME = os.getenv("NOTIFIER_TOPIC_NAME")
THIS_FUNCTION_CALLER_ID = "schedule_manager"  # envvar it!


def process_acc_to_the_caller(caller, event_data):
    response = event_data
    return response


def send_to_topic(topic_name, response):
    topic_path = publisher.topic_path(PROJECT_ID, topic_name)
    message_json = json.dumps(
        {
            "data": {"message": response, "caller": THIS_FUNCTION_CALLER_ID},
        }
    )
    message_bytes = message_json.encode("utf-8")
    try:
        publish_future = publisher.publish(topic_path, data=message_bytes)
        publish_result = publish_future.result()  # Verify the publish succeeded
        print(publish_result)
        return "Message published."
    except Exception as e:
        print(e)
        return (e, 500)


def parse_the_response(event):
    print(f"Received event with ID: {event['id']} and data {event.data}")
    data_parsed = json.loads(base64.b64decode(event.data["message"]["data"]).decode())
    print(data_parsed)
    data = data_parsed.get("data")
    message = data.get("message")
    caller = data.get("caller")
    return caller, message


@functions_framework.cloud_event
def entrypoint(manager_event):
    caller, message = parse_the_response(manager_event)
    if caller == "schedule_reader":
        response = process_acc_to_the_caller(caller, message)
        send_to_topic(HOLEFINDER_TOPIC_NAME, response)
    elif caller == "hole_finder":
        response = process_acc_to_the_caller(caller, message)
        send_to_topic(NOTIFIER_TOPIC_NAME, response)
