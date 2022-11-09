from abc import abstractmethod


class DetectionStrategy:
    @abstractmethod
    def is_entry_a_hole(self, entry):
        pass


class QuestionMarksStrategy(DetectionStrategy):
    def is_entry_a_hole(self, entry):
        parsed_entry = entry.split("__")
        if len(parsed_entry) < 2:
            raise Exception(
                f"Entry should be __ separated txt, f.e. '2022-10-11 16:00__janek', got '{entry}'"
            )
        return parsed_entry[1] == "???"


class HoleDetector:
    def __init__(self, strategy) -> None:
        self.strategy = strategy

    def detect_holes(self, entries):
        holes = [entry for entry in entries if self.strategy.is_entry_a_hole(entry)]
        return holes

