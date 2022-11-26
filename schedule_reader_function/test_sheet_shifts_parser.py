import pytest
from test_proddata import test_shifts_flat_data
from sheet_shifts_parser import SheetShiftsParser


def test_parser():
    parser = SheetShiftsParser()
    parsed = parser.parse(test_shifts_flat_data)
    print(parsed)


if __name__ == "__main__":
    pytest.main(["-s"])
