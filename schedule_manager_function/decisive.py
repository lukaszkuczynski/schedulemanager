from datetime import datetime, timedelta


class Decisive:
    def __init__(self, days_ahead) -> None:
        self.days_ahead = days_ahead

    def current_datetime(self):
        return datetime.now()

    def holes_to_notify(self, hole_message):
        holes = [
            datetime.strptime(hole.split("_")[0], "%Y-%m-%d %H:%M")
            for hole in hole_message
        ]
        start_period = self.current_datetime()
        end_period = start_period + timedelta(days=self.days_ahead)
        print(f"Searching for holes within the period {start_period} - {end_period}")
        holes_within = [
            hole.strftime("%Y-%m-%d %H:%M")
            for hole in holes
            if end_period > hole > start_period
        ]
        return holes_within
