from contacts_helper import EnvVarContactsHelper, MessageDesigner
import os
import random, string
import json


def randomword(length):
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(length))


def string_from_contact_data(contact_dict):
    contacts_string = json.dumps(contact_dict).replace(" ", "")
    return contacts_string


shifts_data = [
    "2020-10-08 10:00__John",
    "2020-10-10 10:00__John",
    "2020-10-10 11:00__Mark",
    "2020-10-10 12:00__John",
    "2020-10-10 13:00__Frank",
    "2020-10-10 09:00__John",
]

contact_data = {"John": "+48100100|john@a.pl", "Mark": "+48200200|mark@a.pl"}


def test_helper_should_match():
    tmp_name = randomword(20)
    os.environ[tmp_name] = string_from_contact_data(contact_data)
    helper = EnvVarContactsHelper(tmp_name)
    merged = helper.merge_shifts(shifts_data)
    del os.environ[tmp_name]
    assert merged[0]["phone_no"] == "+48100100"
    assert merged[2]["phone_no"] == "+48200200"
    assert merged[4]["phone_no"] is None


def test_helper_should_match_emails():
    tmp_name = randomword(20)
    os.environ[tmp_name] = string_from_contact_data(contact_data)
    helper = EnvVarContactsHelper(tmp_name)
    merged = helper.merge_shifts(shifts_data)
    del os.environ[tmp_name]
    assert merged[0]["email"] == "john@a.pl"
    assert merged[2]["email"] == "mark@a.pl"
    assert merged[4]["email"] is None


def test_helper_should_compact_with_phone():
    tmp_name = randomword(20)
    os.environ[tmp_name] = string_from_contact_data(contact_data)
    helper = EnvVarContactsHelper(tmp_name)
    compacted_dict = helper.compact_shifts(shifts_data)
    assert len(compacted_dict) == 3
    first_compact = compacted_dict[0]
    assert first_compact["phone_no"] == "+48100100"
    del os.environ[tmp_name]


def test_helper_should_compact_with_email():
    tmp_name = randomword(20)
    os.environ[tmp_name] = string_from_contact_data(contact_data)
    helper = EnvVarContactsHelper(tmp_name)
    compacted_dict = helper.compact_shifts(shifts_data)
    print(json.dumps(compacted_dict))
    assert len(compacted_dict) == 3
    assert compacted_dict[0]["name"] == "John"
    assert compacted_dict[0]["email"] == "john@a.pl"
    del os.environ[tmp_name]


def name_dict_from_compacted_list(compacted_dict):
    return {el["name"]: el for el in compacted_dict}


def test_compact_should_have_times_sorted_asc():
    tmp_name = randomword(20)
    os.environ[tmp_name] = string_from_contact_data(contact_data)
    helper = EnvVarContactsHelper(tmp_name)
    compacted_dict = helper.compact_shifts(shifts_data)
    name_dict = name_dict_from_compacted_list(compacted_dict)
    johns_shifts = name_dict["John"]["shifts"]
    assert johns_shifts[0] == "[Thu] Oct 08, 10 AM"
    assert johns_shifts[1] == "[Sat] Oct 10, 09 AM"
    assert johns_shifts[2] == "[Sat] Oct 10, 10 AM"
    assert johns_shifts[3] == "[Sat] Oct 10, 12 PM"
    del os.environ[tmp_name]


def test_filter_compact_by_number_by_assigned_and_not():
    tmp_name = randomword(20)
    os.environ[tmp_name] = string_from_contact_data(contact_data)
    helper = EnvVarContactsHelper(tmp_name)
    compacted_dict = helper.compact_shifts(shifts_data)
    assigned, unassigned = helper.filter_compact_by_number_by_assigned_and_not(
        compacted_dict
    )
    assert len(assigned) == 2
    assert len(unassigned) == 1
    del os.environ[tmp_name]


chosen_hole_data = ["2020-10-08 10:00", "2020-10-10 10:00"]


def test_hole_notifications_are_created():
    tmp_name = randomword(20)
    os.environ[tmp_name] = string_from_contact_data(contact_data)
    helper = EnvVarContactsHelper(tmp_name)
    notifys = helper.make_hole_notifications(chosen_hole_data, ["John", "John"])
    assert len(notifys) == 2
    del os.environ[tmp_name]


def test_hole_messages_are_created():
    tmp_name = randomword(20)
    os.environ[tmp_name] = string_from_contact_data(contact_data)
    helper = EnvVarContactsHelper(tmp_name)
    messageDesigner = MessageDesigner()
    notifys = helper.make_hole_notifications(chosen_hole_data, ["John", "Mark"])
    msg2 = messageDesigner.get_message_for_hole(notifys[1], 7)
    assert msg2 is not None
    del os.environ[tmp_name]


def test_hole_notifications_are_created_when_user_not_found():
    tmp_name = randomword(20)
    os.environ[tmp_name] = string_from_contact_data(contact_data)
    helper = EnvVarContactsHelper(tmp_name)
    notifys = helper.make_hole_notifications(chosen_hole_data, ["Joh", "John"])
    assigned, unassigned = helper.filter_compact_by_number_by_assigned_and_not(notifys)
    assert len(assigned) == 1
    assert len(unassigned) == 1
    del os.environ[tmp_name]
