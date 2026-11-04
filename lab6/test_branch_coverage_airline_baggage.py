"""Branch-coverage suite for airline_baggage.py.

Run from this directory:
    coverage erase
    coverage run --branch --source=airline_baggage -m pytest -q test_branch_coverage_airline_baggage.py
    coverage report -m
"""
import pytest
from airline_baggage import baggage_fee, carry_on_ok, check_in_status

@pytest.mark.parametrize("cabin", ["economy", "premium", "business"])
def test_all_valid_cabins(cabin):
    assert baggage_fee(cabin, 0, "domestic", False) == 0

@pytest.mark.parametrize("cabin", ["first", "", None])
def test_unknown_cabin_branch(cabin):
    with pytest.raises(ValueError, match="unknown cabin"):
        baggage_fee(cabin, 10, "domestic", False)

@pytest.mark.parametrize("weight", [-1, 0])
def test_negative_weight_decision(weight):
    if weight < 0:
        with pytest.raises(ValueError, match="invalid weight"):
            baggage_fee("economy", weight, "domestic", False)
    else:
        assert baggage_fee("economy", weight, "domestic", False) == 0

@pytest.mark.parametrize("cabin,weight,member", [
    ("economy", 15, False), ("economy", 25, True),
    ("business", 40, True), ("premium", 25, False),
])
def test_member_and_allowance_boundaries(cabin, weight, member):
    assert baggage_fee(cabin, weight, "domestic", member) == 0

@pytest.mark.parametrize("weight,route,expected", [
    (15, "domestic", 0), (16, "domestic", 20),
    (16, "international", 45), (36, "domestic", 840),
    (36, "international", 2100), (35, "international", 900),
    (36, "other", 1890),
])
def test_fee_route_and_excess_branches(weight, route, expected):
    assert baggage_fee("economy", weight, route, False) == expected

@pytest.mark.parametrize("weight,items,infant,expected", [
    (8, 2, True, True), (8, 3, True, False),
    (8, 1, False, False), (7, 1, False, True), (7, 2, False, False),
])
def test_carry_on_all_decisions(weight, items, infant, expected):
    assert carry_on_ok(weight, items, infant) is expected

@pytest.mark.parametrize("minutes,baggage,international,expected", [
    (120, True, False, "open"), (60, True, False, "open"),
    (45, True, False, "late"), (44, True, False, "closed"),
    (180, False, True, "open"), (90, False, True, "late"),
    (89, False, True, "closed"),
])
def test_check_in_all_decisions(minutes, baggage, international, expected):
    assert check_in_status(minutes, baggage, international) == expected
