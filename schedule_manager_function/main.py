import functions_framework
from decisive import Decisive
from contacts_helper import EnvVarContactsHelper, MessageDesigner
from schedule_function_common import get_required_env_var, CommsHelper

PROJECT_ID = get_required_env_var("GOOGLE_CLOUD_PROJECT")
HOLEFINDER_TOPIC_NAME = get_required_env_var("HOLEFINDER_TOPIC_NAME")
NOTIFIER_TOPIC_NAME = get_required_env_var("NOTIFIER_TOPIC_NAME")
THIS_FUNCTION_CALLER_ID = "schedule_manager"  # envvar it!
DAYS_AHEAD_CHECK = int(get_required_env_var("DAYS_AHEAD_CHECK"))
# TODO: move it to some nosql ?
CONTACT_DATA = get_required_env_var("CONTACT_DATA")
HOLE_NOTIFIED_PEOPLE = get_required_env_var("HOLE_NOTIFIED_PEOPLE")
contacts_helper = EnvVarContactsHelper("CONTACT_DATA")
message_designer = MessageDesigner()


def merge_shifts_with_contact_data(event_data, contacts):
    print(event_data)
    for event in event_data:
        event["recipient"] = contacts.get(event)


def log_unreacheable_recipients(shifts_enriched):
    print("These shifts were not reachable - no phone number found for them")
    print(shifts_enriched)


def process_acc_to_the_caller(flow, caller, event_data):
    if flow == "FIND_HOLES":
        if caller == "hole_finder":
            decisive = Decisive(DAYS_AHEAD_CHECK)
            holes_to_notify = decisive.holes_to_notify(event_data)
            print(f"From this list {event_data} chosen {holes_to_notify} to notify")
            if len(holes_to_notify) == 0:
                print("No holes to notify today...")
                # TODO: think about sth nicer, abort type of msg and send to group of admins
                response = None
            else:
                hole_notified_people = HOLE_NOTIFIED_PEOPLE.split(",")
                # TODO: add alerting validation to filter out not found people names
                hole_notifications = contacts_helper.make_hole_notifications(
                    holes_to_notify, hole_notified_people
                )
                (
                    assigned,
                    unassigned,
                ) = contacts_helper.filter_compact_by_number_by_assigned_and_not(
                    hole_notifications
                )
                log_unreacheable_recipients(unassigned)
                all_notifications = [
                    message_designer.get_message_for_hole(notify, DAYS_AHEAD_CHECK)
                    for notify in assigned
                ]
                response = all_notifications
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


def log_the_flow_end(flow, response):
    print(f"The flow '{flow}' has ended")


@functions_framework.cloud_event
def entrypoint(manager_event):
    comms = CommsHelper(PROJECT_ID, THIS_FUNCTION_CALLER_ID)

    caller, message, flow = comms.parse_the_response(manager_event)
    if flow == "FIND_HOLES":
        if caller == "schedule_reader":
            response = process_acc_to_the_caller(flow, caller, message)
            comms.send_to_topic(HOLEFINDER_TOPIC_NAME, flow, response)
        elif caller == "hole_finder":
            response = process_acc_to_the_caller(flow, caller, message)
            if response:
                comms.send_to_topic(NOTIFIER_TOPIC_NAME, flow, response)
        else:
            print(f"no caller identified : {caller}")
    elif flow == "SEND_TO_RECIPIENTS":
        if caller == "schedule_reader":
            response = process_acc_to_the_caller(flow, caller, message)
            comms.send_to_topic(NOTIFIER_TOPIC_NAME, flow, response)
        elif caller == "notifier":
            response = process_acc_to_the_caller(flow, caller, message)
            log_the_flow_end(flow, response)
