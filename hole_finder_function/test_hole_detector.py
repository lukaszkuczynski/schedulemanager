from hole_detector import HoleDetector, QuestionMarksStrategy


def test_strategy_for_a_hole():
    single_hole = "2022-10-11 16:00__???"
    strategy = QuestionMarksStrategy()
    assert strategy.is_entry_a_hole(single_hole) == True


def test_strategy_for_a_non_hole():
    single_hole = "2022-10-11 16:00__?zz"
    strategy = QuestionMarksStrategy()
    assert strategy.is_entry_a_hole(single_hole) == False


def test_detector_using_strategy_without_holes():
    entries = [
        "2022-10-11 16:00__janek",
        "2022-10-11 16:00__franek",
        "2022-10-11 17:00__aa",
    ]
    detector = HoleDetector(QuestionMarksStrategy())
    holes = detector.detect_holes(entries)
    assert len(holes) == 0


def test_detector_using_strategy_on_holes():
    entries = [
        "2022-10-11 16:00__janek",
        "2022-10-11 16:00__franek",
        "2022-10-11 17:00__???",
    ]
    detector = HoleDetector(QuestionMarksStrategy())
    holes = detector.detect_holes(entries)
    assert len(holes) == 1


def test_detector_using_strategy_2():
    message = [
        "2022-10-11 16:00__janek",
        "2022-10-11 16:00__franek",
        "2022-10-11 17:00__aa",
        "2022-10-18 16:00__zbigniew",
        "2022-10-18 17:00__franciszek",
        "2022-10-15 13:00__bula1",
        "2022-10-15 13:00__mula1",
        "2022-10-22 13:00__jola",
        "2022-10-22 13:00__kola",
        "2022-10-22 14:00__mola",
        "2022-10-22 14:00__sola",
    ]
    detector = HoleDetector(QuestionMarksStrategy())
    holes = detector.detect_holes(message)
    assert len(holes) == 0

