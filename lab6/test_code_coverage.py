"""Code (statement) coverage tests for airline_baggage.py.

Goal: execute every statement in the module at least once.

Run:
    coverage run -m pytest test_code_coverage.py
    coverage report -m
"""
import pytest
from airline_baggage import FREE_ALLOWANCE, baggage_fee, carry_on_ok, check_in_status


# ---------------- baggage_fee ----------------

def test_free_allowance_table():
    assert FREE_ALLOWANCE == {"economy": 15, "premium": 25, "business": 40}


def test_unknown_cabin_raises():
    with pytest.raises(ValueError, match="unknown cabin"):
        baggage_fee("first", 10, "domestic", False)


def test_negative_weight_raises():
    with pytest.raises(ValueError, match="invalid weight"):
        baggage_fee("economy", -1, "domestic", False)


def test_within_allowance_returns_zero():
    assert baggage_fee("economy", 10, "domestic", False) == 0


def test_member_gets_extra_allowance():
    # premium 25 + 10 member bonus = 35 -> 30 kg is free
    assert baggage_fee("premium", 30, "domestic", True) == 0


def test_domestic_small_excess():
    # economy 15, 20 kg -> 5 kg excess * 20
    assert baggage_fee("economy", 20, "domestic", False) == 100


def test_international_large_excess():
    # economy 15, 50 kg -> 35 kg excess, rate (45*2)+10 = 100
    assert baggage_fee("economy", 50, "international", False) == 3500


# ---------------- carry_on_ok ----------------

def test_carry_on_infant():
    assert carry_on_ok(10, 2, True) is True


def test_carry_on_overweight():
    assert carry_on_ok(8, 1, False) is False


def test_carry_on_ok():
    assert carry_on_ok(5, 1, False) is True


# ---------------- check_in_status ----------------

def test_check_in_open_with_baggage_international():
    # cutoff 60 + 60 = 120
    assert check_in_status(130, True, True) == "open"


def test_check_in_late_without_baggage():
    # cutoff 45, late window 30..44
    assert check_in_status(35, False, False) == "late"


def test_check_in_closed():
    assert check_in_status(10, False, False) == "closed"
