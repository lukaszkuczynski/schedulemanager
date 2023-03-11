from google.cloud import datastore
import json
from datetime import datetime, timedelta
from icalendar import vCalAddress, vText, Calendar, Event
from schedule_function_common import get_required_env_var
from google.cloud import storage
import hashlib


datastore_client = datastore.Client()
storage_client = storage.Client()

EVENT_NAME = "Scheduled Shift [automated]"
INPUT_DATETIME_FORMAT = "%Y-%m-%d %H:%M"
ORGANIZER_EMAIL = "ORGANIZERR@EMAIL.COM"
ICS_STORAGE_BUCKET = get_required_env_var("ICS_STORAGE_BUCKET")


class ShiftSaver:
    def _get_month(self):
        return "202303"  # TODO externalize, this is part of the key

    def save_shifts(self, shifts_from_message):
        usermonth_entries = []
        for user_data in shifts_from_message:
            username = user_data["name"]
            email = user_data["email"]
            shifts = user_data["shifts_no_format"]
            extended_key = f"{username}_{self._get_month()}"
            user_month = datastore.Entity(
                datastore_client.key("schedulemanager_usershift", extended_key)
            )
            created_ics_filenames = self._create_ics_based_on_shifts(
                username, email, shifts
            )
            user_month.update(
                {
                    "username": username,
                    "email": email,
                    "shifts": shifts,
                    "ics": created_ics_filenames,
                }
            )
            usermonth_entries.append(user_month)
        resp = datastore_client.put_multi(usermonth_entries)
        print(resp)

    def _create_ics_based_on_shifts(self, name, email, shifts):
        dts = [datetime.strptime(dt, INPUT_DATETIME_FORMAT) for dt in shifts]
        created_files_keys = []
        for shift_datehour in dts:
            ics_text = self._create_ics(name, email, shift_datehour)
            bucket = storage_client.bucket(ICS_STORAGE_BUCKET)
            blob_name = hashlib.md5(
                str(shift_datehour.isoformat() + name).encode()
            ).hexdigest()
            blob_fullname = f"{blob_name}.ics"
            blob = bucket.blob(blob_fullname)
            with blob.open("wb") as f:
                f.write(ics_text)
            created_files_keys.append(blob_fullname)
        return created_files_keys

    def _create_ics(self, name, email, shift_datehour_dt):
        ical = None
        try:
            cal = Calendar()
            cal.add("prodid", "-//My calendar product//mxm.dk//")
            cal.add("version", "2.0")

            organizer_email = ORGANIZER_EMAIL
            organizer = vCalAddress("MAITO:%s" % organizer_email)
            organizer.params["cn"] = vText(organizer_email)
            event = Event()
            event.add("summary", f"{EVENT_NAME} : {name}")

            dt_shift_start = shift_datehour_dt
            dt_shift_end = shift_datehour_dt + timedelta(hours=1)
            event.add("dtstart", dt_shift_start)
            event.add("dtend", dt_shift_end)
            event["organizer"] = organizer

            attendee = vCalAddress("MAILTO:%s" % email)
            event.add("attendee", attendee)

            cal.add_component(event)
            ical = cal.to_ical()
        except Exception as e:
            print("ERROR!!" + e)
        finally:
            return ical


if __name__ == "__main__":
    saver = ShiftSaver()
    with open("sample_message.json") as f:
        shift_data = json.load(f)["data"]["message"]
        saver.save_shifts(shift_data)

