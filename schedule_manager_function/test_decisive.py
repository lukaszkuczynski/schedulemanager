from decisive import Decisive
import mock
from datetime import datetime


def test_decisive_should_select():
    with mock.patch.object(Decisive, "current_datetime") as current_datetime_mocked:
        current_datetime_mocked.return_value = datetime(2022, 10, 10, 1, 1)
        decisive = Decisive(3)
        hole_msg = [
            "2022-10-11 17:00__???",
            "2022-10-11 18:00__???",
            "2022-10-22 15:00__???",
        ]
        notify_holes = decisive.holes_to_notify(hole_msg)
        print(notify_holes)
        assert len(notify_holes) == 2


def test_decisive_should_select2():
    with mock.patch.object(Decisive, "current_datetime") as current_datetime_mocked:
        current_datetime_mocked.return_value = datetime(2022, 10, 10, 1, 1)
        decisive = Decisive(3)
        hole_msg = [
            "2022-10-09 17:00__???",
            "2022-10-09 18:00__???",
            "2022-10-13 15:00__???",
        ]
        notify_holes = decisive.holes_to_notify(hole_msg)
        assert len(notify_holes) == 0

