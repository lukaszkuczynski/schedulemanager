import functions_framework
import os

from schedule_function_common import get_required_env_var, CommsHelper
from shift_saver import ShiftSaver

PROJECT_ID = get_required_env_var("GOOGLE_CLOUD_PROJECT")
MANAGER_TOPIC_NAME = get_required_env_var("MANAGER_TOPIC_NAME")
THIS_FUNCTION_CALLER_ID = "shift_recorder"  # envvar it!


shift_saver = ShiftSaver()


@functions_framework.cloud_event
def entrypoint(notifier_event):
    comms = CommsHelper(PROJECT_ID, THIS_FUNCTION_CALLER_ID, MANAGER_TOPIC_NAME)
    caller, message, flow = comms.parse_the_response(notifier_event)
    save_result = shift_saver.save_shifts(message)
    result = comms.call_the_manager(flow, save_result=shift_saver.save_shifts(message))
    return result


def dry_run_send(msg_text, whatsapp_no):
    print(f"Dry run send! Sending txt: {msg_text} to whatsapp_no {whatsapp_no}")

