import os
import json
from collections import defaultdict
from datetime import datetime

INPUT_DATETIME_FORMAT = "%Y-%m-%d %H:%M"
OUTPUT_DATETIME_FORMAT = "[%a] %b %d, %I %p"


class EnvVarContactsHelper:
    def __init__(self, var_name):
        if not var_name in os.environ:
            raise Exception(f"Environment variable '{var_name}' not found.")
        contacts_string = os.getenv(var_name)
        self.contact_data = json.loads(contacts_string)

    def _enrich_shift(self, shift_str, contact_data):
        shift = shift_str.split("__")
        shift_datetime = shift[0]
        name = shift[1]
        phone_no = contact_data.get(name)
        return {"name": name, "shift_datetime": shift_datetime, "phone_no": phone_no}

    def merge_shifts(self, shifts):
        return [self._enrich_shift(shift, self.contact_data) for shift in shifts]

    def _sort_and_format_shifts(self, shifts):
        dt_list = [
            datetime.strptime(shift_time_str, INPUT_DATETIME_FORMAT)
            for shift_time_str in shifts
        ]
        dt_list_sorted = sorted(dt_list)
        return [
            datetime.strftime(dt_shift, OUTPUT_DATETIME_FORMAT)
            for dt_shift in dt_list_sorted
        ]

    def compact_shifts(self, shifts):
        enriched = self.merge_shifts(shifts)
        compact_dict = defaultdict(list)
        for shift in enriched:
            compact_dict[shift["name"]].append(shift["shift_datetime"])
        compact_dict_with_numbers = []
        for key, shifts in compact_dict.items():
            compact_dict_with_numbers.append(
                {
                    "name": key,
                    "phone_no": self.contact_data.get(key, ""),
                    "shifts": self._sort_and_format_shifts(shifts),
                }
            )
        return compact_dict_with_numbers

    def __is_number_assigned(self, phone_no):
        return phone_no is not None and len(phone_no.strip()) > 0

    def filter_compact_by_number_by_assigned_and_not(self, compacted_dict):
        assigned = [
            shift_compact
            for shift_compact in compacted_dict
            if self.__is_number_assigned(shift_compact["phone_no"])
        ]
        unassigned = [
            shift_compact
            for shift_compact in compacted_dict
            if not self.__is_number_assigned(shift_compact["phone_no"])
        ]
        return assigned, unassigned

    def make_hole_notifications(self, hole_data, hole_notified_people):
        hole_notifications = []
        for notify_name in hole_notified_people:
            notify_dict = {
                "name": notify_name,
                "phone_no": self.contact_data.get(notify_name, ""),
                "holes": hole_data,
            }
            hole_notifications.append(notify_dict)
        return hole_notifications


class MessageDesigner:
    def get_message_for_shift_data(self, shift_data):
        dates_string = ", ".join(shift_data["shifts"])
        message_text = f"""hello dear Participant {shift_data["name"]},
this is the list of your shifts from the upcoming schedule {dates_string}.
Please verify with the main program and add to your calendar.
Enjoy!
"""
        return {"whatsapp_no": shift_data["phone_no"], "message_text": message_text}

    def get_message_for_shift_data(self, shift_data):
        dates_string = ", ".join(shift_data["shifts"])
        message_text = f"""hello dear Participant {shift_data["name"]},
this is the list of your shifts from the upcoming schedule {dates_string}.
Please verify with the main program and add to your calendar.
Enjoy!
"""
        return {"whatsapp_no": shift_data["phone_no"], "message_text": message_text}

    def get_message_for_hole(self, hole_data):
        dates_string = ", ".join(hole_data["holes"])
        period = "the following days"
        message_text = f"""Hi {hole_data["name"]},
The following is the list of free shifts you can take for the period of {period}. 
Days and hours are as follows {dates_string}. Please check the main schedule.
"""
        return {"whatsapp_no": hole_data["phone_no"], "message_text": message_text}

    def get_message_for_hole_temp(self, hole_data):
        dates_string = ", ".join(hole_data["holes"])
        name = hole_data["name"]
        message_text = f"""Your package has been shipped. It will be delivered in {name}{dates_string} business days.
"""
        return {"whatsapp_no": hole_data["phone_no"], "message_text": message_text}

