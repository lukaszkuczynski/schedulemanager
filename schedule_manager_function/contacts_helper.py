import os
import json
from collections import defaultdict


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

    def compact_shifts(self, shifts):
        enriched = self.merge_shifts(shifts)
        compact_dict = defaultdict(list)
        for shift in enriched:
            compact_dict[shift["name"]].append(shift["shift_datetime"])
        compact_dict_with_numbers = []
        for key, value in compact_dict.items():
            compact_dict_with_numbers.append(
                {
                    "name": key,
                    "phone_no": self.contact_data.get(key, ""),
                    "shifts": value,
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


class MessageDesigner:
    def get_message_for_shift_data(self, shift_data):
        dates_string = ",".join(shift_data["shifts"])
        message_text = f"""hello dear Participant {shift_data["name"]},
this is the list of your shifts from the upcoming schedule {dates_string}.
Please verify with the main program and add to your calendar.
Enjoy!
"""
        return {"whatsapp_no": shift_data["phone_no"], "message_text": message_text}

