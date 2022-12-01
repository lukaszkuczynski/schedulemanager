import functions_framework
import os
from twilio_sender import TwilioSender

from schedule_function_common import get_required_env_var, CommsHelper

PROJECT_ID = get_required_env_var("GOOGLE_CLOUD_PROJECT")
MANAGER_TOPIC_NAME = get_required_env_var("MANAGER_TOPIC_NAME")
THIS_FUNCTION_CALLER_ID = "notifier"  # envvar it!
DRY_RUN_SEND = int(get_required_env_var("DRY_RUN_SEND", 1))

twilioSender = TwilioSender()


@functions_framework.cloud_event
def entrypoint(notifier_event):
    comms = CommsHelper(PROJECT_ID, THIS_FUNCTION_CALLER_ID, MANAGER_TOPIC_NAME)
    caller, message, flow = comms.parse_the_response(notifier_event)
    send_result = send_all_messages(message)
    result = comms.call_the_manager(flow, send_result)
    return result


def send_test_message():
    msg_text = """hello dear Participant 111,
this is the list of your shifts from the upcoming schedule 2222.
Please verify with the main program and add to your calendar.
Enjoy!"""
    whatsapp_no = get_required_env_var("NOTIFIER_TO")
    msg_response = twilioSender.send_message_to(msg_text, whatsapp_no)
    print(msg_response)


def dry_run_send(msg_text, whatsapp_no):
    print(f"Dry run send! Sending txt: {msg_text} to whatsapp_no {whatsapp_no}")


def send_all_messages(messages):
    for msg in messages:
        print(f"will send this msg : {msg}")
        msg_text = msg["message_text"]
        whatsapp_no = msg["whatsapp_no"]
        if DRY_RUN_SEND == 1:
            dry_run_send(msg_text, whatsapp_no)
        else:
            msg_response = twilioSender.send_message_to(msg_text, whatsapp_no)
            print(msg_response)
    return 0
