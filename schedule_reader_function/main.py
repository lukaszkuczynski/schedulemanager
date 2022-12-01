import os
from googleapiclient.discovery import build
import google.auth
import functions_framework
from sheet_shifts_parser import SheetShiftsParser
from schedule_function_common import get_required_env_var, CommsHelper

PROJECT_ID = get_required_env_var("GOOGLE_CLOUD_PROJECT")
MANAGER_TOPIC_NAME = get_required_env_var("MANAGER_TOPIC_NAME")
THIS_FUNCTION_CALLER_ID = "schedule_reader"  # envvar it!
DEFAULT_FLOW = "SEND_TO_RECIPIENTS"


@functions_framework.cloud_event
def entrypoint(reader_event):
    comms = CommsHelper(PROJECT_ID, THIS_FUNCTION_CALLER_ID, MANAGER_TOPIC_NAME)
    caller, message, flow = comms.parse_the_response(reader_event)
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
    res = comms.call_the_manager(flow, parsed)
    return str(res)

