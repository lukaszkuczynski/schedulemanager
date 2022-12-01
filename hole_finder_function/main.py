import functions_framework
import os
from hole_detector import HoleDetector, QuestionMarksStrategy

from schedule_function_common import get_required_env_var, CommsHelper

PROJECT_ID = get_required_env_var("GOOGLE_CLOUD_PROJECT")
MANAGER_TOPIC_NAME = get_required_env_var("MANAGER_TOPIC_NAME")
THIS_FUNCTION_CALLER_ID = "hole_finder"  # envvar it!


@functions_framework.cloud_event
def entrypoint(holefinder_event):
    comms = CommsHelper(PROJECT_ID, THIS_FUNCTION_CALLER_ID, MANAGER_TOPIC_NAME)
    caller, message, flow = comms.parse_the_response(holefinder_event)
    holes = HoleDetector(QuestionMarksStrategy()).detect_holes(message)
    comms.call_the_manager(flow, holes)

