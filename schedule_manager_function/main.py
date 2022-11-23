import functions_framework
from google.cloud import pubsub_v1
import os
import json
import base64
from decisive import Decisive
from contacts_helper import EnvVarContactsHelper, MessageDesigner

# Instantiates a Pub/Sub client
publisher = pubsub_v1.PublisherClient()
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
HOLEFINDER_TOPIC_NAME = os.getenv("HOLEFINDER_TOPIC_NAME")
NOTIFIER_TOPIC_NAME = os.getenv("NOTIFIER_TOPIC_NAME")
THIS_FUNCTION_CALLER_ID = "schedule_manager"  # envvar it!
DAYS_AHEAD_CHECK = int(os.getenv("DAYS_AHEAD_CHECK"))
# TODO: move it to some nosql ?
CONTACT_DATA = os.getenv("CONTACT_DATA")
contacts_helper = EnvVarContactsHelper("CONTACT_DATA")
message_designer = MessageDesigner()


def merge_shifts_with_contact_data(event_data, contacts):
    print(event_data)
    for event in event_data:
        event["recipient"] = contacts.get(event)


def log_unreacheable_recipients(shifts_enriched):
    print(shifts_enriched)


def process_acc_to_the_caller(flow, caller, event_data):
    if flow is None:
        if caller == "hole_finder":
            decisive = Decisive(DAYS_AHEAD_CHECK)
            holes_to_notify = decisive.holes_to_notify(event_data)
            print(f"From this list {event_data} chosen {holes_to_notify} to notify")
            response = holes_to_notify
        else:
            response = event_data
        return response
    elif flow == "SEND_TO_RECIPIENTS":
        if caller == "schedule_reader":
            shifts_compacted = contacts_helper.compact_shifts(event_data)
            (
                assigned,
                unassigned,
            ) = contacts_helper.filter_compact_by_number_by_assigned_and_not(
                shifts_compacted
            )
            log_unreacheable_recipients(unassigned)
            all_notifications = [
                message_designer.get_message_for_shift_data(shift) for shift in assigned
            ]
            return all_notifications


def send_to_topic(topic_name, response):
    topic_path = publisher.topic_path(PROJECT_ID, topic_name)
    message_json = json.dumps(
        {"data": {"message": response, "caller": THIS_FUNCTION_CALLER_ID},}
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
    flow = data.get("flow")
    return caller, message, flow


def log_the_flow_end(flow, response):
    print(f"The flow '{flow}' has ended")


@functions_framework.cloud_event
def entrypoint(manager_event):
    caller, message, flow = parse_the_response(manager_event)
    if flow is None:
        if caller == "schedule_reader":
            response = process_acc_to_the_caller(flow, caller, message)
            send_to_topic(HOLEFINDER_TOPIC_NAME, response)
        elif caller == "hole_finder":
            response = process_acc_to_the_caller(flow, caller, message)
            send_to_topic(NOTIFIER_TOPIC_NAME, response)
        else:
            print(f"no caller identified : {caller}")
    elif flow == "SEND_TO_RECIPIENTS":
        if caller == "schedule_reader":
            response = process_acc_to_the_caller(flow, caller, message)
            send_to_topic(NOTIFIER_TOPIC_NAME, response)
        elif caller == "notifier":
            response = process_acc_to_the_caller(flow, caller, message)
            log_the_flow_end(flow, response)
