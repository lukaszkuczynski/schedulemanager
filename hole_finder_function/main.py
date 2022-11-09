import functions_framework
import base64
from google.cloud import pubsub_v1
import os
import json
from hole_detector import HoleDetector, QuestionMarksStrategy

publisher = pubsub_v1.PublisherClient()
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
MANAGER_TOPIC_NAME = os.getenv("MANAGER_TOPIC_NAME")
THIS_FUNCTION_CALLER_ID = "hole_finder"  # envvar it!


@functions_framework.cloud_event
def entrypoint(schedule_cloud_event):
    print(
        f"Received event with ID: {schedule_cloud_event['id']} and data {schedule_cloud_event.data}"
    )
    print("decoding")
    decoded_msg = json.loads(
        base64.b64decode(schedule_cloud_event.data["message"]["data"]).decode()
    )
    print("Received this msg:")
    print(decoded_msg)
    decoded_events = decoded_msg["data"]["message"]
    print("and received these events:")
    print(decoded_events)
    holes = HoleDetector(QuestionMarksStrategy()).detect_holes(decoded_events)
    call_the_manager(holes)


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
