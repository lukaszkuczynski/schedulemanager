from sched import scheduler
import functions_framework
from google.cloud import pubsub_v1
import os
import json

# Instantiates a Pub/Sub client
publisher = pubsub_v1.PublisherClient()
PROJECT_ID = os.getenv('GOOGLE_CLOUD_PROJECT')
HOLEFINDER_TOPIC_NAME = os.getenv("HOLEFINDER_TOPIC_NAME")

@functions_framework.cloud_event
def entrypoint(manager_event):
   # route according to the request
   # call reader, holefinder, or sender
   print(f"Received event with ID: {manager_event['id']} and data {manager_event.data}")
   schedule = [
      {"date":"2022-01-01", "person":"Adam"},
      {"date":"2022-01-01", "person":"John"}
   ]
   call_hole_finder(schedule)


def call_hole_finder(schedule):
    topic_path = publisher.topic_path(PROJECT_ID, HOLEFINDER_TOPIC_NAME)
    message_json = json.dumps({
        'data': {'message': schedule},
    })
    message_bytes = message_json.encode('utf-8')
    # Publishes a message
    try:
        publish_future = publisher.publish(topic_path, data=message_bytes)
        publish_future.result()  # Verify the publish succeeded
        return 'Message published.'
    except Exception as e:
        print(e)
        return (e, 500)