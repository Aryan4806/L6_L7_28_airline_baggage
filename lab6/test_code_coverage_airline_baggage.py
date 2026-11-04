"""Line-coverage suite for airline_baggage.py.

Run from this directory:
    coverage erase
    coverage run --source=airline_baggage -m pytest -q test_code_coverage_airline_baggage.py
    coverage report -m
"""
import pytest
from airline_baggage import baggage_fee, carry_on_ok, check_in_status

@pytest.mark.parametrize("cabin,weight,route,member,expected", [
    ("economy", 10, "domestic", False, 0),
    ("economy", 20, "domestic", False, 100),
    ("premium", 30, "international", False, 225),
    ("business", 50, "international", True, 450),
    ("economy", 30, "domestic", True, 100),
    ("economy", 36, "international", False, 2100),
])
def test_baggage_fee_representative_paths(cabin, weight, route, member, expected):
    assert baggage_fee(cabin, weight, route, member) == expected

@pytest.mark.parametrize("cabin", ["first", "", None])
def test_baggage_fee_rejects_unknown_cabin(cabin):
    with pytest.raises(ValueError, match="unknown cabin"):
        baggage_fee(cabin, 10, "domestic", False)

def test_baggage_fee_rejects_negative_weight():
    with pytest.raises(ValueError, match="invalid weight"):
        baggage_fee("economy", -0.1, "domestic", False)

@pytest.mark.parametrize("weight,items,infant,expected", [
    (5, 1, False, True), (8, 1, False, False), (5, 2, False, False),
    (8, 2, True, True), (8, 3, True, False),
])
def test_carry_on_representative_paths(weight, items, infant, expected):
    assert carry_on_ok(weight, items, infant) is expected

@pytest.mark.parametrize("minutes,baggage,international,expected", [
    (60, True, False, "open"), (50, True, False, "late"),
    (44, True, False, "closed"), (105, False, True, "open"),
    (95, False, True, "late"), (89, False, True, "closed"),
])
def test_check_in_status_representative_paths(minutes, baggage, international, expected):
    assert check_in_status(minutes, baggage, international) == expected
