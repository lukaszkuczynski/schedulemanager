from contacts_helper import EnvVarContactsHelper
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
    "2020-10-10 10:00__John",
    "2020-10-10 11:00__Mark",
    "2020-10-10 12:00__John",
    "2020-10-10 13:00__Frank",
]

contact_data = {"John": "+48100100", "Mark": "+48200200"}


def test_helper_should_match():
    tmp_name = randomword(20)
    os.environ[tmp_name] = string_from_contact_data(contact_data)
    helper = EnvVarContactsHelper(tmp_name)
    merged = helper.merge_shifts(shifts_data)
    del os.environ[tmp_name]
    assert merged[0]["phone_no"] == "+48100100"
    assert merged[1]["phone_no"] == "+48200200"
    assert merged[2]["phone_no"] == "+48100100"
    assert merged[3]["phone_no"] is None


def test_helper_should_compact():
    tmp_name = randomword(20)
    os.environ[tmp_name] = string_from_contact_data(contact_data)
    helper = EnvVarContactsHelper(tmp_name)
    compacted_dict = helper.compact_shifts(shifts_data)
    print(compacted_dict)
    assert len(compacted_dict) == 3
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
