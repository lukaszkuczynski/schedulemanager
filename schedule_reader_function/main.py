import os
from datetime import datetime
from datetime import datetime
import time
import json
from googleapiclient.discovery import build
import google.auth
from google.cloud import pubsub_v1
import functions_framework
from sheet_shifts_parser import SheetShiftsParser
import base64

publisher = pubsub_v1.PublisherClient()
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
MANAGER_TOPIC_NAME = os.getenv("MANAGER_TOPIC_NAME")
THIS_FUNCTION_CALLER_ID = "schedule_reader"  # envvar it!
DEFAULT_FLOW = "SEND_TO_RECIPIENTS"


def parse_the_response(event):
    print(f"Received event with ID: {event['id']} and data {event.data}")
    data_parsed = json.loads(base64.b64decode(event.data["message"]["data"]).decode())
    print(data_parsed)
    data = data_parsed.get("data")
    message = data.get("message")
    caller = data.get("caller")
    flow = data.get("flow")
    return caller, message, flow


@functions_framework.cloud_event
def entrypoint(reader_event):
    # caller, message, flow = parse_the_response(reader_event)
    parser = SheetShiftsParser()
    credentials, project_id = google.auth.default(
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )
    service = build("sheets", "v4", credentials=credentials)
    spreadsheet_id = os.getenv("SPREADSHEET_ID")
    sheet_range = os.getenv("SHEET_RANGE")
    sheet = service.spreadsheets()
    range_str = sheet_range
    print(f"Getting range {range_str}")
    result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_str).execute()
    values_all = result.get("values", [])
    print(values_all)
    parsed = parser.parse(values_all)
    print(parsed)
    call_the_manager(DEFAULT_FLOW, parsed)
    return str(len(parsed))


def call_the_manager(flow, response):
    topic_path = publisher.topic_path(PROJECT_ID, MANAGER_TOPIC_NAME)
    message_json = json.dumps(
        {"data": {"message": response, "caller": THIS_FUNCTION_CALLER_ID, "flow": flow}}
    )
    message_bytes = message_json.encode("utf-8")
    try:
        publish_future = publisher.publish(topic_path, data=message_bytes)
        publish_future.result()  # Verify the publish succeeded
        return "Message published."
    except Exception as e:
        print(e)
        return (e, 500)
